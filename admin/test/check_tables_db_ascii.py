"""Verificación completa de la base de datos incluyendo relaciones many-to-many."""

from src.core.database import db
from sqlalchemy import inspect
from app import create_app

def main():
    app = create_app("development")

    # Inicializar db si no está inicializado
    if not hasattr(app, "extensions") or "sqlalchemy" not in app.extensions:
        db.init_app(app)

    # Tablas principales y columnas esperadas
    expected_tables = {
        "site": [
            {"name": "id", "type": "INTEGER", "nullable": False},
            {"name": "name", "type": "VARCHAR", "nullable": False},
            {"name": "category_id", "type": "INTEGER", "nullable": False},
            {"name": "state_id", "type": "INTEGER", "nullable": False},
            {"name": "user_id", "type": "INTEGER", "nullable": False},
        ],
        "category": [
            {"name": "id", "type": "INTEGER", "nullable": False},
            {"name": "name", "type": "VARCHAR", "nullable": False},
        ],
        "state": [
            {"name": "id", "type": "INTEGER", "nullable": False},
            {"name": "name", "type": "VARCHAR", "nullable": False},
        ],
        "tag": [
            {"name": "id", "type": "INTEGER", "nullable": False},
            {"name": "name", "type": "VARCHAR", "nullable": False},
        ],
        "site_history": [
            {"name": "id", "type": "INTEGER", "nullable": False},
            {"name": "site_id", "type": "INTEGER", "nullable": False},
            {"name": "user_id", "type": "INTEGER", "nullable": False},
            {"name": "date_change", "type": "DATETIME", "nullable": False},
        ],
        "users": [
            {"name": "id_user", "type": "INTEGER", "nullable": False},
            {"name": "user_name", "type": "VARCHAR", "nullable": False},
            {"name": "email", "type": "VARCHAR", "nullable": False},
            {"name": "password", "type": "VARCHAR", "nullable": False},
            {"name": "role", "type": "INTEGER", "nullable": False},
        ],
        # Tablas intermedias many-to-many
        "permission_list": [
            {"name": "id_permission", "type": "INTEGER", "nullable": False},
            {"name": "id_role", "type": "INTEGER", "nullable": False},
        ],
        "site_tag": [
            {"name": "site_id", "type": "INTEGER", "nullable": False},
            {"name": "tag_id", "type": "INTEGER", "nullable": False},
        ]
    }

    expected_fks = {
        "site": {"category_id": "category.id", "state_id": "state.id", "user_id": "users.id_user"},
        "site_history": {"site_id": "site.id", "user_id": "users.id_user"},
        "users": {"role": "role.id_role"},
        "permission_list": {"id_permission": "permission.id_permission", "id_role": "role.id_role"},
        "site_tag": {"site_id": "site.id", "tag_id": "tag.id"},
    }

    with app.app_context():
        inspector = inspect(db.engine)
        print("\n=== VERIFICACIÓN COMPLETA DE LA BASE DE DATOS (M2M) ===\n")

        for table_name, columns in expected_tables.items():
            if table_name in inspector.get_table_names():
                print(f"Tabla '{table_name}': [OK] Existe")
                actual_cols_info = {col['name']: col for col in inspector.get_columns(table_name)}

                for col in columns:
                    col_name = col['name']
                    if col_name not in actual_cols_info:
                        print(f"  [NO] Falta columna '{col_name}'")
                        continue

                    actual = actual_cols_info[col_name]
                    expected_type = col['type'].upper()
                    actual_type = str(actual['type']).upper()
                    if expected_type not in actual_type:
                        print(f"  [WARN] Columna '{col_name}': tipo esperado '{expected_type}', encontrado '{actual_type}'")

                    if col['nullable'] != actual['nullable']:
                        print(f"  [WARN] Columna '{col_name}': nullable esperado '{col['nullable']}', encontrado '{actual['nullable']}'")

                # Revisar claves foráneas
                if table_name in expected_fks:
                    actual_fks = {fk["constrained_columns"][0]: fk["referred_table"] + "." + fk["referred_columns"][0]
                                  for fk in inspector.get_foreign_keys(table_name)}
                    for col, ref in expected_fks[table_name].items():
                        if col not in actual_fks:
                            print(f"  [NO] Falta FK en columna '{col}' apuntando a '{ref}'")
                        elif actual_fks[col] != ref:
                            print(f"  [WARN] FK en columna '{col}' apunta a '{actual_fks[col]}' y debería ser '{ref}'")
            else:
                print(f"Tabla '{table_name}': [NO] NO EXISTE")

        print("\n=== FIN DE VERIFICACIÓN COMPLETA (M2M) ===\n")

if __name__ == "__main__":
    main()