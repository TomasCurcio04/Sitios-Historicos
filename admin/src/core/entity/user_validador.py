import re

class UserValidator:
    def __init__(self, data):
        self.data = data 
        self.errors = {}
        self.data_cleaned = {} 
        self.EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    def validate(self):
        email = self.data.get("email", "").strip().lower()
        password = self.data.get("password", "")
        confirm_password = self.data.get("confirm_password", "")
        rol_str = self.data.get("rol", "")
        username = self.data.get("username", "").strip()

        if not re.match(self.EMAIL_REGEX, email):
            self.errors['email'] = "Email inválido"
        
        if len(password) < 6:
            self.errors['password'] = "La contraseña debe tener al menos 6 caracteres"
        
        if password != confirm_password:
            self.errors['confirm_password'] = "Las contraseñas no coinciden"
            
        
        try:
            rol_int = int(rol_str)
        except ValueError:
            self.errors['rol'] = "Debes seleccionar un rol válido"
            rol_int = None 

        if not self.errors:
            self.data_cleaned['email'] = email
            self.data_cleaned['username'] = username
            self.data_cleaned['password'] = password
    
            if rol_int is not None:
                self.data_cleaned['rol'] = rol_int
        
        return not self.errors