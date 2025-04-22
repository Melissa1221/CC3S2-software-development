#!/bin/bash
# ================================================================
# Script avanzado para administrar funcionalidades de Git
# ================================================================
# Este script ofrece un menú interactivo que permite:
# 1) Listar el reflog y restaurar un commit.
# 2) Agregar un submódulo.
# 3) Agregar un subtree.
# 4) Gestión de ramas (listar, crear, cambiar y borrar ramas).
# 5) Gestión de stashes (listar, crear, aplicar y borrar stashes).
# 6) Mostrar estado del repositorio y últimos commits.
# 7) Gestión de tags (listar, crear y borrar tags).
# 8) Gestión de git bisect (iniciar proceso interactivo).
# 9) Gestión de git diff (ver diferencias entre revisiones o ramas).
# 10) Gestión de Hooks (listar, crear, editar y borrar hooks).
# 11) Generar reporte de estado del repositorio.
# 12) Merge automatizado de una rama.
# 13) Salir.
#
# Requisitos: Se debe ejecutar dentro de un repositorio Git.
#
# Cómo ejecutar el script:
#   1. Guardar el archivo (por ejemplo: git_avanzado.sh).
#   2. Otorgar permisos de ejecución:
#         chmod +x git_avanzado.sh
#   3. Ejecutarlo dentro de un repositorio Git:
#         ./git_avanzado.sh
# ================================================================

# Funciones principales

# Función para mostrar el menú principal
function mostrar_menu_principal() {
    echo ""
    echo "====== Menú avanzado de Git ======"
    echo "1) Listar reflog y restaurar un commit"
    echo "2) Agregar un submódulo"
    echo "3) Agregar un subtree"
    echo "4) Gestión de ramas"
    echo "5) Gestión de stashes"
    echo "6) Mostrar estado y últimos commits"
    echo "7) Gestión de tags"
    echo "8) Gestión de git bisect"
    echo "9) Gestión de git diff"
    echo "10) Gestión de Hooks"
    echo "11) Generar reporte de estado del repositorio"
    echo "12) Merge automatizado de una rama"
    echo "13) Salir"
    echo -n "Seleccione una opción: "
}

# 1. Reflog y restauración de commit
function restaurar_commit() {
    echo ""
    echo "=== Listado de reflog ==="
    git reflog --date=iso | head -n 10
    echo ""
    echo -n "Ingrese la referencia (ej: HEAD@{1} o hash) que desea restaurar: "
    read ref
    echo -n "¿Desea restaurar a '$ref'? (s/n): "
    read confirmacion
    if [[ "$confirmacion" =~ ^[sS] ]]; then
        git reset --hard "$ref"
        echo "Repositorio restaurado a: $ref"
    else
        echo "Operación cancelada."
    fi
}

# 2. Agregar un submódulo
function agregar_submodulo() {
    echo ""
    echo -n "Ingrese la URL del repositorio para el submódulo: "
    read url_submodulo
    echo -n "Ingrese el directorio donde se ubicará el submódulo: "
    read directorio
    git submodule add "$url_submodulo" "$directorio"
    git submodule update --init --recursive
    echo "Submódulo agregado en: $directorio"
}

# 3. Agregar un subtree
function agregar_subtree() {
    echo ""
    echo -n "Ingrese la URL del repositorio para el subtree: "
    read url_subtree
    echo -n "Ingrese el directorio donde se integrará el subtree: "
    read directorio
    echo -n "Ingrese la rama del repositorio externo (por defecto master): "
    read rama
    rama=${rama:-master}
    git subtree add --prefix="$directorio" "$url_subtree" "$rama" --squash
    echo "Subtree agregado en: $directorio"
}

# 4. Gestión de ramas
function gestionar_ramas() {
    while true; do
        echo ""
        echo "=== Gestión de ramas ==="
        echo "a) Listar ramas"
        echo "b) Crear nueva rama y cambiar a ella"
        echo "c) Cambiar a una rama existente"
        echo "d) Borrar una rama"
        echo "e) Renombrar una rama"
        echo "f) Volver al menú principal"
        echo -n "Seleccione una opción: "
        read opcion_rama
        case "$opcion_rama" in
            a|A)
                echo ""
                echo "Ramas existentes:"
                git branch
                ;;
            b|B)
                echo -n "Ingrese el nombre de la nueva rama: "
                read nueva_rama
                git checkout -b "$nueva_rama"
                echo "Rama '$nueva_rama' creada y activada."
                ;;
            c|C)
                echo -n "Ingrese el nombre de la rama a la que desea cambiar: "
                read rama
                git checkout "$rama"
                ;;
            d|D)
                echo -n "Ingrese el nombre de la rama a borrar: "
                read rama
                git branch -d "$rama"
                echo "Rama '$rama' borrada."
                ;;
            e|E)
                echo -n "Ingrese el nombre de la rama actual: "
                read rama_actual
                echo -n "Ingrese el nuevo nombre para la rama: "
                read nuevo_nombre
                current_branch=$(git rev-parse --abbrev-ref HEAD)
                if [[ "$rama_actual" == "$current_branch" ]]; then
                    git branch -m "$nuevo_nombre"
                    echo "Rama '$rama_actual' renombrada a '$nuevo_nombre' (era la rama actual)."
                else
                    git branch -m "$rama_actual" "$nuevo_nombre"
                    echo "Rama '$rama_actual' renombrada a '$nuevo_nombre'."
                fi
                ;;
            f|F)
                break
                ;;
            *)
                echo "Opción no válida, intente de nuevo."
                ;;
        esac
    done
}

# 5. Gestión de stashes
function gestionar_stash() {
    while true; do
        echo ""
        echo "=== Gestión de stash ==="
        echo "a) Listar stashes"
        echo "b) Crear un stash"
        echo "c) Aplicar un stash"
        echo "d) Borrar un stash"
        echo "e) Volver al menú principal"
        echo -n "Seleccione una opción: "
        read opcion_stash
        case "$opcion_stash" in
            a|A)
                echo ""
                git stash list
                ;;
            b|B)
                echo -n "Ingrese un mensaje para el stash (opcional): "
                read mensaje
                git stash push -m "$mensaje"
                echo "Stash creado."
                ;;
            c|C)
                echo -n "Ingrese el identificador del stash a aplicar (ej: stash@{0}): "
                read idstash
                git stash apply "$idstash"
                echo "Stash $idstash aplicado."
                ;;
            d|D)
                echo -n "Ingrese el identificador del stash a borrar (ej: stash@{0}): "
                read idstash
                git stash drop "$idstash"
                echo "Stash $idstash borrado."
                ;;
            e|E)
                break
                ;;
            *)
                echo "Opción no válida, intente de nuevo."
                ;;
        esac
    done
}

# 6. Mostrar estado y últimos commits
function mostrar_status_y_log() {
    echo ""
    echo "=== Estado del repositorio ==="
    git status
    echo ""
    echo "=== Últimos commits (últimos 5) ==="
    git log --oneline -n 5
}

# 7. Gestión de tags
function gestionar_tags() {
    while true; do
        echo ""
        echo "=== Gestión de tags ==="
        echo "a) Listar tags"
        echo "b) Crear un tag"
        echo "c) Borrar un tag"
        echo "d) Volver al menú principal"
        echo -n "Seleccione una opción: "
        read opcion_tags
        case "$opcion_tags" in
            a|A)
                echo ""
                git tag
                ;;
            b|B)
                echo -n "Ingrese el nombre del tag a crear: "
                read tag_name
                echo -n "Ingrese un mensaje descriptivo para el tag: "
                read tag_msg
                git tag -a "$tag_name" -m "$tag_msg"
                echo "Tag '$tag_name' creado."
                ;;
            c|C)
                echo -n "Ingrese el nombre del tag a borrar: "
                read tag_name
                git tag -d "$tag_name"
                echo "Tag '$tag_name' borrado."
                ;;
            d|D)
                break
                ;;
            *)
                echo "Opción no válida, intente de nuevo."
                ;;
        esac
    done
}

# 8. Gestión de git bisect
function gestionar_bisect() {
    echo ""
    echo "=== Gestión de Git Bisect ==="
    echo "El proceso de git bisect te ayudará a identificar el commit problemático."
    echo "1) Se iniciará la sesión de bisect."
    echo "2) Se marcará el commit actual como 'malo'."
    echo "3) Debes indicar un commit 'bueno' conocido."
    echo "4) Luego, sigue las instrucciones interactivas de git bisect."
    echo ""
    echo -n "¿Desea iniciar el proceso de git bisect? (s/n): "
    read confirmacion
    if [[ "$confirmacion" =~ ^[sS] ]]; then
        echo -n "Ingrese el identificador del commit 'bueno': "
        read commit_bueno
        git bisect start
        git bisect bad
        git bisect good "$commit_bueno"
        echo "Git bisect ha iniciado. Sigue las instrucciones que se muestran en la terminal."
    else
        echo "Operación cancelada."
    fi
}

# 9. Gestión de git diff
function gestionar_diff() {
    while true; do
        echo ""
        echo "=== Gestión de Git Diff ==="
        echo "a) Mostrar diferencias entre el working tree y el área de staging (git diff)"
        echo "b) Mostrar diferencias entre el área de staging y el último commit (git diff --cached)"
        echo "c) Comparar diferencias entre dos ramas o commits"
        echo "d) Comparar diferencias de un archivo específico"
        echo "e) Volver al menú principal"
        echo -n "Seleccione una opción: "
        read opcion_diff
        case "$opcion_diff" in
            a|A)
                echo ""
                git diff
                ;;
            b|B)
                echo ""
                git diff --cached
                ;;
            c|C)
                echo -n "Ingrese el primer identificador (rama o commit): "
                read id1
                echo -n "Ingrese el segundo identificador (rama o commit): "
                read id2
                git diff "$id1" "$id2"
                ;;
            d|D)
                echo -n "Ingrese el primer identificador (rama o commit): "
                read id1
                echo -n "Ingrese el segundo identificador (rama o commit): "
                read id2
                echo -n "Ingrese la ruta del archivo: "
                read archivo_path
                git diff "$id1" "$id2" -- "$archivo_path" | cat
                ;;
            e|E)
                break
                ;;
            *)
                echo "Opción no válida, intente de nuevo."
                ;;
        esac
    done
}

# 10. Gestión de hooks
function gestionar_hooks() {
    while true; do
        echo ""
        echo "=== Gestión de hooks ==="
        echo "a) Listar hooks disponibles"
        echo "b) Crear/instalar un hook (ej. pre-commit)"
        echo "c) Editar un hook existente"
        echo "d) Borrar un hook"
        echo "e) Volver al menú principal"
        echo -n "Seleccione una opción: "
        read opcion_hooks
        case "$opcion_hooks" in
            a|A)
                echo ""
                echo "Hooks en el directorio .git/hooks:"
                ls .git/hooks
                ;;
            b|B)
                echo "Se instalará un hook pre-commit para verificar comentarios de documentación."
                hook_name="pre-commit"
                hook_file=".git/hooks/$hook_name"

                # Contenido del hook
                cat << 'EOF' > "$hook_file"
#!/bin/bash
# Hook pre-commit para verificar documentación en funciones

# Lista de archivos modificados que son de código fuente común
files=$(git diff --cached --name-only --diff-filter=ACM | grep '\.\(c\|h\|js\|py\|java\|sh\)$')

# Si no hay archivos de código fuente modificados, salir sin error
if [ -z "$files" ]; then
    exit 0
fi

echo "Verificando comentarios de documentación en archivos modificados..."

has_error=0
for file in $files; do
    # Ejemplo simplificado: verificar si existe al menos una línea con comentario ('#' para scripts, '//' para otros)
    comment_pattern="#" # Por defecto para scripts .sh
    if [[ "$file" == *.py ]]; then
        comment_pattern="#"
    elif [[ "$file" == *.c ]] || [[ "$file" == *.h ]] || [[ "$file" == *.js ]] || [[ "$file" == *.java ]]; then
        comment_pattern="//"
    fi

    # Comprueba si el archivo existe y si contiene el patrón de comentario
    if [ -f "$file" ] && ! grep -q "$comment_pattern" "$file"; then
        echo "Error: El archivo '$file' no parece contener comentarios de documentación (${comment_pattern})."
        has_error=1
    fi
done

if [ $has_error -eq 1 ]; then
    echo "Commit abortado. Agrega comentarios a los archivos indicados."
    exit 1 # Aborta el commit
fi

echo "Verificación de comentarios completada."
exit 0 # Permite el commit
EOF
                # Asignar permisos de ejecución
                chmod +x "$hook_file"
                echo "Hook '$hook_name' para verificación de comentarios instalado."
                ;;
            c|C)
                echo -n "Ingrese el nombre del hook a editar: "
                read hook_name
                hook_file=".git/hooks/$hook_name"
                if [[ -f "$hook_file" ]]; then
                    ${EDITOR:-nano} "$hook_file"
                else
                    echo "El hook '$hook_name' no existe."
                fi
                ;;
            d|D)
                echo -n "Ingrese el nombre del hook a borrar: "
                read hook_name
                hook_file=".git/hooks/$hook_name"
                if [[ -f "$hook_file" ]]; then
                    rm "$hook_file"
                    echo "Hook '$hook_name' eliminado."
                else
                    echo "El hook '$hook_name' no existe."
                fi
                ;;
            e|E)
                break
                ;;
            *)
                echo "Opción no válida, intente de nuevo."
                ;;
        esac
    done
}

# 11. Generar reporte
function generar_reporte() {
    report_file="reporte_git_$(date +%Y%m%d_%H%M%S).txt"
    echo "Generando reporte en '$report_file'..."

    {
        # Pipe commands to cat to prevent paging issues
        echo "====== Reporte del Repositorio Git ======"
        echo "Generado el: $(date)"
        echo ""

        echo "=== Estado del repositorio (git status) ==="
        git status | cat 
        echo ""

        echo "=== Ramas existentes (git branch) ==="
        git branch -vv | cat # Más verboso para ver tracking
        echo ""

        echo "=== Últimos 5 commits (git log -n 5) ==="
        git log --oneline --graph --decorate -n 5 | cat
        echo ""

        echo "=== Lista de stashes (git stash list) ==="
        git stash list | cat
        echo ""

        echo "=== Tags existentes (git tag) ==="
        git tag -l --sort=-creatordate | cat # Listar tags ordenados por fecha de creación
        echo ""

        echo "=== Remotos configurados (git remote -v) ==="
        git remote -v | cat
        echo ""

        echo "====== Fin del Reporte ======"

    } > "$report_file" # Redirige toda la salida de los comandos dentro de {} al archivo

    if [ $? -eq 0 ]; then
        echo "Reporte generado exitosamente en '$report_file'."
    else
        echo "Error al generar el reporte."
    fi
}

# 12. Merge automatizado
function merge_automatizado() {
    echo ""
    echo "=== Merge automatizado ==="
    echo -n "Ingrese el nombre de la rama a fusionar en la rama actual: "
    read rama_a_fusionar
    echo "Seleccione la estrategia de resolución de conflictos:"
    echo "  1) theirs (prioriza los cambios de la rama fusionada)"
    echo "  2) ours (prioriza los cambios de la rama actual)"
    echo -n "Seleccione una estrategia (1/2): "
    read estrategia_opcion

    estrategia_git=""
    if [[ "$estrategia_opcion" == "1" ]]; then
        estrategia_git="-X theirs"
        echo "Usando estrategia 'theirs'."
    elif [[ "$estrategia_opcion" == "2" ]]; then
        estrategia_git="-X ours"
        echo "Usando estrategia 'ours'."
    else
        echo "Opción de estrategia inválida. Abortando."
        return
    fi

    echo "Intentando fusionar '$rama_a_fusionar' en la rama actual ($(git rev-parse --abbrev-ref HEAD))..."
    # Ejecutar el merge con la estrategia seleccionada
    git merge "$rama_a_fusionar" $estrategia_git | cat

    # Verificar el estado del merge
    if [ $? -eq 0 ]; then
        echo "Merge completado exitosamente con la estrategia seleccionada."
    else
        echo "El merge falló o encontró conflictos que no se pudieron resolver automáticamente con la estrategia seleccionada."
        echo "Puede que necesites resolver los conflictos manualmente y luego hacer 'git commit'."
        echo "Para abortar el merge, usa 'git merge --abort'."
    fi
    git status -s # Mostrar un estado breve
}

# Bucle principal del menú
while true; do
    mostrar_menu_principal
    read opcion
    case "$opcion" in
        1) restaurar_commit ;;
        2) agregar_submodulo ;;
        3) agregar_subtree ;;
        4) gestionar_ramas ;;
        5) gestionar_stash ;;
        6) mostrar_status_y_log ;;
        7) gestionar_tags ;;
        8) gestionar_bisect ;;
        9) gestionar_diff ;;
        10) gestionar_hooks ;;
        11) 
            # Llamada a la función del ejercicio 5
            generar_reporte 
            ;;
        12) # <-- Nuevo caso para merge automatizado
            merge_automatizado
            ;;
        13) # <-- Salir ahora es la opción 13
            echo "Saliendo del script."
            exit 0
            ;;
        *)
            echo "Opción no válida, intente de nuevo."
            ;;
    esac
done

