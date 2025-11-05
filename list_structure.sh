#!/usr/bin/env bash
# listar_estructura.sh
# Lista todos los archivos y carpetas desde el directorio actual hacia abajo
# y guarda la estructura en un archivo estructura.txt

OUTFILE="estructura.txt"

echo "Generando estructura de: $(pwd)" > "$OUTFILE"
echo "Fecha: $(date)" >> "$OUTFILE"
echo "----------------------------------------" >> "$OUTFILE"
echo "" >> "$OUTFILE"

# Función recursiva para listar con indentación
listar() {
    local dir="$1"
    local prefix="$2"

    # Listar directorios primero, luego archivos
    for item in "$dir"/*; do
        # si no existe (por ejemplo, si no hay nada en la carpeta), saltar
        [ -e "$item" ] || continue

        local name="$(basename "$item")"

        if [ -d "$item" ]; then
            echo "${prefix}📁 $name/" >> "$OUTFILE"
            listar "$item" "    $prefix"
        else
            echo "${prefix}📄 $name" >> "$OUTFILE"
        fi
    done
}

listar "." ""

echo "" >> "$OUTFILE"
echo "Hecho. Archivo generado: $(pwd)/$OUTFILE"
