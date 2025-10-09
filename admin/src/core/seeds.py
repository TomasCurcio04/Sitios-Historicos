# pylint: disable=import-error
# pylint: disable=unused-variable
"""Script de semillas para la base de datos."""

from src.core import board
from src.core import auth

# from src.core.auth import feature_flag


def run():
    """Función para ejecutar el script de semillas."""

    permissions1 = auth.create_permission(
        permission_name="view_site", permission_description="Ver el Sitio"
    )
    permissions2 = auth.create_permission(
        permission_name="edit_site", permission_description="Editar el Sitio"
    )
    permissions3 = auth.create_permission(
        permission_name="delete_site", permission_description="Eliminar el Sitio"
    )
    permissions4 = auth.create_permission(
        permission_name="create_site", permission_description="Crear el Sitio"
    )

    role1 = auth.create_role(name="admin", description="Administrador")
    role2 = auth.create_role(name="editor", description="Editor")
    role3 = auth.create_role(name="viewer", description="Visualizador")

    role1.permission = [permissions1, permissions2, permissions3, permissions4]
    role2.permission = [permissions1, permissions2, permissions4]
    role3.permission = [permissions1]

    user1 = auth.create_user(
        user_name="admin",
        email="admin@mysite.com",
        password="adminpass",
        role=1,
        s_user=True,
    )
    user2 = auth.create_user(
        user_name="editor", email="editor@mysite.com", password="editorpass", role=2
    )
    user3 = auth.create_user(
        user_name="viewer", email="viewer@mysite.com", password="viewerpass", role=3
    )

    board_category1 = board.create_category(
        name="Monumento", description="Monumento histórico"
    )
    board_category2 = board.create_category(
        name="Edificio Histórico", description="Edificio histórico"
    )
    board_category3 = board.create_category(
        name="Sitio Arqueológico", description="Sitio arqueológico"
    )

    board_state1 = board.create_state(name="Santa Cruz")
    board_state2 = board.create_state(name="Córdoba")
    board_state3 = board.create_state(name="Buenos Aires")
    board_state4 = board.create_state(name="Jujuy")

    board_tag1 = board.create_tag(name="Arqueológico", slug="arqueologico")
    board_tag2 = board.create_tag(name="Natural", slug="natural")
    board_tag3 = board.create_tag(name="Cultural", slug="cultural")
    board_tag4 = board.create_tag(name="Histórico", slug="historico")
    board_tag5 = board.create_tag(name="Turístico", slug="turistico")
    board_tag6 = board.create_tag(
        name="Patrimonio de la Humanidad", slug="patrimonio-humanidad"
    )

    site1 = board.create_site(
        name="Cerro de los 7 colores",
        short_description="Cerro multicolor en Purmamarca",
        full_description="El Cerro de los 7 colores es una formación geológica ubicada en Purmamarca, Jujuy, Argentina. Es conocido por sus vibrantes colores que representan diferentes períodos geológicos.",
        city="Purmamarca",
        state=4,
        latitude=-23.2081,
        longitude=-65.4076,
        conservation_state="Bueno",
        category=3,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag2, board_tag5, board_tag6],
    )
    site2 = board.create_site(
        name="La Cueva de las Manos",
        short_description="Cueva con pinturas rupestres",
        full_description="La Cueva de las Manos es un sitio arqueológico ubicado en la provincia de Santa Cruz, Argentina. Es famosa por sus pinturas rupestres que datan de hace más de 9,000 años, incluyendo numerosas representaciones de manos humanas.",
        city="Perito Moreno",
        state=1,
        latitude=-46.5725,
        longitude=-70.0736,
        conservation_state="Excelente",
        category=3,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag1, board_tag3, board_tag6],
    )
    site3 = board.create_site(
        name="La Manzana Jesuítica",
        short_description="Conjunto histórico en Córdoba",
        full_description="La Manzana Jesuítica es un conjunto arquitectónico ubicado en la ciudad de Córdoba, Argentina. Fue declarado Patrimonio de la Humanidad por la UNESCO y alberga edificios históricos como la Iglesia de la Compañía de Jesús y la Universidad Nacional de Córdoba.",
        city="Córdoba",
        state=2,
        latitude=-31.4167,
        longitude=-64.1833,
        conservation_state="Muy Bueno",
        category=2,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag1, board_tag3, board_tag4, board_tag6],
    )
    site4 = board.create_site(
        name="Cabildo de Buenos Aires",
        short_description="Edificio histórico en Buenos Aires",
        full_description="El Cabildo de Buenos Aires es un edificio histórico ubicado en la Plaza de Mayo, en el centro de Buenos Aires, Argentina. Fue la sede del gobierno colonial español y desempeñó un papel crucial en la historia del país, especialmente durante la Revolución de Mayo de 1810.",
        city="Buenos Aires",
        state=3,
        latitude=-34.6083,
        longitude=-58.3708,
        conservation_state="Bueno",
        category=2,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag1, board_tag3, board_tag4, board_tag6],
        inauguration_year=1610,
    )

    flags = [
        auth.FeatureFlag(
            name="admin_maintenance_mode",
            description="Modo mantenimiento de administración",
            enabled=False,
            maintenance_message="El sistema de administración está en mantenimiento.",
            updated_by=user1.id_user,
        ),
        auth.FeatureFlag(
            name="portal_maintenance_mode",
            description="Modo mantenimiento de portal web",
            enabled=False,
            maintenance_message="El portal está en mantenimiento.",
            updated_by=user1.id_user,
        ),
        auth.FeatureFlag(
            name="reviews_enabled",
            description="Permitir nuevas reseñas",
            enabled=True,
            maintenance_message=None,
            updated_by=user1.id_user,
        ),
    ]
    board.db.session.add_all(flags)
    board.db.session.commit()
    board.db.session.close()
    print("✔️   DB rellenada con datos de prueba.")
