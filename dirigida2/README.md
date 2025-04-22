# Actividad: Exploración y administración avanzada de Git mediante un script interactivo

Instrucciones previas:

Descargar guardar y asignar permisos al script que está en la raíz del repositorio:

![](https://i.imgur.com/ps7PACH.png)

Ejecutando el script para ver que funciona:

![](https://i.imgur.com/pj9rQdl.png)

### Preguntas

1.  **¿Qué diferencias observas en el historial del repositorio después de restaurar un commit mediante reflog?**
    *   Al restaurar usando `git reset --hard` (como en la opción 1 del script), el historial de la rama actual se reescribe. Los commits hechos *después* del punto restaurado dejan de ser parte de la historia visible de esa rama (en `git log`), aunque permanecen en el reflog por un tiempo. El `HEAD` y el índice se actualizan al estado del commit restaurado.
2.  **¿Cuáles son las ventajas y desventajas de utilizar submódulos en comparación con subtrees?**
    *   **Submódulos:** Ventaja: Mantienen historiales separados, fácil actualizar/contribuir al repo externo. Desventaja: Requieren comandos extra (`submodule update`), clonado inicial necesita `--recurse-submodules`.
    *   **Subtrees:** Ventaja: Integran el código directamente, clonado simple. Desventaja: Mezclan historiales (puede ser complejo), más difícil devolver cambios al repo original.
3.  **¿Cómo impacta la creación y gestión de hooks en el flujo de trabajo y la calidad del código?**
    *   Impactan positivamente al automatizar validaciones (formato, tests, mensajes de commit) antes de completar acciones como `commit` o `push`, mejorando la consistencia y calidad. Pueden ralentizar ligeramente las operaciones de Git y requieren ser gestionados (asegurar que el equipo los use).
4.  **¿De qué manera el uso de `git bisect` puede acelerar la localización de un error introducido recientemente?**
    *   `git bisect` usa una búsqueda binaria en el historial. Marcando un commit "malo" (con error) y uno "bueno" (sin error), Git presenta automáticamente commits intermedios para probar, reduciendo exponencialmente el número de pasos necesarios para encontrar el commit problemático comparado con una revisión manual lineal.
5.  **¿Qué desafíos podrías enfrentar al administrar ramas y stashes en un proyecto con múltiples colaboradores?**
    *   **Ramas:** Conflictos frecuentes al integrar cambios (merge hell), necesidad de políticas para mantener ramas actualizadas (rebase/merge), posible acumulación de ramas obsoletas y la importancia de convenciones de nombrado.
    *   **Stashes:** Son locales y no se comparten fácilmente; aplicar stashes sobre código base diferente puede generar conflictos; riesgo de olvidar stashes antiguos.

Siguiendo las instrucciones, extendí el script `git_avanzado.sh`.

##### Ejercicio 1: Renombrar ramas

Agregué la opción 'f) Renombrar una rama' al menú de gestión de ramas.

```bash
# ...
        echo "d) Borrar una rama"
        echo "e) Renombrar una rama" # <--- Opción agregada (se recorre la 'e' original)
        echo "f) Volver al menú principal" # <--- Opción original 'e' recorrida
        echo -n "Seleccione una opción: "
        read opcion_rama
        case "$opcion_rama" in
            # ... existing code ...
            d|D)
                echo -n "Ingrese el nombre de la rama a borrar: "
                read rama
                git branch -d "$rama"
                echo "Rama '$rama' borrada."
                ;;
            e|E) # <--- Nueva lógica para renombrar
                echo -n "Ingrese el nombre de la rama actual: "
                read rama_actual
                echo -n "Ingrese el nuevo nombre para la rama: "
                read nuevo_nombre
                # Verificar si la rama actual es la que se quiere renombrar
                current_branch=$(git rev-parse --abbrev-ref HEAD)
                if [[ "$rama_actual" == "$current_branch" ]]; then
                    git branch -m "$nuevo_nombre"
                    echo "Rama '$rama_actual' renombrada a '$nuevo_nombre' (era la rama actual)."
                else
                    git branch -m "$rama_actual" "$nuevo_nombre"
                    echo "Rama '$rama_actual' renombrada a '$nuevo_nombre'."
                fi
                ;;
            f|F) # <--- Opción original 'e' recorrida
                break
                ;;
            *)
                echo "Opción no válida, intente de nuevo."
                ;;
        esac
# ...
```

Luego ejecuté la nueva opción para renombrar una rama.

![](blob:https://imgur.com/b2b305d2-b672-485c-b92d-4a2a92e001e9)

Ahora cuando hago `git branch` me sale el nuevo nombre de la rama

![](https://i.imgur.com/5NTjuDk.png)

##### Ejercicio 2: Diff de archivo específico

Añadí la opción 'e) Comparar diferencias de un archivo específico' al submenú de diff.

```bash
        echo "c) Comparar diferencias entre dos ramas o commits"
        echo "d) Comparar diferencias de un archivo específico" # <-- Nueva opción
        echo "e) Volver al menú principal" # <-- Opción original 'd' recorrida
        echo -n "Seleccione una opción: "
        read opcion_diff
        case "$opcion_diff" in
            # ... existing code ...
            c|C)
                echo -n "Ingrese el primer identificador (rama o commit): "
                read id1
                echo -n "Ingrese el segundo identificador (rama o commit): "
                read id2
                git diff "$id1" "$id2"
                ;;
            d|D) # <-- Nueva lógica para diff de archivo
                echo -n "Ingrese el primer identificador (rama o commit): "
                read id1
                echo -n "Ingrese el segundo identificador (rama o commit): "
                read id2
                echo -n "Ingrese la ruta del archivo: "
                read archivo_path
                git diff "$id1" "$id2" -- "$archivo_path"
                ;;
            e|E) # <-- Opción original 'd' recorrida
                break
                ;;
            *)
                echo "Opción no válida, intente de nuevo."
                ;;
        esac
```

Para probarlo primero hice:
```
echo "Contenido inicial" > archivo_prueba.txt
git add archivo_prueba.txt
git commit -m "Commit inicial de archivo_prueba"
echo "Contenido modificado" > archivo_prueba.txt
git add archivo_prueba.txt
git commit -m "Commit modificado de archivo_prueba"
```

Luego ejecuté la nueva opción para ver el diff de un archivo entre dos commits/ramas.

![](https://i.imgur.com/iDMsGRA.png)

##### Ejercicio 3: Hook de pre-commit para documentación

Modifiqué la opción 'b' del menú de hooks para instalar un hook pre-commit específico que verifica comentarios.

```bash
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
```

Para probarlo primero ejecuté el script para instalar el hook (opción 10 -> b), y luego hice:

```bash
echo "Nuevo contenido sin comentarios" > archivo_prueba.sh
git add archivo_prueba.sh
git commit -m "Intento de commit sin comentarios"
```

Instalé el hook usando la opción modificada y probé hacer un commit.

![](https://i.imgur.com/FDAUjhW.png)

Como pueden ver me salió:
```bash
Verificando comentarios de documentación en archivos modificados...
Error: El archivo 'archivo_prueba.sh' no parece contener comentarios de documentación (#).
Commit abortado. Agrega comentarios a los archivos indicados.
```

##### Ejercicio 4: Merge automatizado con estrategia

Agregué la opción '12) Merge automatizado de una rama' al menú principal.

```bash
# Script 'git_avanzado.sh' modificado

# ... (otras funciones) ...

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
    git merge "$rama_a_fusionar" $estrategia_git

    # Verificar el estado del merge
    if [ $? -eq 0 ]; then
        echo "Merge completado exitosamente con la estrategia seleccionada."
    else
        echo "El merge falló o encontró conflictos que no se pudieron resolver automáticamente con la estrategia '$estrategia_git'."
        echo "Puede que necesites resolver los conflictos manualmente y luego hacer 'git commit'."
        echo "Para abortar el merge, usa 'git merge --abort'."
    fi
    git status -s # Mostrar un estado breve
}

# ... (Bucle principal del menú) ...
function mostrar_menu_principal() {
    # ... (opciones 1-11) ...
    echo "12) Merge automatizado de una rama" # <-- Nueva opción
    echo "13) Salir" # <-- Opción original 11 recorrida
    echo -n "Seleccione una opción: "
}

# Bucle principal del menú
while true; do
    mostrar_menu_principal
    read opcion
    case "$opcion" in
        # ... (casos 1-10) ...
        11) # <-- Caso original 11 ahora es para el reporte
            generar_reporte # Asumiendo que la función del ejercicio 5 se llama así
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
```
Para que no me afecte el hook del ejercicio 3 hice
un
```
git reset --hard
99e0e341ea3c2b1c3147b753f452d79da0ff173f
```
Que me manda a antes de hacer los commits. (busqué 
el hash en git log)

Ahora sí. Para probar el cambio, primero creé un conflicto:

```bash
git checkout -b feature/merge-test

echo "Linea original en feature" > merge_conflict_test.txt
git add merge_conflict_test.txt
git commit -m "Commit inicial en feature/merge-test"

git checkout main

echo "Linea original y conflictiva en main" > merge_conflict_test.txt
git add merge_conflict_test.txt
git commit -m "Commit conflictivo en main"
```
![](https://i.imgur.com/lLnAWzt.png)
Luego ejecuté la nueva opción para hacer un merge automático.

![](https://i.imgur.com/KquFx4B.png)

##### Ejercicio 5: Generar reporte del repositorio

Agregué la opción '11) Generar reporte de estado del repositorio' (reemplazando la de Salir original) y la función correspondiente.

```bash
# Script 'git_avanzado.sh' modificado

# ... (otras funciones) ...

# 11. Generar reporte
function generar_reporte() {
    report_file="reporte_git_$(date +%Y%m%d_%H%M%S).txt"
    echo "Generando reporte en '$report_file'..."

    {
        echo "====== Reporte del Repositorio Git ======"
        echo "Generado el: $(date)"
        echo ""

        echo "=== Estado del repositorio (git status) ==="
        git status
        echo ""

        echo "=== Ramas existentes (git branch) ==="
        git branch -vv # Más verboso para ver tracking
        echo ""

        echo "=== Últimos 5 commits (git log -n 5) ==="
        git log --oneline --graph --decorate -n 5
        echo ""

        echo "=== Lista de stashes (git stash list) ==="
        git stash list
        echo ""

        echo "=== Tags existentes (git tag) ==="
        git tag -l --sort=-creatordate # Listar tags ordenados por fecha de creación
        echo ""

        echo "=== Remotos configurados (git remote -v) ==="
        git remote -v
        echo ""

        echo "====== Fin del Reporte ======"

    } > "$report_file" # Redirige toda la salida de los comandos dentro de {} al archivo

    if [ $? -eq 0 ]; then
        echo "Reporte generado exitosamente en '$report_file'."
    else
        echo "Error al generar el reporte."
    fi
}

# ... (Menú principal y bucle principal actualizados como en el Ejercicio 4) ...

function mostrar_menu_principal() {
    echo ""
    echo "====== Menú avanzado de Git ======"
    # ... (opciones 1-10) ...
    echo "11) Generar reporte de estado del repositorio" # <-- Nueva opción 11
    echo "12) Merge automatizado de una rama"
    echo "13) Salir" # <-- Salir ahora es la opción 13
    echo -n "Seleccione una opción: "
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
        11) generar_reporte ;; # <-- Llamada a la nueva función
        12) merge_automatizado ;;
        13) # <-- Salir
            echo "Saliendo del script."
            exit 0
            ;;
        *) echo "Opción no válida, intente de nuevo." ;;
    esac
done
```

Ejecución:
![](https://i.imgur.com/fes3XTs.png)

Y este es el reporte dado:

![](https://i.imgur.com/EJctHqV.png)

Moví el reporte a la carpeta dirigida2.
Reporte [aquí](reporte_git_20250422_134328.txt)