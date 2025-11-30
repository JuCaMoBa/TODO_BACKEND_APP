"""funcion para hashear contraseñas"""
import bcrypt


def hash_password(plain_password: str) -> str:
    """Hashea una contraseña en texto plano utilizando bcrypt.

    Args:
        plain_password (str): La contraseña en texto plano.

    Returns:
        str: La contraseña hasheada.
    """
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña en texto plano coincide con una contraseña hasheada.

    Args:
        plain_password (str): La contraseña en texto plano.
        hashed_password (str): La contraseña hasheada.

    Returns:
        bool: True si las contraseñas coinciden, False en caso contrario.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
