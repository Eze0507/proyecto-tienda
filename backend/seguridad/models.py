from django.contrib.auth.models import AbstractUser
from seguridad.infrastructure.validators import (
    validar_codigo_sucursal,
    validar_solo_letras,
    validar_solo_numeros,
)
from django.db import models
from datetime import time

# Create your models here.
class Usuario(AbstractUser):
    class sigla(models.TextChoices):
        SC = "SC", "sc"
        LP = "LP", "lp"
        CB = "CB", "cb"
        OR = "OR", "or"
        PT = "PT", "pt"
        TJ = "TJ", "tj"
        CH = "CH", "ch"
        BN = "BN", "bn"
        PA = "PA", "pa"
    
    documento_identidad = models.CharField(max_length=8, unique=True, validators=[validar_solo_numeros])
    telefono = models.CharField(max_length=8, validators=[validar_solo_numeros], blank=True)
    debe_Cambiar_password = models.BooleanField(default=True)
    departamento_sigla = models.CharField(max_length=2, choices=sigla.choices)
    
    class Meta:
        db_table = "usuario"
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        permissions = [
            ("change_user_status", "Puede activar o inactivar usuarios"),
            ("reset_user_password", "Puede restablecer contraseñas de usuarios")
        ]

class Sucursal(models.Model):
    codigo = models.CharField(validators=[validar_codigo_sucursal], max_length=6, unique=True)
    nombre = models.CharField(max_length=50, unique=True, validators=[validar_solo_letras])
    telefono = models.CharField(max_length=8, validators=[validar_solo_numeros], blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    is_main = models.BooleanField(default=False, help_text="este atributo nos permite definir si una sucursal es la principal, solo puede exister una sucursal princiapl")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    usuario = models.ManyToManyField(Usuario, through="UsuarioSucursal", related_name="sucursales")
    
    class Meta:
        db_table = "sucursal"
        verbose_name = "sucursal"
        verbose_name_plural = "sucursales"
        constraints = [
            models.UniqueConstraint(fields=["is_main"], 
                                    condition=models.Q(is_main=True), 
                                    name="unique_main_sucursal")
        ]
        permissions = [
            ("change_sucursal_status", "Puede activar o desactivar sucursales"),
        ]

class Turno(models.Model):
    nombre = models.CharField(max_length=20, unique=True, validators=[validar_solo_letras])
    hora_inicio = models.TimeField(default=time(8,0))
    hora_final = models.TimeField(default=time(15,0))
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "turno"
        verbose_name = "turno"
        verbose_name_plural = "turnos"

class UsuarioSucursal(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, null=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "usuario_sucursal"
        verbose_name = "asignacion de empleado a sucursal"
        verbose_name_plural = "asignaciones de empleados a sucursales"
        constraints = [
            models.UniqueConstraint(
                fields = ["usuario", "sucursale"],
                name="unique_usuario_sucursal"
            )
        ]

