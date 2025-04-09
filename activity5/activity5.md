# Actividad 5

#### 1. Fusión Fast-forward (git merge --ff)
![](https://i.imgur.com/fRK2eza.png)

**Pregunta:** Muestra la estructura de commits resultante.

![](https://i.imgur.com/6Hd2SMM.png)

#### 2. Fusión No-fast-forward (git merge --no-ff)

![](https://i.imgur.com/21qjpzp.png)

**Pregunta:** Muestra el log de commits resultante.
![](https://i.imgur.com/XKdUJjA.png)


##### 3. Fusión squash (git merge --squash)

![](https://i.imgur.com/kQoFg2a.png)
![](https://i.imgur.com/W9lcxZh.png)
![](https://i.imgur.com/qC4Kjnz.png)


#### Ejercicios

1. **Clona un repositorio Git con múltiples ramas.**  
![](https://i.imgur.com/tR8ljzD.png)
![](https://i.imgur.com/u5muqYp.png)
![](https://i.imgur.com/4BoAYfb.png)
usando `git merge --ff`
![](https://i.imgur.com/r975Bav.png)

**Pregunta:** ¿En qué situaciones recomendarías evitar el uso de `git merge --ff`? Reflexiona sobre las desventajas de este método.

Dado que fast-forward solo avanza el puntero de la rama base se perdería el historial de commits, lo cual puede ser un poco contraproducente en equipos colaborativos cuando se quiere tener un registro y orden de los avances realizados a lo largo del proyecto. 

2. **Simula un flujo de trabajo de equipo.**

![](https://i.imgur.com/6kHMZvX.png)
![](https://i.imgur.com/ntLH1eI.png)
Fusiona ambas ramas con `git merge --no-ff` para ver cómo se crean los commits de fusión.
![](https://i.imgur.com/4vkZ0Xv.png)
![](https://i.imgur.com/LAkAp3R.png)
![](https://i.imgur.com/NJW3kh3.png)

**Pregunta:** ¿Cuáles son las principales ventajas de utilizar `git merge --no-ff` en un proyecto en equipo? ¿Qué problemas podrían surgir al depender excesivamente de commits de fusión?

Las principales ventajas son que se tiene un historial más detallado de cuándo se hicieron las fusiones, además de una mayor comprensión por parte del equipo de desarrollo con el proyecto. Algunos problemas a surgir sería que ante situaciones en las que sea innecesario tener el registro de una fusión ya sea por una corrección de sintaxis o de formato, espaciados, etc puede aumentar la complejidad del grafo al visualizarlo y sería más difícil analizar el proyecto debido a múltiples fusiones.

3. **Crea múltiples commits en una rama.**
![](https://i.imgur.com/K2CDSU4.png)

Fusiona la rama con `git merge --squash` para aplanar todos los commits en uno solo.
![](https://i.imgur.com/Ou1tUiK.png)

Después del commit 
![](https://i.imgur.com/8QWQA39.png)

![](https://i.imgur.com/AUQ3t4l.png)

**Pregunta:** ¿Cuándo es recomendable utilizar una fusión squash? ¿Qué ventajas ofrece para proyectos grandes en comparación con fusiones estándar?
Es recomendable cuando se trabaja en ramas con features muy pequeñas o muchas correcciones menores. Sobre las ventajas, es que se reduce el desorden en el historial al poder integrar cambios pequeños. Haciendo más limpio el historial y el flujo de trabajo solo teniendo los commits más significativos debido a la gran cantidad de estos por ser un proyecto grande.

#### Resolver conflictos en una fusión non-fast-forward

![](https://i.imgur.com/SD4zFJR.png)
![](https://i.imgur.com/50SDVzj.png)
![](https://i.imgur.com/IJZZgPi.png)

- ¿Qué pasos adicionales tuviste que tomar para resolver el conflicto?
En este caso fue decidir si conservar los cambios de cada rama. Además de entrar a vim para confirmar el mensaje del commit después del comando `git commit`. 
- ¿Qué estrategias podrías emplear para evitar conflictos en futuros desarrollos colaborativos?
Asegurarse de tener la rama principal actualizada y en cada rama nueva que se trabaje esta debe estar actualizada a la versión más reciente para evitar conflictos.

#### Ejercicio: Comparar los historiales con git log después de diferentes fusiones

![](https://i.imgur.com/WzqSynY.png)

Fusiona feature-1 usando fast-forward:
![](https://i.imgur.com/wU8owzV.png)

Fusiona feature-2 usando non-fast-forward:
![](https://i.imgur.com/GG5m9rv.png)

Realiza una nueva rama feature-3 con múltiples commits y fusiónala con squash:
![](https://i.imgur.com/1CQmW6l.png)
Compara el historial de Git:

![](https://i.imgur.com/DJPosHm.png)
![](https://i.imgur.com/YsEGICu.png)

**Preguntas:**

- ¿Cómo se ve el historial en cada tipo de fusión?
- ¿Qué método prefieres en diferentes escenarios y por qué?
Se evidencia que la única fusión visible es --no-ff dado que este sí registra el historial. Mientras con ff no se registra, y squash une los commits a uno solo.
Sobre cuál prefiero sería --no-ff dado que me gusta tener el registro de todos los cambios que se hagan en un proyecto y así poder revertir en caso de cualquier fallo así sea un cambio mínimo.

#### Ejercicio: Usando fusiones automáticas y revertir fusiones

![](https://i.imgur.com/68R5POn.png)

![](https://i.imgur.com/yvk31O9.png)

![](https://i.imgur.com/t05ccEl.png)
(apareció en vim al revertir)

**Preguntas:**

- ¿Cuándo usarías un comando como git revert para deshacer una fusión?
- ¿Qué tan útil es la función de fusión automática en Git?

Lo utilizaría cuando haya un conflicto grande entre las dos ramas, preferiría primero arreglar y actualizar la otra rama antes de fusionarla a main. 
Para este ejemplo si hubieron conflictos, pero cuando no los hay y se hace la fusión automática ahorra mucho tiempo para saber si se pueden integrar los cambios. 

#### Ejercicio: Fusión remota en un repositorio colaborativo

![](https://i.imgur.com/3KWSnU3.png)

pull request
![](https://i.imgur.com/aYfIka9.png)
![](https://i.imgur.com/BPXMWuk.png)

**Preguntas:**

- ¿Cómo cambia la estrategia de fusión cuando colaboras con otras personas en un repositorio remoto?
- ¿Qué problemas comunes pueden surgir al integrar ramas remotas?

Cuando se trata de distintos repositorios y estamos en un entorno colaborativo cada modificación debe ser revisada, además de comprobar que no existan conflictos. Es por esto que un pull request facilita mucho estos entornos.
Los problemas más comunes son cuando se olvidan de actualizar los cambios más recientes, también cuando surgen equivocaciones o malas prácticas. Por suerte esto se puede resolver con las metodologías existentes.

#### Ejercicio final: flujo de trabajo completo
Configura un proyecto simulado:

- Crea un proyecto con tres ramas: main, feature1, y feature2.
- Realiza varios cambios en feature1 y feature2 y simula colaboraciones paralelas.
![](https://i.imgur.com/YP9RAhl.png)

- Realiza fusiones utilizando diferentes métodos:
    - Fusiona feature1 con main utilizando `git merge --ff`.
- ![](https://i.imgur.com/Aub4Sbx.png)

    - Fusiona feature2 con main utilizando `git merge --no-ff`
    - 
![](https://i.imgur.com/KDFBNYl.png)
![](https://i.imgur.com/ojn5Krc.png)
![](https://i.imgur.com/Ob83tA5.png)


Haz una rama adicional llamada feature3 y aplasta sus commits utilizando `git merge --squash

![](https://i.imgur.com/ofCzvfJ.png)


Analiza el historial de commits:

- Revisa el historial para entender cómo los diferentes métodos de fusión afectan el árbol de commits.
- Compara los resultados y discute con tus compañeros de equipo cuál sería la mejor estrategia de fusión para proyectos más grandes.

![](https://i.imgur.com/TqVdDIT.png)


Se deja en evidencia que con ff no se visualiza la fusión mientras que con no ff sí. Además de la gran utilidad de squash para cambios pequeños e insignificantes como en este caso una adición de letras que se le pudo haber pasado a un desarrollador, lo cual simplifica la visualización del historial.

Para proyectos más grandes se recomienda squash para minimizar commits innecesarios y no fast forward para tener un registro de cada commit. Además del uso de pull request para la revisión más cómoda de cada fusión a realizar.

