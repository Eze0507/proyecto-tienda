from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from seguridad.infrastructure.validators import (
    validar_solo_letras,
    validar_codigo_sucursal,
    validar_solo_numeros
)
from django.db import models
from datetime import time
from seguridad.domain.enums import ResultadoEvento, OrigenEvento
from enum import StrEnum
import uuid

def enum_a_choices(enum_cls: type[StrEnum]) -> list[tuple[str, str]]:
    return [(item.value, item.value) for item in enum_cls]

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
                fields = ["usuario", "sucursal"],
                name="unique_usuario_sucursal"
            )
        ]

class Bitacora(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid7,
        editable=False
    )
    tipo_evento = models.CharField(max_length=100)
    accion = models.CharField(max_length=100)
    resultado = models.CharField(max_length=50, choices=enum_a_choices(ResultadoEvento))
    motivo = models.CharField(max_length=100, null=True, blank=True)
    
    usuario = models.ForeignKey(
        Usuario, 
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="eventos_historicos"
    )
    usuario_nombre = models.CharField(max_length=150, null=True, blank=True)
    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="eventos_bitacora"
    )
    sucursal_nombre = models.CharField(max_length=150, null=True, blank=True)
    
    entidad = models.CharField(max_length=100)
    registro_id = models.CharField(max_length=100, null=True, blank=True)
    origen = models.CharField(max_length=30, choices=enum_a_choices(OrigenEvento))
    ip = models.CharField(max_length=60, null=True)
    
    datos_anteriores = models.JSONField(null=True, blank=True)
    datos_nuevos = models.JSONField(null=True, blank=True)
    
    occurred_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "bitacora"
        ordering = ["-occurred_at"]
        indexes = [
            models.Index(fields=["entidad", "registro_id"]),
            models.Index(fields=["-occurred_at"]),
            models.Index(fields=["tipo_evento", "accion"]),
        ]