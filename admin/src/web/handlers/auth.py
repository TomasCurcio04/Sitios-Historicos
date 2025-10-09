

def is_authenticated(session):
    """Verifica que el usuario este autenticado."""
    return session.get("user") is not None