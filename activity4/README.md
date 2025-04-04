# Activity 4

#### Ejercicio 1: Manejo avanzado de ramas y resolución de conflictos

**Objetivo**: Practicar la creación, fusión y eliminación de ramas, así como la resolución de conflictos que puedan surgir durante la fusión.

1. **Crear una nueva rama para una característica:**
![](https://i.imgur.com/c0N3R7L.png)

2. **Modificar archivos en la nueva rama:**
![](https://i.imgur.com/r8Ijnlh.png)

3. **Simular un desarrollo paralelo en la rama main:**
![](https://i.imgur.com/lYdB2Dx.png)

4. **Intentar fusionar la rama feature/advanced-feature en main:**

![](https://i.imgur.com/qxZ7dwo.png)

5. **Resolver el conflicto de fusión:**

![](https://i.imgur.com/gGgMQz5.png)
![](https://i.imgur.com/cXHwJhl.png)


6. **Eliminar la rama fusionada:**
![](https://i.imgur.com/xxlEJrA.png)


#### Ejercicio 2: Exploración y manipulación del historial de commits

1. **Ver el historial detallado de commits:**
![](https://i.imgur.com/YfrAmdC.png)

Las diferencias se pueden ver con `git diff [commit]`
![](https://i.imgur.com/MIwb40B.png)

En este caso se remplazó la línea de `Hello from advanced feature` por `Hello World - updated in main`

2. **Filtrar commits por autor**
![](https://i.imgur.com/K3UJpH8.png)

3. **Revertir un commit:**
![](https://i.imgur.com/bnDRljc.png)

4. **Rebase interactivo:**
![](https://i.imgur.com/W1FgwHE.png)

![](https://i.imgur.com/7y9MZFV.png)

5. **Visualización gráfica del historial:**
![](https://i.imgur.com/oGOIsMz.png)

Se puede ver que hubo un merge entre dos ramas, luego de ciertos commits se hizo un revert para regresar a un anterior y finalmente se regresó en 3 commits atrás.

#### Ejercicio 3: Creación y gestión de ramas desde commits específicos

1. **Crear una nueva rama desde un commit específico:**
![](https://i.imgur.com/7zjdf4k.png)

2. **Modificar y confirmar cambios en la nueva rama:**
![](https://i.imgur.com/foC7GhF.png)

3. **Fusionar los cambios en la rama principal:**
![](https://i.imgur.com/L8WkNiL.png)

4. **Explorar el historial después de la fusión:**
![](https://i.imgur.com/TwseoTO.png)

5. **Eliminar la rama bugfix/rollback-feature**
![](https://i.imgur.com/2xpQgut.png)

#### Ejercicio 4: Manipulación y restauración de commits con git reset y git restore

1. **Hacer cambios en el archivo main.py:**
![](https://i.imgur.com/C0ITXBv.png)

2. **Usar git reset para deshacer el commit:**
![](https://i.imgur.com/xMF5RLP.png)

3. **Usar git restore para deshacer cambios no confirmados:**
![](https://i.imgur.com/rRzgkq6.png)

#### Ejercicio 5: Trabajo colaborativo y manejo de Pull Requests

1. **Crear un nuevo repositorio remoto:**
![](https://i.imgur.com/KyF8Sel.png)

2. **Crear una nueva rama para desarrollo de una característica:**
![](https://i.imgur.com/2SodVd3.png)

3. **Realizar cambios y enviar la rama al repositorio remoto:**

![](https://i.imgur.com/2moZw1Y.png)

4. **Abrir un Pull Request:**
![](https://i.imgur.com/sH2Erko.png)
En este caso el archivo diferente es el `readme` en la rama `feature/team-feature`

5. **Revisar y fusionar el Pull Request:**
![](https://i.imgur.com/ayMgPUS.png)

![](https://i.imgur.com/J2J0wk3.png)

6. **Eliminar la rama remota y local:**

![](https://i.imgur.com/jBYVFzz.png)

#### Ejercicio 6: Cherry-Picking y Git Stash

1. **Realiza y confirma varios cambios en `main.py` en la rama `main`**:
En este caso elegí crear un nuevo archivo python dado que main.py ya tenía contenido previo.

![](https://i.imgur.com/5D390SZ.png)
![](https://i.imgur.com/T8h5FDX.png)

2. **Crear una nueva rama y aplicar el commit específico:**
![](https://i.imgur.com/tpHxo8e.png)

3. **Guardar temporalmente cambios no confirmados:**
![](https://i.imgur.com/DV1WbIf.png)

![](https://i.imgur.com/RjRJhyg.png)

4. **Aplicar los cambios guardados:**
5. **Revisar el historial y confirmar la correcta aplicación de los cambios:**
![](https://i.imgur.com/XnVk8sR.png)

