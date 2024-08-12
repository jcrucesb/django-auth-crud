from django.contrib import admin
from django.urls import path
#Agregamos las vistas.
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    #Utilizaremos el formulario; UserCreationForm.
    path('', views.home, name="home"),
    path('singup/', views.singup, name="registro"),
    #Creamos la vista para crear las tareas.
    path('tasks/', views.task, name="tasks"),
    #Creamos la vista para crear las tareas.
    path('tasks/create_tasks/', views.create_tasks, name="create_tasks"),
    # tASK dETAIL.
    path('tasks/<int:detail_id>/', views.task_detail, name="task_detail"),
    # Trea Realizada con fecha automática en la BD.
    path('tasks/<int:detail_id>/complete/', views.task_complete, name="task_complete"),
    # Eliminar una tarea en la BD solodel usuario que corresponda.
    path('tasks/<int:detail_id>/delete/', views.task_delete, name="task_delete"),
    #Treas Realizadas.
    path('task/task_finish/', views.task_finish, name="task_finish"),
    # Cerrar Sesión.
    path('logout/', views.cerrar_sesion, name="logout"),
    #
    path('signin/', views.signin, name="signin"),
    
]