from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
# Llamamos este comando para ejecutar un formulario.
# UserCreationForm; SIRVE PARA CREAR UN USUARIO.
# AuthenticationForm; Validar si un usuario existe. (Loguin)
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# Utilizaremos la librería mencionada para poder registrar a los nuevos usuarios.
# Importamos el modelo de User que viene en DJANGO.
from django.contrib.auth.models import User
# Utilizamso este import para ver si el usuario tiene session activa, NO verifica si esta bien logueado o no.
#authenticate; Es el que verifica si el usuario existe en la BD.
from django.contrib.auth import login, logout, authenticate
# Importamos IntegrityError para detectar un error en la BD.
from django.db import IntegrityError
# Agregamos el archivo forms que contiene el nuevo formulario para crear tarease importamos la clase, TaskForm
from .forms import TaskForm
#Necesitamos el model para ñistar todas las tareas.
from .models import Task
#desde sjango.urils, importamos timezone.
from django.utils import timezone
# Verificamos que el usuario esté correctamente logueado con la import de login_required.
from django.contrib.auth.decorators import login_required

# Create your views here.
# Creamos el método de Index.
def home(request):
    return render(request, 'home.html')

#
def singup(request):
    # Mostrar la vista o recibir los datos del formulario por POST.
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        try:
            # Debemos verificar si las contraseñas cohincide.
            if request.POST["password1"] == request.POST["password2"]:
                # Guardar los datos del formulario.
                # Al usar estos métodos para crear a un usuario, realiza la validación siguiente;
                # si existe el usuario, por ende, no lo inserta si llegase a existir.
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password2'])
                # Guardamos los datos obtenidos en la BD.
                user.save()
                # Llamamos el import Loguin.
                login(request, user)
                # print(user)
                return redirect('create_tasks')
        except IntegrityError:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                # Enviamos un mensaje de Alerta.
                'error': 'El usuario ya existe'
            })
    return render(request, 'signup.html', {
        'form': UserCreationForm,
        # Enviamos un mensaje de Alerta.
        'error': 'La Password es incorrecta'
    })

#Verificamos el user esté logueado antes de entrar a tareas.
@login_required 
# Cremos la vista para crear Tareas (Tasks)
def task(request):
    #Obtenemos todas las tareas.
    #tasks = Task.objects.all()
    # Solo mostrar las tareas que corresponde al usuario que inició sessión.
    #filter; Utilizamos la propiedad user y le pasamos el user que inició sessión.
    #El user, es del models, osea de la tabla task, es la foreygn_key.
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    # datecompleted__isnull; es lapropieda del model de Task, yle decimos que solo nos 
    # traiga las tareas completadas del usuario que inició sessión.
    #tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    print(tasks)
    return render(request, 'tasks/tasks.html',{
            'tasks': tasks
        })

@login_required 
#Renderizamos el HTML de create_tasks.html
def create_tasks(request):
    if request.method == 'GET':
        #Pasamos el formulario que creamos al html.
        return render(request, 'tasks/create_task.html', {
            'form_create_tasks': TaskForm
        })
    else:
        try:
            #
            print(request.POST)
            #Creamos el Objeto TASKS. y le pasamos los datos por POST.
            #Es un formulario que recibe los values de los inputs.
            form = TaskForm(request.POST)
            # Con esto, commit=False, hacemos que NO guarde los datos en la BD automaticamente.
            # Si es commit=False, los datos se guardan automáticamente.
            new_tasks = form.save(commit=False)
            #Obtener el usuario que está creabndo la tarea por medio de su sessión.
            new_tasks.user = request.user
            print(form)
            #Obtenemos el nombre de Usuario Correctamente.
            print(new_tasks.user)
            #Ahora guardamos los datos directamente desde la BD.
            new_tasks.save()
            #Pasamos el formulario que creamos al html.
            return render(request, 'tasks/create_task.html', {
                'form_create_tasks': TaskForm
            })
        except ValueError:
            #Si llegamos a tener error, mandamos la misma vista pero con un mensaje de error.
            return render(request, 'tasks/create_task.html', {
                'form_create_tasks': TaskForm,
                'error': 'Se ha producido un error, vuelva a intentarlo..'
            }) 

@login_required 
#OJO, el parametro de la url, debe ser el mismo nombre la cual se está pasando a la ruta.
#path('tasks/<int:detail_id>/', views.task_detail, name="task_detail"); 
#ese nombre de variable, <int:detail_id>, debe ser el mismo nombre del parámetro de la función.
def task_detail(request, detail_id):
    if request.method == 'GET':
        # print(detail_id)
        #description = Task.objects.get(pk=detail_id)
        task = get_object_or_404(Task, pk=detail_id, user=request.user)
        # Para editar los campos, llamamos al archivo; TaskForm, el cual contiene los inputs para registrar
        #una tarea, en este caso lo utilizaremos para editar la información.
        #En esta oportunidad al formulario le pasamos los datos que tiene la variable, task. 
        form = TaskForm(instance=task)
        print(task)
        return render(request, 'tasks/task_details.html', {
            'task': task,
            'form':form
        })
    else:
        try:
            print(request.POST)
            #description = Task.objects.get(pk=detail_id)
            #El usuario user; user=request.user, debe cohincidir con el usuario que va a editar la tarea.
            task = get_object_or_404(Task, pk=detail_id, user=request.user)
            # Para editar los campos, llamamos al archivo; TaskForm, el cual contiene los inputs para registrar
            #una tarea, en este caso lo utilizaremos para editar la información.
            #En esta oportunidad al formulario le pasamos los datos que tiene la variable, task. 
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'tasks/task_details.html', {
            'error': 'Se ha producido un error, vuelva a intentarlo',
            'task':task,
            'form': form,
        })

@login_required 
#Tarea Completada.
def task_complete(request, detail_id):
    #Obtenemos la tarea que corresponde al usuario logueado.
    task = get_object_or_404(Task, pk=detail_id, user=request.user)
    print(task)
    if request.method == 'POST':
        #Cambiamos la propiedad de la tabla Task por la fecha de Modificación.
        task.datecompleted = timezone.now()
        #Guardamos el dato en la BD.
        task.save() 
        return redirect('tasks')

@login_required 
#Eliminar una tarea.
def task_delete(request, detail_id):
     #Obtenemos la tarea que corresponde al usuario logueado.
    task = get_object_or_404(Task, pk=detail_id, user=request.user)
    print(task)
    if request.method == 'POST':
        #Eliminamos de la BD.
        task.delete() 
        return redirect('tasks')

@login_required 
#Tareas que están finalizadas.
def task_finish(request):
    #Realizamos un filtro para obtener las tareas que NO estén finalizadas.  
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    print(tasks)
    return render(request, 'tasks/task_finish.html',{
            'tasks': tasks
        })

@login_required 
# Crear Cerrar Sesión. OJO, NOSE PUEDE COLOCAR EL NOMBRE DE logout, PORQUE GENERA CONFLICTO CON EL IMPORT,
# DEBE SER CUALQUIER OTRO NOMBRE.
def cerrar_sesion(request):
    # Llamamos al método que importamos, logout.
    logout(request)
    return redirect('home')

# Crear el registro. OJO, NO SE PUEDE COLOCAR LOGIN EN EL NOMBRE DE LA FUNCIÓN, debido a que ya
# se está utilizando en el import y genera problemas.
def signin(request):
    # Verificamos i estamos enviando un formulario o no.
    if request.method == 'GET':
        return render(request, 'tasks/signin.html', {
            'autenticar': AuthenticationForm
        })
    else:
        #return redirect('create_tareas').
        #User nos devuelve un None si no existe el usuario.
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        #print(user)
        #Realizamos la validación del usuario es None.
        if user is None:
            return render(request, 'tasks/signin.html', {
                'autenticar': AuthenticationForm,
                'error': 'El Usuario o Password es incorrecta'
            })
        else:
            #ANTES DE REDIRECCIONAR, DEBEMOS GUARDAR LA SESSION.
            login(request, user)
            return redirect('create_tasks')