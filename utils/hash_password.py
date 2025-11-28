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
