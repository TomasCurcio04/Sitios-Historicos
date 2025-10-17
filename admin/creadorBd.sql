CREATE SCHEMA IF NOT EXISTS nico AUTHORIZATION current_user;
SET search_path TO nico;
-- SCHEMA
COMMENT ON SCHEMA nico IS '';


-- SEQUENCES
CREATE SEQUENCE nico.category_id_category_seq START 1 INCREMENT 1;
CREATE SEQUENCE nico.feature_flag_id_seq START 1 INCREMENT 1;
CREATE SEQUENCE nico.permission_id_permission_seq START 1 INCREMENT 1;
CREATE SEQUENCE nico.role_id_role_seq START 1 INCREMENT 1;
CREATE SEQUENCE nico.site_id_site_seq START 1 INCREMENT 1;
CREATE SEQUENCE nico.site_history_id_site_history_seq START 1 INCREMENT 1;
CREATE SEQUENCE nico.state_id_state_seq START 1 INCREMENT 1;
CREATE SEQUENCE nico.tag_id_tag_seq START 1 INCREMENT 1;
CREATE SEQUENCE nico.users_id_user_seq START 1 INCREMENT 1;

-- TABLES
CREATE TABLE nico.category (
  id_category integer PRIMARY KEY DEFAULT nextval('nico.category_id_category_seq'),
  name varchar(50) NOT NULL,
  description varchar(255) NOT NULL
);

CREATE TABLE nico.role (
  id_role integer PRIMARY KEY DEFAULT nextval('nico.role_id_role_seq'),
  name varchar(50) NOT NULL,
  description varchar(255) NOT NULL
);

CREATE TABLE nico.users (
  id_user integer PRIMARY KEY DEFAULT nextval('nico.users_id_user_seq'),
  user_name varchar(50) NOT NULL,
  email varchar(50) UNIQUE NOT NULL,
  password varchar(100) NOT NULL,
  role integer NOT NULL REFERENCES nico.role(id_role),
  active boolean NOT NULL,
  s_user boolean NOT NULL,
  date_create timestamp NOT NULL,
  modify timestamp NOT NULL
);

CREATE TABLE nico.feature_flag (
  id integer PRIMARY KEY DEFAULT nextval('nico.feature_flag_id_seq'),
  name varchar(50) UNIQUE NOT NULL,
  description varchar(255) NOT NULL,
  enabled boolean NOT NULL,
  maintenance_message varchar(255),
  updated_at timestamp NOT NULL,
  updated_by integer NOT NULL REFERENCES nico.users(id_user)
);

CREATE TABLE nico.permission (
  id_permission integer PRIMARY KEY DEFAULT nextval('nico.permission_id_permission_seq'),
  permission_name varchar(50) NOT NULL,
  permission_description varchar(255) NOT NULL
);

CREATE TABLE nico.permission_list (
  id_permission integer NOT NULL REFERENCES nico.permission(id_permission),
  id_role integer NOT NULL REFERENCES nico.role(id_role)
);

CREATE TABLE nico.state (
  id_state integer PRIMARY KEY DEFAULT nextval('nico.state_id_state_seq'),
  name varchar(50) NOT NULL
);

CREATE TABLE nico.tag (
  id_tag integer PRIMARY KEY DEFAULT nextval('nico.tag_id_tag_seq'),
  name varchar(50) UNIQUE NOT NULL,
  slug varchar(50) UNIQUE NOT NULL,
  date_created timestamp NOT NULL
);

CREATE TABLE nico.site (
  id_site integer PRIMARY KEY DEFAULT nextval('nico.site_id_site_seq'),
  name varchar(150) NOT NULL,
  short_description varchar(120) NOT NULL,
  full_description text NOT NULL,
  city varchar(50) NOT NULL,
  state integer NOT NULL REFERENCES nico.state(id_state),
  latitude numeric(9,6) NOT NULL,
  longitude numeric(9,6) NOT NULL,
  conservation_state varchar(20),
  inauguration_year integer,
  category integer NOT NULL REFERENCES nico.category(id_category),
  date_registered timestamp NOT NULL,
  is_visible boolean NOT NULL,
  created_by integer NOT NULL REFERENCES nico.users(id_user)
);

CREATE TABLE nico.site_tag (
  id_site integer NOT NULL REFERENCES nico.site(id_site),
  id_tag integer NOT NULL REFERENCES nico.tag(id_tag)
);

CREATE TABLE nico.site_history (
  id_site_history integer PRIMARY KEY DEFAULT nextval('nico.site_history_id_site_history_seq'),
  id_site integer NOT NULL REFERENCES nico.site(id_site),
  id_user integer NOT NULL REFERENCES nico.users(id_user),
  action_type varchar(50) NOT NULL,
  action_detail text NOT NULL,
  date_action timestamp NOT NULL
);

-- CATEGORY
INSERT INTO nico.category (id_category, name, description) VALUES
(1, 'Monumento', 'Monumento histórico'),
(2, 'Edificio Histórico', 'Edificio histórico'),
(3, 'Sitio Arqueológico', 'Sitio arqueológico');

-- FEATURE_FLAG
INSERT INTO nico.feature_flag (id, name, description, enabled, maintenance_message, updated_at, updated_by) VALUES
(2, 'portal_maintenance_mode', 'Modo mantenimiento de portal web', false, 'El portal está en mantenimiento.', '2025-10-08 04:19:52.796765', 1),
(3, 'reviews_enabled', 'Permitir nuevas reseñas', true, NULL, '2025-10-08 04:19:52.796765', 1),
(1, 'admin_maintenance_mode', 'Modo mantenimiento de administración', true, 'El sistema de administración está en mantenimiento.', '2025-10-08 04:19:52.796765', 1);

-- PERMISSION
INSERT INTO nico.permission (id_permission, permission_name, permission_description) VALUES
(1, 'view_site', 'Ver el Sitio'),
(2, 'edit_site', 'Editar el Sitio'),
(3, 'delete_site', 'Eliminar el Sitio'),
(4, 'create_site', 'Crear el Sitio');

-- PERMISSION_LIST
INSERT INTO nico.permission_list (id_permission, id_role) VALUES
(1, 1), (2, 1), (3, 1), (4, 1),
(1, 2), (2, 2), (4, 2),
(1, 3);

-- ROLE
INSERT INTO nico.role (id_role, name, description) VALUES
(1, 'admin', 'Administrador'),
(2, 'editor', 'Editor'),
(3, 'viewer', 'Visualizador');

-- SITE
INSERT INTO nico.site (id_site, name, short_description, full_description, city, state, latitude, longitude, conservation_state, inauguration_year, category, date_registered, is_visible, created_by) VALUES
(1, 'Cerro de los 7 colores', 'Cerro multicolor en Purmamarca', 'El Cerro de los 7 colores es una formación geológica ubicada en Purmamarca, Jujuy, Argentina. Es conocido por sus vibrantes colores que representan diferentes períodos geológicos.', 'Purmamarca', 4, -23.208100, -65.407600, 'Bueno', NULL, 3, '2025-10-08 04:19:47.338341', true, 1),
(2, 'La Cueva de las Manos', 'Cueva con pinturas rupestres', 'La Cueva de las Manos es un sitio arqueológico ubicado en la provincia de Santa Cruz, Argentina. Es famosa por sus pinturas rupestres que datan de hace más de 9,000 años, incluyendo numerosas representaciones de manos humanas.', 'Perito Moreno', 1, -46.572500, -70.073600, 'Excelente', NULL, 3, '2025-10-08 04:19:48.594798', true, 1),
(3, 'La Manzana Jesuítica', 'Conjunto histórico en Córdoba', 'La Manzana Jesuítica es un conjunto arquitectónico ubicado en la ciudad de Córdoba, Argentina. Fue declarado Patrimonio de la Humanidad por la UNESCO y alberga edificios históricos como la Iglesia de la Compañía de Jesús y la Universidad Nacional de Córdoba.', 'Córdoba', 2, -31.416700, -64.183300, 'Muy Bueno', NULL, 2, '2025-10-08 04:19:50.072925', true, 1),
(4, 'Cabildo de Buenos Aires', 'Edificio histórico en Buenos Aires', 'El Cabildo de Buenos Aires es un edificio histórico ubicado en la Plaza de Mayo, en el centro de Buenos Aires, Argentina. Fue la sede del gobierno colonial español y desempeñó un papel crucial en la historia del país, especialmente durante la Revolución de Mayo de 1810.', 'Buenos Aires', 3, -34.608300, -58.370800, 'Bueno', 1610, 2, '2025-10-08 04:19:51.468888', true, 1);

-- SITE_TAG
INSERT INTO nico.site_tag (id_site, id_tag) VALUES
(1, 2), (1, 5), (1, 6),
(2, 1), (2, 3), (2, 6),
(3, 1), (3, 3), (3, 4), (3, 6),
(4, 1), (4, 3), (4, 4), (4, 6),
(1, 2), (1, 5), (1, 6),
(2, 1), (2, 3), (2, 6);

-- STATE
INSERT INTO nico.state (id_state, name) VALUES
(1, 'Santa Cruz'),
(2, 'Córdoba'),
(3, 'Buenos Aires'),
(4, 'Jujuy');

-- TAG
INSERT INTO nico.tag (id_tag, name, slug, date_created) VALUES
(1, 'Arqueológico', 'arqueologico', '2025-10-08 04:19:44.132773'),
(2, 'Natural', 'natural', '2025-10-08 04:19:44.670843'),
(3, 'Cultural', 'cultural', '2025-10-08 04:19:45.110009'),
(4, 'Histórico', 'historico', '2025-10-08 04:19:45.644523'),
(5, 'Turístico', 'turistico', '2025-10-08 04:19:46.156309'),
(6, 'Patrimonio de la Humanidad', 'patrimonio-humanidad', '2025-10-08 04:19:46.602950');

-- USERS
INSERT INTO nico.users (id_user, user_name, email, password, role, active, s_user, date_create, modify) VALUES
(1, 'admin', 'admin@mysite.com', 'adminpass', 1, true, true, '2025-10-08 04:19:39.551501', '2025-10-08 04:19:39.551501'),
(2, 'editor', 'editor@mysite.com', 'editorpass', 2, true, false, '2025-10-08 04:19:39.904866', '2025-10-08 04:19:39.904866'),
(3, 'viewer', 'viewer@mysite.com', 'viewerpass', 3, true, false, '2025-10-08 04:19:40.338428', '2025-10-08 04:19:40.338428');
