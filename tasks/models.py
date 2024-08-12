from django.db import models
# Utilizaremos la librería mencionada para poder registrar a los nuevos usuarios.
# Importamos el model de User que viene en DJANGO.
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    description=models.TextField(blank=True)
    #Se inserta la hra por defecto.
    created=models.DateTimeField(auto_now_add=True)
    datecompleted=models.DateTimeField(null=True)
    #blank=True; Sirve para dejar opcionalun inputs, etc, por parte del usuario.
    #null=True; Se inserta si o si en la BD.
    #datecompleted=models.DateTimeField(null=True, blank=True)
    #Camnpo BOOLEANO en False..
    important = models.BooleanField(default=False)
    #Relacionamos la tarea con algún usuario.
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        #Retornamos de esta clase la propiedad llamada Title.
        #Este es el nombre del Proyecto que aparece en DASHBOARD ADMIN.
        return self.title + '- by ' + self.user.username
