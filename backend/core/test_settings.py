"""Configuración aislada para ejecutar pruebas sin PostgreSQL ni un archivo .env."""

import os

for name in ("DB_NAME", "DB_USER", "DB_PASSWORD"):
    os.environ.setdefault(name, "test")

from .settings import *  # noqa: E402,F403

SECRET_KEY = "solo-para-pruebas-locales"
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
