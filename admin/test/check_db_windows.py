# test/check_db_windows_summary.py
from sqlalchemy import inspect
from app import create_app  # Ajustá la ruta si tu app.py está en otro lugar
from src.core.database import db

# Configuración de tablas y columnas esperadas
EXPECTED_TABLES = {
    "site": ["id", "category_id", "state_id", "user_id"],
    "category": ["id"],
    "state": ["id"],
    "tag": ["id"],
    "site_history": ["id", "site_id", "user_id", "date_change"],
    "users": ["id_user", "user_name", "email", "password", "role"],
    "permission_list": ["id_permission", "id_role"],
    "site_tag": ["site_id", "tag_id"],
    "role": ["id_role", "name", "description"],
    "permission": ["id_permission", "name"],
    "feature_flag": ["id", "name", "enabled", "updated_by"]
}

# Claves foráneas esperadas (tabla -> columna -> referencia)
EXPECTED_FK = {
    "site": {
        "category_id": "category.id",
        "state_id": "state.id",
        "user_id": "users.id_user"
    },
    "site_history": {
        "site_id": "site.id",
        "user_id": "users.id_user"
    },
    "site_tag": {
        "site_id": "site.id",
        "tag_id": "tag.id"
    }
}

def main():
    app = create_app("development")

    missing_tables = []
    missing_columns = {}
    missing_fks = {}

    with app.app_context():
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        print("=== VERIFICACIÓN DE LA BASE DE DATOS ===\n")

        for table_name, columns in EXPECTED_TABLES.items():
            if table_name in existing_tables:
                print(f"Tabla '{table_name}': Existe")
                table_columns = [col["name"] for col in inspector.get_columns(table_name)]
                
                for col in columns:
                    if col not in table_columns:
                        missing_columns.setdefault(table_name, []).append(col)
                
                # Revisar FK
                fks = inspector.get_foreign_keys(table_name)
                fk_map = {fk["constrained_columns"][0]: fk["referred_table"] + "." + fk["referred_columns"][0] for fk in fks}
                if table_name in EXPECTED_FK:
                    for col, ref in EXPECTED_FK[table_name].items():
                        if col not in fk_map or fk_map[col] != ref:
                            missing_fks.setdefault(table_name, {})[col] = ref
            else:
                missing_tables.append(table_name)

        # Resumen final
        print("\n=== RESUMEN DE LA VERIFICACIÓN ===\n")
        if missing_tables:
            print("Tablas faltantes:")
            for t in missing_tables:
                print(f"  - {t}")
        else:
            print("Todas las tablas esperadas existen.")

        if missing_columns:
            print("\nColumnas faltantes por tabla:")
            for t, cols in missing_columns.items():
                print(f"  {t}: {', '.join(cols)}")
        else:
            print("\nNo faltan columnas en las tablas existentes.")

        if missing_fks:
            print("\nClaves foráneas faltantes o incorrectas:")
            for t, fks in missing_fks.items():
                for col, ref in fks.items():
                    print(f"  {t}.{col} -> {ref}")
        else:
            print("\nTodas las claves foráneas esperadas están presentes.")

        print("\n=== FIN DE VERIFICACIÓN ===")

if __name__ == "__main__":
    main()
