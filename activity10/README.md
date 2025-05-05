# Actividad: Ejecutar pruebas con pytest

Esta actividad se centra en el aprendizaje de pytest como herramienta para ejecutar pruebas unitarias en Python. 
Entre los objetivos se encuentran la instalación, ejecución de pruebas unitarias, salida detallada e informes de covertura para los resultados de las pruebas

**Paso 1: Instalando pytest y pytest-cov**
Primero creé la carpeta correspondiente a la actividad en este caso 10, luego crear y activar el entorno virtual en el cual se instalarán las dependencias requeridas, para este caso `pytest` y `pytest-cov`
![](https://i.imgur.com/X60KZR3.png)

**Paso 2: Escribiendo y ejecutando pruebas con pytest**
El comando `pytest` ejecuta las pruebas que se encuentran en la actividad sin embargo no muestran tanto detalle como lo haría `pytest -v` el cual muestra qué pruebas se ejecutaron y su resultado
![](https://i.imgur.com/otnMXrR.png)

**Paso 3: Añadiendo cobertura de pruebas con pytest-cov**
para conocer cuánto de nuestro código es cubierto por pruevas existe `pytest-cov` el cuál nos muestra el porcentaje de covertura de cada archivo. Para este caso mi directorio es activity10
![](https://i.imgur.com/WDyPW0N.png)

Además se puede generar en formato html para una mejor revisión con el comando `pytest --cov=pruebas_pytest --cov-report=html`, en mi caso con activity10. Y el resultado luce como la image, cabe resaltar que se muestra de archivos, funciones y clases.
![](https://i.imgur.com/p1JYWeT.png)

En caso se quiera hacer reportes individuales existe la opción con el comando `pytest -v --cov=triangle`. Así mismo el reporte HTML. 
![](https://i.imgur.com/Zxo1ssU.png)

También se puede conocer cuando falta covertura con el comando `pytest --cov=triangle --cov-report=term-missing`. Para este ejemplo cubre el 100% por tanto no hay una parte en "missing".

**Paso 4: Añadiendo colores automáticamente**
En caso no se muestren los colores se puede arreglar con el comando ``--color=yes``. Para este ejemplo como se ve en las imágenes, cumple adecuadamente.

**Paso 5: Automatizando la configuración de pytest**
Es posible que al ejecutar `pytest` se puedan tener todas las configuraciones deseadas. En este caso con el archivo setup.cfg se puede definir con encabezados como  [tool:pytest] o [coverage:report], esto con el fin de centralizar la configuración en un solo archivo.


```
[tool:pytest]
addopts = -v --tb=short --cov=. --cov-report=term-missing

[coverage:run]
branch = True

[coverage:report]
show_missing = True
```

[tool:pytest]es una sección específica para configurar pytest.

- addopts: Opciones adicionales para pytest (en este caso, activa la salida detallada -v, el tipo de rastro corto para errores --tb=short, y la cobertura con informe de líneas faltantes --cov-report=term-missing).
- [coverage:run] y [coverage:report]: Configuración para la herramienta de cobertura, en este caso, para medir la cobertura de ramas (branch=True) y mostrar qué líneas faltan (show_missing=True).

En caso solo se quiera configurar pytest se puede con `pytest.ini`

```
[pytest]
addopts = -v --tb=short --cov=. --cov-report=term-missing

[coverage:run]
branch = True

[coverage:report]
show_missing = True
```

**Paso 6: Ejecutando pruebas con la configuración automatizada** 
En este caso existe el archivo setup.cfg con la debida configuración para esta actividad. Al ejecutar `pytest` se obtiene el resultado:
![](https://i.imgur.com/8hsq8hU.png)
