from django.forms import ModelForm
#Iportamos los Models.
from .models import Task

#Clase TaskForm: Esta clase hereda de ModelForm, que es una clase de Django que permite
# crear formularios basados en modelos de Django.
class TaskForm(ModelForm):
    #Creamos la clase Meta, la cual es para utilizar el import ModelForm.
    #Clase Meta: Esta es una clase interna dentro de TaskForm que se utiliza para especificar metadatos
    # del formulario. En este caso, se utiliza para indicar el modelo y los campos que se incluirán 
    # en el formulario.
    class Meta:
        #Hacemos referencia al modelo que queremos utilizar para crear el formulario.
        model = Task
        #Seleccionamos los campos que queremos para nuestro nuevo formulario de tareas.
        fields = ['title', 'description', 'important']