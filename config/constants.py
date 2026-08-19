"""
Constantes compartidas entre modelos, controladores y rutas.
Centralizarlas evita que la lista de roles o la política de contraseñas
queden desincronizadas entre archivos.
"""

ROLES = ("superadmin", "admin", "supervisor", "operador")
PASSWORD_MIN_LENGTH = 6
