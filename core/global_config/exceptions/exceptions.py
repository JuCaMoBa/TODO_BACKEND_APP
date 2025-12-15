"""Modulo que define las excepciones personalizadas para la configuracion global."""


class RepositoryConnectionError(Exception):
    """Excepcion lanzada cuando hay un error al conectar con la base de datos."""
    pass


class RepositoryConflictError(Exception):
    """Expecion lanzada cuando hy un conflicto con los datos en la base de datos """
    pass


class RepositoryQueryError(Exception):
    """Excepcion lanzada cuando hay un error interno en la base de datos"""
    pass


class InvalidCredentialsError(Exception):
    """Excepción de dominio para credenciales inválidas."""
    pass


class ExceptionDataError(Exception):
    """Excepción de dominio para errores en obtener datos de user o tasks"""
    pass
