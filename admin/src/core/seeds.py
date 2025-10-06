# pylint: disable=import-error
# pylint: disable=unused-variable
"""Script de semillas para la base de datos."""

from src.core import board
from src.core import auth


def run():
    """Función para ejecutar el script de semillas."""

    permissions1 = auth.create_permission(name="view_site", description="Ver el Sitio")
    permissions2 = auth.create_permission(
        name="edit_site", description="Editar el Sitio"
    )
    permissions3 = auth.create_permission(
        name="delete_site", description="Eliminar el Sitio"
    )
    permissions4 = auth.create_permission(
        name="create_site", description="Crear el Sitio"
    )

    role1 = auth.create_role(name="admin", description="Administrador")
    role2 = auth.create_role(name="editor", description="Editor")
    role3 = auth.create_role(name="viewer", description="Visualizador")

    role1.permissions = auth.assign_permissions(
        role1, [permissions1, permissions2, permissions3, permissions4]
    )

    role2.permissions = auth.assign_permissions(
        role2, [permissions1, permissions2, permissions4]
    )
    role3.permissions = auth.assign_permissions(role3, [permissions1])

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
        user_name="viewer", email="viewer@mysite.com ", password="viewerpass", role=3
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

    board_tag1 = board.create_tag(name="Arqueológico")
    board_tag2 = board.create_tag(name="Natural")
    board_tag3 = board.create_tag(name="Cultural")
    board_tag4 = board.create_tag(name="Histórico")
    board_tag5 = board.create_tag(name="Turístico")
    board_tag6 = board.create_tag(name="Patrimonio de la Humanidad")

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
        created_by=user1,
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
        created_by=user1,
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
        created_by=user1,
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
        created_by=user1,
        tag=[board_tag1, board_tag3, board_tag4, board_tag6],
        inauguration_year=1610,
    )

    board.session.commit()
    board.session.close()
    print("Datos de semillas insertados correctamente.")
