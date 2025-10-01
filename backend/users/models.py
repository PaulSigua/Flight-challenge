from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Aquí puedes añadir campos extra si los necesitas en el futuro,
    # como 'phone_number = models.CharField(max_length=15, blank=True, null=True)'
    
    # Si quieres que el email sea requerido y el campo de login principal,
    # puedes hacer ajustes (aunque para empezar, AbstractUser ya es suficiente):
    email = models.EmailField(unique=True, blank=False, null=False)
    
    # Si usas AbstractUser, no necesitas redefinir username, password, etc.
    # Pero puedes cambiar qué campo se usa para login:
    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["username"]

    class Meta:
        # Esto es importante si cambiaste el nombre del modelo
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username