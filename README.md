📖 Descripción

Este proyecto fue desarrollado para la materia Proyecto de Software 2025 de la Universidad Nacional de La Plata.

La aplicación tiene como objetivo centralizar información sobre sitios históricos de distintas ciudades del país, permitiendo su administración, consulta y visualización mediante mapas interactivos.

El sistema está compuesto por:

🔒 Aplicación privada de administración desarrollada con Flask.
🌐 Portal público desarrollado con Vue.js.
🗺️ Integración con mapas interactivos y geolocalización.
🗄️ Base de datos PostgreSQL con soporte geoespacial.
🔑 Sistema de autenticación y control de roles.
🚀 Tecnologías utilizadas:

Backend:
- Python 3.12
- Flask
- SQLAlchemy
- PostgreSQL 16
- Flask-Session
- Poetry

Frontend:
- Vue.js 3.5
- HTML5
- CSS3
- JavaScript

Herramientas:
+ Git & GitHub
- GitLab
- Postman
- MinIO (etapa 2)

⚙️ Funcionalidades principales
🔐 Aplicación privada (Administración)
Usuarios y autenticación
Login con manejo manual de sesiones.
Control de permisos y roles.
CRUD de usuarios.
Bloqueo/desbloqueo de usuarios.
Gestión de Feature Flags.
Gestión de sitios históricos
Alta, baja y modificación de sitios.
Búsqueda avanzada.
Exportación a CSV.
Historial de modificaciones.
Gestión de tags.
Moderación
Moderación de reseñas.
Gestión de imágenes.
Administración de contenido.

🌍 Portal público
Exploración de sitios
Listado responsive de sitios históricos.
Búsqueda avanzada y filtros.
Visualización en mapas interactivos.
Detalle completo de cada sitio.
Usuarios públicos
Login con Google.
Favoritos.
Reseñas y puntuaciones.
Perfil de usuario.
🗺️ Características destacadas
📱 Diseño Mobile First
🧩 Arquitectura MVC
🔒 Seguridad y manejo de sesiones
🌎 Datos georreferenciados
📊 Exportación de información
🏷️ Sistema de etiquetas
⭐ Sistema de reseñas y favoritos
🛠️ Instalación del proyecto
1️⃣ Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_PROYECTO>
2️⃣ Configurar backend
Crear entorno virtual e instalar dependencias
poetry install
Configurar variables de entorno

Crear archivo .env:

FLASK_APP=run.py
FLASK_ENV=development

DATABASE_URL=postgresql://usuario:password@localhost:5432/bd_sitios

SECRET_KEY=tu_clave_secreta
SESSION_TYPE=filesystem
3️⃣ Configurar base de datos

Crear la base PostgreSQL y ejecutar:

poetry run flask reset-db
poetry run flask seed-db
4️⃣ Ejecutar backend
poetry run flask run

Servidor disponible en:

http://127.0.0.1:5000
5️⃣ Configurar frontend

Ir a la carpeta web:

cd web
npm install
npm run dev

Frontend disponible en:

http://localhost:5173
👥 Roles del sistema
Rol	Permisos
Usuario Público	Ver sitios, favoritos y reseñas
Editor	Gestionar sitios y tags
Administrador	Gestionar usuarios y exportaciones
System Admin	Acceso total + feature flags
🔒 Seguridad
Contraseñas almacenadas con hash seguro.
Validaciones cliente/servidor.
Manejo seguro de sesiones.
Protección mediante permisos por módulo.
Uso de SQLAlchemy para evitar SQL Injection.
📸 Capturas (pendiente)

Agregar imágenes del sistema:

Login
Dashboard
Listado de sitios
Mapa interactivo
Portal público
📌 Estado del proyecto

🚧 Proyecto en desarrollo — Trabajo Integrador 2025.

👨‍💻 Integrantes: Grupo 10
- Tomás Curcio
- J.C
- F.G

📚 Materia

Proyecto de Software 2025
Licenciatura en Sistemas
Universidad Nacional de La Plata

📄 Licencia

Este proyecto fue desarrollado con fines educativos para la cursada de Proyecto de Software 2025.
