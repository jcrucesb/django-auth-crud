from django.contrib import admin
#Importamos el modelo Task, esto es para que aparezca en el dasboard de ADMIN.
from .models import Task

#Creamos una clase que heredará de Task.
class TaskAdmin(admin.ModelAdmin):
    #Elejimos los campos que queremos deshabilitar para el usuario. En este caso, mostramos el campo, created, el cual
    #se inserta por defecto en la BD y lo queremos visualizar.
    readonly_fields = ("created",)
# Register your models here.
admin.site.register(Task, TaskAdmin)