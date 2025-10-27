# pylint: disable=import-error
# pylint: disable=unused-variable
"""Script de semillas para la base de datos."""

from src.core import board
from src.core import auth

# from src.core.services.auth import feature_flag


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
    user4 = auth.create_user(
        user_name="supereditor",
        email="seditor@mysite.com",
        password="seditorpass",
        role=2,
        s_user=True,
    )
    user5 = auth.create_user(
        user_name="normaladmin",
        email="nadmin@mysite.com",
        password="nadminpass",
        role=1,
    )

    # Crear 25 usuarios adicionales
    for i in range(1, 26):
        auth.create_user(
            user_name=f"user{i}",
            email=f"user{i}@mysite.com",
            password=f"user{i}pass",
            role=(i % 3) + 1,
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
    board_state5 = board.create_state(name="Catamarca")
    board_state6 = board.create_state(name="Chaco")
    board_state7 = board.create_state(name="Chubut")
    board_state8 = board.create_state(name="Corrientes")
    board_state9 = board.create_state(name="Entre Ríos")
    board_state10 = board.create_state(name="Formosa")
    board_state11 = board.create_state(name="La Pampa")
    board_state12 = board.create_state(name="La Rioja")
    board_state13 = board.create_state(name="Mendoza")
    board_state14 = board.create_state(name="Misiones")
    board_state15 = board.create_state(name="Neuquén")
    board_state16 = board.create_state(name="Río Negro")
    board_state17 = board.create_state(name="Salta")
    board_state18 = board.create_state(name="San Juan")
    board_state19 = board.create_state(name="San Luis")
    board_state20 = board.create_state(name="Santa Fe")
    board_state21 = board.create_state(name="Santiago del Estero")
    board_state22 = board.create_state(name="Tierra del Fuego")
    board_state23 = board.create_state(name="Tucumán")
    board_state24 = board.create_state(name="Ciudad de Buenos Aires")

    board_tag1 = board.create_tag(name="Arqueológico")
    board_tag2 = board.create_tag(name="Natural")
    board_tag3 = board.create_tag(name="Cultural")
    board_tag4 = board.create_tag(name="Histórico")
    board_tag5 = board.create_tag(name="Turístico")
    board_tag6 = board.create_tag(name="Patrimonio de la Humanidad")

    site1 = board.create_site(
        name="Machu Picchu", short_description="Antigua ciudad inca en Perú", full_description="Machu Picchu es una antigua ciudad inca ubicada en las montañas de los Andes en Perú. Es conocida por su arquitectura impresionante, sus terrazas agrícolas y su importancia histórica y cultural como uno de los sitios arqueológicos más importantes de América del Sur.", city="Aguas Calientes", state=1, latitude=-13.1631, longitude=-72.5450, conservation_state="Bueno", category=1, is_visible=True, created_by=user1.id_user, tag=[board_tag1, board_tag3, board_tag4, board_tag6], inauguration_year=1450,
    )

    site2 = board.create_site(
        name="Cristo Redentor", short_description="Estatua de Cristo en Río de Janeiro", full_description="El Cristo Redentor es una icónica estatua de Jesucristo ubicada en la cima del Cerro del Corcovado en Río de Janeiro, Brasil. Es conocida por su impresionante altura, su ubicación panorámica y su importancia cultural y religiosa como símbolo de la ciudad y del país.", city="Río de Janeiro", state=2, latitude=-22.9519, longitude=-43.2105, conservation_state="Regular", category=2, is_visible=True, created_by=user1.id_user, tag=[board_tag3, board_tag4, board_tag5, board_tag6], inauguration_year=1931,
    )

    site3 = board.create_site(
        name="Chichén Itzá", short_description="Ruinas mayas en México", full_description="Chichén Itzá es un antiguo sitio arqueológico maya ubicado en la península de Yucatán, México. Es conocido por sus impresionantes estructuras arquitectónicas, como la pirámide de Kukulkán, y su importancia histórica y cultural como uno de los sitios más importantes de la civilización maya.", city="Tinum", state=3, latitude=20.6843, longitude=-88.5678, conservation_state="Malo", category=1, is_visible=True, created_by=user1.id_user, tag=[board_tag1, board_tag3, board_tag4, board_tag6], inauguration_year=600,
    )

    site4 = board.create_site(
        name="Catedral de Salta", short_description="Catedral barroca en Salta", full_description="La Catedral de Salta es una catedral barroca ubicada en la ciudad de Salta, provincia de Salta, Argentina. Es conocida por su arquitectura impresionante y su importancia religiosa e histórica en la región.", city="Salta", state=17, latitude=-24.7821, longitude=-65.4232, conservation_state="Bueno", category=2, is_visible=True, created_by=user1.id_user, tag=[board_tag3, board_tag4], inauguration_year=1858,
    )

    site5 = board.create_site(
        name="Parque Nacional Iguazú", short_description="Parque con las famosas Cataratas del Iguazú", full_description="El Parque Nacional Iguazú es un área protegida ubicada en la provincia de Misiones, Argentina. Es conocido por albergar las impresionantes Cataratas del Iguazú, una de las maravillas naturales del mundo, y es Patrimonio de la Humanidad por la UNESCO.", city="Puerto Iguazú", state=14, latitude=-25.6953, longitude=-54.4367, conservation_state="Regular", category=1, is_visible=True, created_by=user1.id_user, tag=[board_tag2, board_tag5, board_tag6], inauguration_year=1934,
    )

    site6 = board.create_site(
        name="Teatro Colón", short_description="Famoso teatro de ópera en Buenos Aires", full_description="El Teatro Colón es uno de los teatros de ópera más importantes del mundo, ubicado en Buenos Aires, Argentina. Es conocido por su acústica excepcional y su arquitectura impresionante, y ha sido escenario de numerosas producciones artísticas de renombre internacional.", city="Buenos Aires", state=3, latitude=-34.6014, longitude=-58.3816, conservation_state="Malo", category=2, is_visible=True, created_by=user1.id_user, tag=[board_tag3, board_tag4, board_tag5], inauguration_year=1908,
    )

    site7 = board.create_site(
        name="Ruinas de San Ignacio Miní", short_description="Ruinas de una antigua misión jesuítica", full_description="Las Ruinas de San Ignacio Miní son un conjunto arqueológico ubicado en la provincia de Misiones, Argentina. Fueron una de las misiones jesuíticas establecidas en el siglo XVII y son Patrimonio de la Humanidad por la UNESCO debido a su importancia histórica y cultural.", city="San Ignacio", state=14, latitude=-27.2556, longitude=-55.6158, conservation_state="Regular", category=3, is_visible=True, created_by=user1.id_user, tag=[board_tag1, board_tag3, board_tag4, board_tag6], inauguration_year=1696,
    )

    site8 = board.create_site(
        name="Glaciar Perito Moreno", short_description="Imponente glaciar en la Patagonia", full_description="El Glaciar Perito Moreno es un glaciar ubicado en el Parque Nacional Los Glaciares, en la provincia de Santa Cruz, Argentina. Es uno de los glaciares más accesibles y espectaculares del mundo, conocido por sus impresionantes desprendimientos de hielo y su belleza natural.", city="El Calafate", state=1, latitude=-50.4967, longitude=-73.1375, conservation_state="Bueno", category=1, is_visible=True, created_by=user1.id_user, tag=[board_tag2, board_tag5, board_tag6], inauguration_year=1917,
    )

    site9 = board.create_site(
        name="Catedral de La Plata", short_description="Imponente catedral gótica en La Plata", full_description="La Catedral de La Plata es una catedral gótica ubicada en la ciudad de La Plata, provincia de Buenos Aires, Argentina. Es una de las catedrales más grandes de América del Sur y destaca por su arquitectura impresionante y sus vitrales coloridos.", city="La Plata", state=3, latitude=-34.9214, longitude=-57.9544, conservation_state="Malo", category=2, is_visible=True, created_by=user1.id_user, tag=[board_tag3, board_tag4], inauguration_year=1932,
    )

    site10 = board.create_site(
        name="Parque Nacional Talampaya", short_description="Parque con formaciones rocosas y petroglifos", full_description="El Parque Nacional Talampaya es un área protegida ubicada en la provincia de La Rioja, Argentina. Es conocido por sus impresionantes formaciones rocosas, cañones y petroglifos que datan de miles de años, y es Patrimonio de la Humanidad por la UNESCO.", city="Villa Unión", state=12, latitude=-29.9875, longitude=-67.5381, conservation_state="Bueno", category=1, is_visible=True, created_by=user1.id_user, tag=[board_tag1, board_tag2, board_tag6], inauguration_year=1997,
    )

    site11 = board.create_site(
        name="Estancia Jesuítica de Alta Gracia", short_description="Antigua estancia jesuítica", full_description="La Estancia Jesuítica de Alta Gracia es un conjunto histórico ubicado en la ciudad de Alta Gracia, provincia de Córdoba, Argentina. Fue una de las estancias establecidas por los jesuitas en el siglo XVII y es Patrimonio de la Humanidad por la UNESCO debido a su importancia histórica y cultural.", city="Alta Gracia", state=2, latitude=-31.6375, longitude=-64.4175, conservation_state="Regular", category=2, is_visible=True, created_by=user1.id_user, tag=[board_tag1, board_tag3, board_tag4, board_tag6], inauguration_year=1643,
    )

    site12 = board.create_site(
        name="Parque Nacional Los Alerces", short_description="Parque con bosques y lagos", full_description="El Parque Nacional Los Alerces es un área protegida ubicada en la provincia de Chubut, Argentina. Es conocido por sus bosques de alerces milenarios, lagos cristalinos y montañas, y es Patrimonio de la Humanidad por la UNESCO debido a su biodiversidad y belleza natural.", city="Esquel", state=7, latitude=-42.9081, longitude=-71.3175, conservation_state="Malo", category=1, is_visible=True, created_by=user1.id_user, tag=[board_tag2, board_tag5, board_tag6], inauguration_year=1937,
    )

    site13 = board.create_site(
        name="Museo Nacional de Bellas Artes", short_description="Principal museo de arte en Argentina", full_description="El Museo Nacional de Bellas Artes es el principal museo de arte en Argentina, ubicado en Buenos Aires. Alberga una extensa colección de obras de arte argentino e internacional, que abarca desde la antigüedad hasta el arte contemporáneo.", city="Buenos Aires", state=3, latitude=-34.5881, longitude=-58.4000, conservation_state="Bueno", category=2, is_visible=True, created_by=user1.id_user, tag=[board_tag3, board_tag4], inauguration_year=1895,
    )

    site14 = board.create_site(
        name="Parque Nacional Sierra de las Quijadas", short_description="Parque con formaciones rocosas y fósiles", full_description="El Parque Nacional Sierra de las Quijadas es un área protegida ubicada en la provincia de San Luis, Argentina. Es conocido por sus impresionantes formaciones rocosas, cañones y fósiles que datan de millones de años, y es un destino popular para el senderismo y la observación de la naturaleza.", city="Santa Rosa de Conlara", state=19, latitude=-32.3033, longitude=-66.9875, conservation_state="Regular", category=1, is_visible=True, created_by=user1.id_user, tag=[board_tag1, board_tag2, board_tag6], inauguration_year=1991,
    )

    site15 = board.create_site(
        name="Casa Rosada", short_description="Sede del gobierno argentino", full_description="La Casa Rosada es la sede del gobierno argentino, ubicada en la Plaza de Mayo, en el centro de Buenos Aires. Es conocida por su distintivo color rosa y su importancia histórica y política, ya que ha sido el lugar desde donde se han anunciado importantes eventos nacionales.", city="Buenos Aires", state=3, latitude=-34.6083, longitude=-58.3708, conservation_state="Malo", category=2, is_visible=True, created_by=user1.id_user, tag=[board_tag3, board_tag4], inauguration_year=1898,
    )

    site16 = board.create_site(
        name="Parque Nacional Quebrada del Condorito", short_description="Parque con paisajes montañosos", full_description="El Parque Nacional Quebrada del Condorito es un área protegida ubicada en la provincia de Córdoba, Argentina. Es conocido por sus impresionantes paisajes montañosos, valles y la presencia del cóndor andino, y es un destino popular para el senderismo y la observación de la naturaleza.", city="La Paz", state=2, latitude=-31.6792, longitude=-64.7031, conservation_state="Bueno", category=1, is_visible=True, created_by=user1.id_user, tag=[board_tag1, board_tag2, board_tag6], inauguration_year=1996,
    )

    site17 = board.create_site(
        name="Iglesia de San Francisco", short_description="Iglesia histórica en Salta", full_description="La Iglesia de San Francisco es una iglesia histórica ubicada en la ciudad de Salta, provincia de Salta, Argentina. Es conocida por su arquitectura barroca y su importancia religiosa e histórica en la región.", city="Salta", state=17, latitude=-24.7821, longitude=-65.4232, conservation_state="Regular", category=2, is_visible=True, created_by=user1.id_user, tag=[board_tag3, board_tag4], inauguration_year=1716,
    )

    site18 = board.create_site(
        name="Parque Nacional El Palmar", short_description="Parque con palmeras y fauna", full_description="El Parque Nacional El Palmar es un área protegida ubicada en la provincia de Entre Ríos, Argentina. Es conocido por sus extensos bosques de palmeras yatay, su biodiversidad y su importancia ecológica, y es un destino popular para el ecoturismo y la observación de la naturaleza.", city="Colón", state=9, latitude=-31.8997, longitude=-58.0844, conservation_state="Malo", category=1, is_visible=True, created_by=user1.id_user, tag=[board_tag2, board_tag5, board_tag6], inauguration_year=1966,
    )

    site19 = board.create_site(
        name="Museo Evita", short_description="Museo dedicado a Eva Perón", full_description="El Museo Evita es un museo dedicado a la vida y obra de Eva Perón, ubicado en Buenos Aires, Argentina. Alberga una colección de objetos personales, fotografías y documentos relacionados con Eva Perón y su impacto en la historia argentina.", city="Buenos Aires", state=3, latitude=-34.6037, longitude=-58.3816, conservation_state="Bueno", category=2, is_visible=True, created_by=user1.id_user, tag=[board_tag3, board_tag4], inauguration_year=2002,
    )

    site20 = board.create_site(
        name="Parque Nacional Chaco", short_description="Parque con bosques y fauna", full_description="El Parque Nacional Chaco es un área protegida ubicada en la provincia del Chaco, Argentina. Es conocido por sus extensos bosques chaqueños, su biodiversidad y su importancia ecológica, y es un destino popular para el ecoturismo y la observación de la naturaleza.", city="Resistencia", state=6, latitude=-27.4519, longitude=-58.9865, conservation_state="Regular", category=1, is_visible=True, created_by=user1.id_user, tag=[board_tag2, board_tag5, board_tag6], inauguration_year=1954,
    )

    site21 = board.create_site(
        name="Parque Nacional Monte León", short_description="Primer parque nacional marino de Argentina", full_description="El Parque Nacional Monte León es un área protegida ubicada en la provincia de Santa Cruz, Argentina. Es conocido por ser el primer parque nacional marino de Argentina, y alberga una gran diversidad de fauna marina, incluyendo pingüinos, lobos marinos y aves marinas.", city="Puerto Santa Cruz", state=1, latitude=-50.0333, longitude=-68.5167, conservation_state="Malo", category=1, is_visible=True, created_by=user1.id_user, tag=[board_tag2, board_tag5, board_tag6], inauguration_year=2004,
    )

    site22 = board.create_site(
        name="Parque Nacional Aconquija", short_description="Parque con montañas y biodiversidad", full_description="El Parque Nacional Aconquija es un área protegida ubicada en la provincia de Tucumán, Argentina. Es conocido por sus impresionantes montañas, valles y su biodiversidad, y es un destino popular para el senderismo y la observación de la naturaleza.", city="Tafí del Valle", state=23, latitude=-26.8497, longitude=-65.5167, conservation_state="Bueno", category=1, is_visible=True, created_by=user1.id_user, tag=[board_tag2, board_tag5, board_tag6], inauguration_year=2010,
    )

    site23 = board.create_site(
        name="Parque Nacional Los Glaciares", short_description="Parque con glaciares y montañas", full_description="El Parque Nacional Los Glaciares es un área protegida ubicada en la provincia de Santa Cruz, Argentina. Es conocido por sus impresionantes glaciares, montañas y lagos, y es Patrimonio de la Humanidad por la UNESCO debido a su biodiversidad y belleza natural.", city="El Calafate", state=1, latitude=-50.4967, longitude=-73.1375, conservation_state="Regular", category=1, is_visible=True, created_by=user1.id_user, tag=[board_tag2, board_tag5, board_tag6], inauguration_year=1937,
    )

    site24 = board.create_site(
        name="Parque Nacional Baritú", short_description="Parque con selva y biodiversidad", full_description="El Parque Nacional Baritú es un área protegida ubicada en la provincia de Salta, Argentina. Es conocido por su selva montana, su biodiversidad y su importancia ecológica, y es un destino popular para el ecoturismo y la observación de la naturaleza.", city="Santa Victoria Este", state=17, latitude=-22.1333, longitude=-63.7667, conservation_state="Malo", category=1, is_visible=True, created_by=user1.id_user, tag=[board_tag2, board_tag5, board_tag6], inauguration_year=1974,
    )

    site25 = board.create_site(
        name="Parque Nacional San Guillermo", short_description="Parque con montañas y fauna", full_description="El Parque Nacional San Guillermo es un área protegida ubicada en la provincia de San Juan, Argentina. Es conocido por sus impresionantes montañas, valles y la presencia del guanaco, y es un destino popular para el senderismo y la observación de la naturaleza.", city="Jáchal", state=18, latitude=-30.5000, longitude=-68.5000, conservation_state="Bueno", category=1, is_visible=True, created_by=user1.id_user, tag=[board_tag2, board_tag5, board_tag6], inauguration_year=1996,
    )

    site26 = board.create_site(
        name="Parque Nacional Quebrada del Condorito", short_description="Parque con quebradas y cóndores", full_description="El Parque Nacional Quebrada del Condorito es un área protegida ubicada en la provincia de Córdoba, Argentina. Es conocido por sus impresionantes quebradas, su biodiversidad y la presencia del cóndor andino, y es un destino popular para el senderismo y la observación de la naturaleza.", city="La Paz", state=12, latitude=-31.0000, longitude=-64.0000, conservation_state="Regular", category=1, is_visible=True, created_by=user1.id_user, tag=[board_tag2, board_tag5, board_tag6], inauguration_year=1996,
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
    from src.core.database import db

    db.session.add_all(flags)
    db.session.commit()

    print("✔️  Base de datos rellenada con datos de prueba.")
