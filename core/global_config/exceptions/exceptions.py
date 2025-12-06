"""Modulo que define las excepciones personalizadas para la configuracion global."""


class RepositoryConnectionError(Exception):
    """Excepcion lanzada cuando hay un error al conectar con la base de datos."""
    pass


class InvalidCredentialsError(Exception):
    """Excepción de dominio para credenciales inválidas."""
    pass


class UserDataError(Exception):
    """Excepción de dominio para errores de usuarios"""
    pass
