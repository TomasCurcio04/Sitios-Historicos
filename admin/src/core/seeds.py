# pylint: disable=import-error
# pylint: disable=unused-variable
"""Script de semillas para la base de datos."""

from src.core.services import board
from src.core.services.auth.role_serv import create_role
from src.core.services.auth.user_serv import create_user
from src.core.services.auth.user_serv import create_user_public
from src.core.services.auth.permission_serv import create_permission
from src.core.entity.feature_flag import FeatureFlag
from src.core.database import db
from src.core.entity.site_image import SiteImage
from src.core.entity.review import Review
from src.core.entity.public_user import PublicUser
from src.core.entity.site_visit import SiteVisit
from src.core.entity.site_favorite import SiteFavorite



def run():
    """Función para ejecutar el script de semillas."""

    permissions1 = create_permission(
        permission_name="site_view", permission_description="Ver el Sitio"
    )
    permissions2 = create_permission(
        permission_name="site_edit", permission_description="Editar el Sitio"
    )
    permissions3 = create_permission(
        permission_name="site_delete", permission_description="Eliminar el Sitio"
    )
    permissions4 = create_permission(
        permission_name="site_create", permission_description="Crear el Sitio"
    )
    permissions5 = create_permission(
        permission_name="site_export_CSV", permission_description="Exportar CSV"
    )
    permissions6 = create_permission(
        permission_name="site_list", permission_description="Listar sitios"
    )
    permissions7 = create_permission(
        permission_name="user_view", permission_description="Ver Usuario"
    )
    permissions8 = create_permission(
        permission_name="user_list", permission_description="Listar Usuarios"
    )
    permissions9 = create_permission(
        permission_name="user_edit", permission_description="Editar Usuario"
    )
    permissions10 = create_permission(
        permission_name="user_delete", permission_description="Eliminar Usuario"
    )
    permissions11 = create_permission(
        permission_name="user_create", permission_description="Crear Usuario"
    )
    permission12 = create_permission(
        permission_name="site_history_view",
        permission_description="Ver un Historico de Sitio",
    )
    permission13 = create_permission(
        permission_name="site_history_list",
        permission_description="Listar Historicos de Sitio",
    )
    permission14 = create_permission(
        permission_name="tag_view", permission_description="Ver Tag"
    )
    permission15 = create_permission(
        permission_name="tag_list", permission_description="Listar Tags"
    )
    permission16 = create_permission(
        permission_name="tag_create", permission_description="Crear Tag"
    )
    permission17 = create_permission(
        permission_name="tag_edit", permission_description="Editar Tag"
    )
    permission18 = create_permission(
        permission_name="tag_delete", permission_description="Eliminar Tag"
    )
    permission19 = create_permission(
        permission_name="review_view", permission_description="Ver Reseña"
    )
    permission20 = create_permission(
        permission_name="review_list", permission_description="Listar Reseñas"
    )
    permission21 = create_permission(
        permission_name="review_create", permission_description="Crear Reseña"
    )
    permission22 = create_permission(
        permission_name="review_edit", permission_description="Editar Reseña"
    )
    permission23 = create_permission(
        permission_name="review_delete", permission_description="Eliminar Reseña"
    )
    permission24 = create_permission(
        permission_name="review_moderate", permission_description="Moderar Reseña"
    )
    permission25 = create_permission(
        permission_name="review_publish", permission_description="Publicar Reseña"
    )


    role1 = create_role(name="admin", description="Administrador")
    role2 = create_role(name="editor", description="Editor")
    role3 = create_role(name="moderator", description="Moderador")
    # role4 = create_role(name="public", description="Usuario Publico")

    role1.permission = [
        permissions1,
        permissions2,
        permissions3,
        permissions4,
        permissions5,
        permissions6,
        permissions7,
        permissions8,
        permissions9,
        permissions10,
        permissions11,
        permission12,
        permission13,
        permission14,
        permission15,
        permission16,
        permission17,
        permission18,
        permission19,
        permission20,
        permission24,
    ]
    role2.permission = [
        permissions1,
        permissions2,
        permissions4,
        permissions6,
        permission14,
        permission15,
        permission16,
        permission17,
        permission18,
        permission20,
        permission24,
    ]
    role3.permission = [
        permission19,
        permission20,
        permission24,
    ]
    # role4.permission = [
    #     permission21,
    #     permission22,
    #     permission23,
    #     permission25,
    # ]

    user1 = create_user(
        user_name="admin",
        email="admin@mysite.com",
        password="adminpass",
        rol=1,
        s_user=True,
    )
    user2 = create_user(
        user_name="editor", email="editor@mysite.com", password="editorpass", rol=2
    )
    user3 = create_user(
        user_name="viewer", email="viewer@mysite.com", password="viewerpass", rol=3
    )
    user4 = create_user(
        user_name="supereditor",
        email="seditor@mysite.com",
        password="seditorpass",
        rol=2,
        s_user=True,
    )
    user5 = create_user(
        user_name="normaladmin",
        email="nadmin@mysite.com",
        password="nadminpass",
        rol=1,
    )

    # Crear 25 usuarios adicionales
    for i in range(1, 26):
        create_user(
            user_name=f"user{i}",
            email=f"user{i}@mysite.com",
            password=f"user{i}pass",
            rol=(i % 3) + 1,
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
    board_category4 = board.create_category(
        name="Sitio Natural", description="Sitio natural o parque"
    )
    board_category5 = board.create_category(
        name="Museo", description="Museo o centro cultural"
    )
    board_category6 = board.create_category(
        name="Sitio Religioso", description="Iglesia, catedral o sitio religioso"
    )
    board_category7 = board.create_category(
        name="Sitio Paleontológico",
        description="Sitio con fósiles o restos paleontológicos",
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
    board_tag7 = board.create_tag(name="Colonial")
    board_tag8 = board.create_tag(name="Religioso")
    board_tag9 = board.create_tag(name="Geológico")
    board_tag10 = board.create_tag(name="Paleontológico")
    board_tag11 = board.create_tag(name="Arquitectónico")
    board_tag12 = board.create_tag(name="Parque Nacional")
    board_tag13 = board.create_tag(name="Reserva Natural")
    board_tag14 = board.create_tag(name="Glaciar")
    board_tag15 = board.create_tag(name="Jesuítico")
    board_tag16 = board.create_tag(name="Indígena")
    board_tag17 = board.create_tag(name="Militar")
    board_tag18 = board.create_tag(name="Educativo")
    board_tag19 = board.create_tag(name="Museo")
    board_tag20 = board.create_tag(name="Monumento Nacional")

    site1 = board.create_site(
        name="Cerro de los 7 colores",
        short_description="Cerro multicolor en Purmamarca",
        full_description="El Cerro de los 7 colores es una formación geológica ubicada en Purmamarca, Jujuy, Argentina. Es conocido por sus vibrantes colores que representan diferentes períodos geológicos.",
        city="Purmamarca",
        state=4,
        latitude=-23.2081,
        longitude=-65.4076,
        conservation_state="Bueno",
        category=4,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag2, board_tag5, board_tag9, board_tag16],
    )
    site2 = board.create_site(
        name="La Cueva de las Manos",
        short_description="Cueva con pinturas rupestres",
        full_description="La Cueva de las Manos es un sitio arqueológico ubicado en la provincia de Santa Cruz, Argentina. Es famosa por sus pinturas rupestres que datan de hace más de 9,000 años, incluyendo numerosas representaciones de manos humanas.",
        city="Perito Moreno",
        state=1,
        latitude=-46.5725,
        longitude=-70.0736,
        conservation_state="Regular",
        category=3,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag1, board_tag3, board_tag6, board_tag16, board_tag20],
    )
    site3 = board.create_site(
        name="La Manzana Jesuítica",
        short_description="Conjunto histórico en Córdoba",
        full_description="La Manzana Jesuítica es un conjunto arquitectónico ubicado en la ciudad de Córdoba, Argentina. Fue declarado Patrimonio de la Humanidad por la UNESCO y alberga edificios históricos como la Iglesia de la Compañía de Jesús y la Universidad Nacional de Córdoba.",
        city="Córdoba",
        state=2,
        latitude=-31.4167,
        longitude=-64.1833,
        conservation_state="Malo",
        category=2,
        is_visible=True,
        created_by=user1.id_user,
        tag=[
            board_tag3,
            board_tag4,
            board_tag6,
            board_tag8,
            board_tag11,
            board_tag15,
            board_tag18,
        ],
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
        tag=[board_tag3, board_tag4, board_tag7, board_tag11, board_tag19, board_tag20],
        inauguration_year=1610,
    )

    # 25 sitios adicionales
    site5 = board.create_site(
        name="Catedral de Salta",
        short_description="Catedral histórica de Salta",
        full_description="La Catedral Basílica de Salta es un templo católico ubicado en la ciudad de Salta, Argentina.",
        city="Salta",
        state=17,
        latitude=-24.7859,
        longitude=-65.4117,
        conservation_state="Bueno",
        category=6,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag3, board_tag4, board_tag7, board_tag8, board_tag11],
    )
    site6 = board.create_site(
        name="Glaciar Perito Moreno",
        short_description="Glaciar en Santa Cruz",
        full_description="El glaciar Perito Moreno es una gruesa masa de hielo ubicada en el departamento Lago Argentino de la provincia de Santa Cruz.",
        city="El Calafate",
        state=1,
        latitude=-50.4684,
        longitude=-73.0372,
        conservation_state="Bueno",
        category=4,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag2, board_tag5, board_tag12, board_tag14],
    )
    site7 = board.create_site(
        name="Teatro Colón",
        short_description="Teatro histórico de Buenos Aires",
        full_description="El Teatro Colón es un teatro lírico ubicado en la ciudad de Buenos Aires, Argentina.",
        city="Buenos Aires",
        state=24,
        latitude=-34.6010,
        longitude=-58.3834,
        conservation_state="Bueno",
        category=5,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag3, board_tag4, board_tag5, board_tag11, board_tag19],
        inauguration_year=1908,
    )
    site8 = board.create_site(
        name="Ruinas de San Ignacio",
        short_description="Ruinas jesuíticas en Misiones",
        full_description="Las ruinas de San Ignacio Miní son los restos de una de las reducciones jesuíticas guaraníes.",
        city="San Ignacio",
        state=14,
        latitude=-27.2584,
        longitude=-55.5339,
        conservation_state="Bueno",
        category=3,
        is_visible=True,
        created_by=user1.id_user,
        tag=[
            board_tag1,
            board_tag3,
            board_tag4,
            board_tag6,
            board_tag8,
            board_tag15,
            board_tag20,
        ],
    )
    site9 = board.create_site(
        name="Aconcagua",
        short_description="Montaña más alta de América",
        full_description="El Aconcagua es una montaña ubicada en la provincia de Mendoza, Argentina.",
        city="Mendoza",
        state=13,
        latitude=-32.6532,
        longitude=-70.0109,
        conservation_state="Bueno",
        category=4,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag2, board_tag5, board_tag12],
    )
    site10 = board.create_site(
        name="Casa Rosada",
        short_description="Sede del gobierno argentino",
        full_description="La Casa Rosada es la sede del Poder Ejecutivo de la República Argentina.",
        city="Buenos Aires",
        state=24,
        latitude=-34.6083,
        longitude=-58.3712,
        conservation_state="Bueno",
        category=2,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag3, board_tag4, board_tag5, board_tag11, board_tag17],
        inauguration_year=1898,
    )
    site11 = board.create_site(
        name="Cataratas del Iguazú",
        short_description="Cataratas en Misiones",
        full_description="Las cataratas del Iguazú son un conjunto de cataratas ubicadas sobre el río Iguazú.",
        city="Puerto Iguazú",
        state=14,
        latitude=-25.6953,
        longitude=-54.4367,
        conservation_state="Bueno",
        category=4,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag2, board_tag5, board_tag6, board_tag12, board_tag13],
    )
    site12 = board.create_site(
        name="Pucará de Tilcara",
        short_description="Fortaleza precolombina en Jujuy",
        full_description="El Pucará de Tilcara es una antigua fortaleza construida por los tilcaras.",
        city="Tilcara",
        state=4,
        latitude=-23.5795,
        longitude=-65.3951,
        conservation_state="Bueno",
        category=3,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag1, board_tag3, board_tag4, board_tag16, board_tag17],
    )
    site13 = board.create_site(
        name="Monumento a la Bandera",
        short_description="Monumento en Rosario",
        full_description="El Monumento Nacional a la Bandera se encuentra en la ciudad de Rosario, Santa Fe.",
        city="Rosario",
        state=20,
        latitude=-32.9468,
        longitude=-60.6393,
        conservation_state="Bueno",
        category=1,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag3, board_tag4, board_tag5, board_tag20],
        inauguration_year=1957,
    )
    site14 = board.create_site(
        name="Península Valdés",
        short_description="Reserva natural en Chubut",
        full_description="Península Valdés es un accidente geográfico en la provincia del Chubut, Argentina.",
        city="Puerto Madryn",
        state=7,
        latitude=-42.5115,
        longitude=-64.0775,
        conservation_state="Bueno",
        category=4,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag2, board_tag5, board_tag6, board_tag13],
    )
    site15 = board.create_site(
        name="Quebrada de Humahuaca",
        short_description="Valle en Jujuy",
        full_description="La Quebrada de Humahuaca es un valle andino ubicado en la provincia de Jujuy.",
        city="Humahuaca",
        state=4,
        latitude=-23.2051,
        longitude=-65.3516,
        conservation_state="Bueno",
        category=4,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag1, board_tag2, board_tag3, board_tag6, board_tag9, board_tag16],
    )
    site16 = board.create_site(
        name="Ushuaia",
        short_description="Ciudad del fin del mundo",
        full_description="Ushuaia es una ciudad argentina, capital de la provincia de Tierra del Fuego.",
        city="Ushuaia",
        state=22,
        latitude=-54.8019,
        longitude=-68.3030,
        conservation_state="Bueno",
        category=4,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag2, board_tag5],
    )
    site17 = board.create_site(
        name="Parque Nacional Los Glaciares",
        short_description="Parque nacional en Santa Cruz",
        full_description="El Parque Nacional Los Glaciares es un parque nacional argentino ubicado en Santa Cruz.",
        city="El Calafate",
        state=1,
        latitude=-49.2734,
        longitude=-73.0478,
        conservation_state="Bueno",
        category=4,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag2, board_tag5, board_tag6, board_tag12, board_tag14],
    )
    site18 = board.create_site(
        name="Esteros del Iberá",
        short_description="Humedales en Corrientes",
        full_description="Los Esteros del Iberá son una red de humedales ubicada en la provincia de Corrientes.",
        city="Mercedes",
        state=8,
        latitude=-28.4595,
        longitude=-58.0758,
        conservation_state="Bueno",
        category=3,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag2, board_tag5, board_tag13],
    )
    site19 = board.create_site(
        name="Parque Nacional Talampaya",
        short_description="Parque nacional en La Rioja",
        full_description="El Parque Nacional Talampaya se encuentra en La Rioja, Argentina.",
        city="Villa Unión",
        state=12,
        latitude=-29.8333,
        longitude=-67.8833,
        conservation_state="Bueno",
        category=3,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag1, board_tag2, board_tag6, board_tag9, board_tag10, board_tag12],
    )
    site20 = board.create_site(
        name="Bariloche",
        short_description="Ciudad turística en Río Negro",
        full_description="San Carlos de Bariloche es una ciudad ubicada en la provincia de Río Negro.",
        city="Bariloche",
        state=16,
        latitude=-41.1335,
        longitude=-71.3103,
        conservation_state="Bueno",
        category=3,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag2, board_tag5, board_tag12],
    )
    site21 = board.create_site(
        name="Parque Nacional Ischigualasto",
        short_description="Valle de la Luna en San Juan",
        full_description="El Parque Nacional Ischigualasto se encuentra en la provincia de San Juan.",
        city="San Agustín de Valle Fértil",
        state=18,
        latitude=-30.1000,
        longitude=-67.9167,
        conservation_state="Bueno",
        category=3,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag1, board_tag2, board_tag6, board_tag9, board_tag10, board_tag12],
    )
    site22 = board.create_site(
        name="Caminito",
        short_description="Calle museo en Buenos Aires",
        full_description="Caminito es una calle museo y un pasaje tradicional del barrio de La Boca.",
        city="Buenos Aires",
        state=24,
        latitude=-34.6398,
        longitude=-58.3634,
        conservation_state="Bueno",
        category=2,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag3, board_tag4, board_tag5, board_tag19],
    )
    site23 = board.create_site(
        name="Parque Nacional Los Cardones",
        short_description="Parque nacional en Salta",
        full_description="El Parque Nacional Los Cardones se encuentra en la provincia de Salta.",
        city="Cachi",
        state=17,
        latitude=-25.1167,
        longitude=-66.1667,
        conservation_state="Bueno",
        category=3,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag2, board_tag5, board_tag12],
    )
    site24 = board.create_site(
        name="Termas de Río Hondo",
        short_description="Termas en Santiago del Estero",
        full_description="Las Termas de Río Hondo se encuentran en Santiago del Estero.",
        city="Termas de Río Hondo",
        state=21,
        latitude=-27.4967,
        longitude=-64.8597,
        conservation_state="Bueno",
        category=3,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag2, board_tag5, board_tag13],
    )
    site25 = board.create_site(
        name="Parque Nacional El Palmar",
        short_description="Parque nacional en Entre Ríos",
        full_description="El Parque Nacional El Palmar se encuentra en la provincia de Entre Ríos.",
        city="Colón",
        state=9,
        latitude=-31.8833,
        longitude=-58.2500,
        conservation_state="Bueno",
        category=3,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag2, board_tag5, board_tag12],
    )
    site26 = board.create_site(
        name="Parque Nacional Calilegua",
        short_description="Parque nacional en Jujuy",
        full_description="El Parque Nacional Calilegua se encuentra en la provincia de Jujuy.",
        city="Libertador General San Martín",
        state=4,
        latitude=-23.7833,
        longitude=-64.7667,
        conservation_state="Bueno",
        category=3,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag2, board_tag5, board_tag12],
    )
    site27 = board.create_site(
        name="Parque Nacional Lanín",
        short_description="Parque nacional en Neuquén",
        full_description="El Parque Nacional Lanín se encuentra en la provincia del Neuquén.",
        city="San Martín de los Andes",
        state=15,
        latitude=-40.1500,
        longitude=-71.3000,
        conservation_state="Bueno",
        category=3,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag2, board_tag5, board_tag12],
    )
    site28 = board.create_site(
        name="Parque Nacional Chaco",
        short_description="Parque nacional en Chaco",
        full_description="El Parque Nacional Chaco se encuentra en la provincia del Chaco.",
        city="Capitán Solari",
        state=6,
        latitude=-26.8000,
        longitude=-59.6167,
        conservation_state="Bueno",
        category=3,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag2, board_tag5, board_tag12],
    )
    site29 = board.create_site(
        name="Parque Nacional Lihué Calel",
        short_description="Parque nacional en La Pampa",
        full_description="El Parque Nacional Lihué Calel se encuentra en la provincia de La Pampa.",
        city="Puelches",
        state=11,
        latitude=-37.9667,
        longitude=-65.5833,
        conservation_state="Bueno",
        category=3,
        is_visible=True,
        created_by=user1.id_user,
        tag=[board_tag2, board_tag5, board_tag12],
    )
 
   

    # Crear imágenes para los sitios con rutas reales de MinIO
    site_images = [
    SiteImage(
        site_id=site1.id_site,
        image_path="public/sites/1/da8d038a-0cee-45f8-a293-abd0951149f5.jpg",
        title="Cerro de los 7 colores",
        description="Imagen del Cerro de los 7 colores",
        display_order=1,
        is_thumbnail=True,
    ),
    SiteImage(
        site_id=site2.id_site,
        image_path="public/sites/2/1d02d758-7ac9-47c9-9c91-7066a44f7cc1.jpg",
        title="La Cueva de las Manos",
        description="Imagen de La Cueva de las Manos",
        display_order=1,
        is_thumbnail=True,
    ),
    SiteImage(
        site_id=site3.id_site,
        image_path="public/sites/3/6b9fd85a-aa11-4f75-9d30-dd6d0a643996.jpg",
        title="La Manzana Jesuítica",
        description="Imagen de La Manzana Jesuítica",
        display_order=1,
        is_thumbnail=True,
    ),
    SiteImage(
        site_id=site4.id_site,
        image_path="public/sites/4/918ed3e6-e111-40a9-8298-61f321530e2b.jpg",
        title="Cabildo de Buenos Aires",
        description="Imagen del Cabildo de Buenos Aires",
        display_order=1,
        is_thumbnail=True,
    ),
    SiteImage(
        site_id=site5.id_site,
        image_path="public/sites/5/241e7979-14fb-410b-90e4-821cee6ea492.jpg",
        title="Catedral de Salta",
        description="Imagen de la Catedral de Salta",
        display_order=1,
        is_thumbnail=True,
    ),
    SiteImage(
        site_id=site6.id_site,
        image_path="public/sites/6/e8eb9dcd-0f6d-490c-85dc-8a44d8b55a4d.jpeg",
        title="Glaciar Perito Moreno",
        description="Imagen del Glaciar Perito Moreno",
        display_order=1,
        is_thumbnail=True,
    ),
    SiteImage(
        site_id=site9.id_site,
        image_path="public/sites/9/f5ec8d77-429a-4053-b556-a0ed8b8d1379.jpeg",
        title="Aconcagua",
        description="Imagen del Aconcagua",
        display_order=1,
        is_thumbnail=True,
    ),
    SiteImage(
        site_id=site10.id_site,
        image_path="public/sites/10/80624add-3ad0-484a-a9a2-aa9564ef39ff.jpeg",
        title="Casa Rosada",
        description="Imagen de la Casa Rosada",
        display_order=1,
        is_thumbnail=True,
    ),
    SiteImage(
        site_id=site11.id_site,
        image_path="public/sites/11/a87c4b33-ea7c-4963-9eeb-3412598a8d78.jpeg",
        title="Cataratas del Iguazú",
        description="Imagen de las Cataratas del Iguazú",
        display_order=1,
        is_thumbnail=True,
    ),
    SiteImage(
        site_id=site13.id_site,
        image_path="public/sites/13/1b687aa7-11cd-46cd-8906-ab3422a7a686.jpeg",
        title="Monumento a la Bandera",
        description="Imagen del Monumento a la Bandera",
        display_order=1,
        is_thumbnail=True,
    ),
    SiteImage(
        site_id=site16.id_site,
        image_path="public/sites/16/738c89b5-7e98-498c-bd2e-fbba42f4b5fa.webp",
        title="Ushuaia",
        description="Imagen de Ushuaia",
        display_order=1,
        is_thumbnail=True,
    ),
    SiteImage(
        site_id=site17.id_site,
        image_path="public/sites/17/f0f119f9-bed2-4a3a-8622-5d04bb045c0c.jpeg",
        title="Parque Nacional Los Glaciares",
        description="Imagen del Parque Nacional Los Glaciares",
        display_order=1,
        is_thumbnail=True,
    ),
    SiteImage(
        site_id=site18.id_site,
        image_path="public/sites/18/4e657abf-a34b-43f4-af7c-108c22b42763.jpeg",
        title="Esteros del Iberá",
        description="Imagen de los Esteros del Iberá",
        display_order=1,
        is_thumbnail=True,
    ),
    SiteImage(
        site_id=site19.id_site,
        image_path="public/sites/19/a836b970-75ea-47c1-8ed6-851ca3cb2ae3.jpeg",
        title="Parque Nacional Talampaya",
        description="Imagen del Parque Nacional Talampaya",
        display_order=1,
        is_thumbnail=True,
    ),
    SiteImage(
        site_id=site20.id_site,
        image_path="public/sites/20/e20fbc16-80fc-437f-9e8b-8833fcb32750.jpg",
        title="Bariloche",
        description="Imagen de Bariloche",
        display_order=1,
        is_thumbnail=True,
    ),
    SiteImage(
        site_id=site21.id_site,
        image_path="public/sites/21/c5c4c6f9-06fc-43bd-b450-8ee3a62fd0d5.jpg",
        title="Parque Nacional Ischigualasto",
        description="Imagen del Parque Nacional Ischigualasto",
        display_order=1,
        is_thumbnail=True,
    ),
    SiteImage(
        site_id=site22.id_site,
        image_path="public/sites/22/34ec6bcd-82a6-4256-a6d5-58bf893679c7.jpg",
        title="Caminito",
        description="Imagen de Caminito",
        display_order=1,
        is_thumbnail=True,
    ),
    SiteImage(
        site_id=site23.id_site,
        image_path="public/sites/23/afb87af5-8d14-4b45-b9e4-ec4d4a4dbb79.jpg",
        title="Parque Nacional Los Cardones",
        description="Imagen del Parque Nacional Los Cardones",
        display_order=1,
        is_thumbnail=True,
    ),
    SiteImage(
        site_id=site25.id_site,
        image_path="public/sites/25/5f66a631-0838-45e8-8a26-3e4bb9b4ee64.jpg",
        title="Parque Nacional El Palmar",
        description="Imagen del Parque Nacional El Palmar",
        display_order=1,
        is_thumbnail=True,
    ),
    SiteImage(
        site_id=site26.id_site,
        image_path="public/sites/26/2ff1c912-626b-440f-9950-332a909f235c.jpg",
        title="Parque Nacional Calilegua",
        description="Imagen del Parque Nacional Calilegua",
        display_order=1,
        is_thumbnail=True,
    ),
    SiteImage(
        site_id=site27.id_site,
        image_path="public/sites/27/d9e99acc-9c81-4cbc-80c8-6849c9626cfa.jpg",
        title="Parque Nacional Lanín",
        description="Imagen del Parque Nacional Lanín",
        display_order=1,
        is_thumbnail=True,
    ),
    SiteImage(
        site_id=site28.id_site,
        image_path="public/sites/28/aa06b73f-e834-4427-834c-478ebdc71e92.jpg",
        title="Parque Nacional Chaco",
        description="Imagen del Parque Nacional Chaco",
        display_order=1,
        is_thumbnail=True,
    ),
    SiteImage(
        site_id=site29.id_site,
        image_path="public/sites/29/728ae69e-1337-481c-a52a-e45764fd7d03.jpg",
        title="Parque Nacional Lihué Calel",
        description="Imagen del Parque Nacional Lihué Calel",
        display_order=1,
        is_thumbnail=True,
    ),
]


    db.session.add_all(site_images)
    db.session.commit()

    flags = [
        FeatureFlag(
            name="admin_maintenance_mode",
            description="Modo mantenimiento de administración",
            enabled=False,
            maintenance_message="El sistema de administración está en mantenimiento.",
            updated_by=user1.id_user,
        ),
        FeatureFlag(
            name="portal_maintenance_mode",
            description="Modo mantenimiento de portal web",
            enabled=False,
            maintenance_message="El portal está en mantenimiento.",
            updated_by=user1.id_user,
        ),
        FeatureFlag(
            name="reviews_enabled",
            description="Permitir nuevas reseñas",
            enabled=True,
            maintenance_message=None,
            updated_by=user1.id_user,
        ),
    ]

    db.session.add_all(flags)
    db.session.commit()

    # Crear reseñas aleatorias
    create_sample_reviews()

    print("✔️  Base de datos rellenada con datos de prueba.")


def create_sample_reviews():
    """Crea reseñas aleatorias para testing"""
    import random
    from datetime import timedelta
    from src.core.entity.review import ReviewStatus

    # Comentarios de ejemplo
    comments = [
        "Excelente lugar histórico, muy bien conservado",
        "Falta mejor señalización en el interior",
        "Hermosa arquitectura colonial",
        "El guía fue muy informativo",
        "Necesita más mantenimiento",
        "Imperdible para los amantes de la historia",
        "Muy interesante pero algo descuidado",
        "Perfecto para visitar en familia",
        "La vista desde aquí es espectacular",
        "Recomiendo visitarlo temprano",
        "Podría tener mejor iluminación",
        "Un tesoro histórico bien preservado",
        "Faltan carteles explicativos",
        "Lugar mágico lleno de historia",
        "Acceso un poco complicado pero vale la pena",
    ]

    # Crear usuario público de prueba si no existe
    public_user = db.session.query(PublicUser).first()
    if not public_user:
        public_user = PublicUser(
            google_id="test_user_123", email="test@example.com", name="Usuario Test"
        )
        db.session.add(public_user)
        db.session.commit()

    # Obtener sitios visibles
    sites = (
        db.session.query(board.Site)
        .filter(board.Site.is_visible, ~board.Site.deleted)
        .all()
    )

    # Crear reseñas para algunos sitios (70%)
    sites_with_reviews = random.sample(sites, min(len(sites), int(len(sites) * 0.7)))

    for site in sites_with_reviews:
        # 1-6 reseñas por sitio
        num_reviews = random.randint(1, 6)

        for _ in range(num_reviews):
            # Rating aleatorio (1-5)
            rating = random.randint(1, 5)

            # Comentario aleatorio
            comment = random.choice(comments)

            # Estado con probabilidades realistas
            status_choice = random.choices(
                [ReviewStatus.APROBADA, ReviewStatus.PENDIENTE, ReviewStatus.RECHAZADA],
                weights=[
                    0.6,
                    0.3,
                    0.1,
                ],  # 60% aprobadas, 30% pendientes, 10% rechazadas
            )[0]

            # Fechas aleatorias en los últimos 6 meses
            from datetime import datetime, timezone

            days_ago = random.randint(1, 180)
            created_date = datetime.now(timezone.utc) - timedelta(days=days_ago)
            updated_date = created_date + timedelta(hours=random.randint(0, 48))

            # Fecha de moderación solo si está aprobada o rechazada
            moderated_date = None
            if status_choice in [ReviewStatus.APROBADA, ReviewStatus.RECHAZADA]:
                moderated_date = created_date + timedelta(days=random.randint(1, 7))

            # Crear reseña
            review = Review(
                id_site=site.id_site,
                id_public_user=public_user.id_public_user,
                rating=rating,
                content=comment,
                status=status_choice,
                date_created=created_date,
                updated_at=updated_date,
                date_moderated=moderated_date,
                moderated_by=1 if moderated_date else None,
            )

            db.session.add(review)

    db.session.commit()
    print("✔️  Reseñas de prueba creadas exitosamente")
