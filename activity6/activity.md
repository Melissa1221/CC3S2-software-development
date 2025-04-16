# Actividad 6

#### **Parte 1: git rebase para mantener un historial lineal**

- Crea un nuevo repositorio Git y dos ramas, main y new-feature:

![](https://i.imgur.com/1GKqBWA.png)

- Crea y cambia a la rama new-feature:
![](https://i.imgur.com/KoyUm6u.png)

**Pregunta:** Presenta el historial de ramas obtenida hasta el momento.
![](https://i.imgur.com/3y1rp5D.png)
por ahora se visualizan dos ramas, teniendo la segunda un commit adicional

![](https://i.imgur.com/gq5Y1oz.png)

**Tarea**: Realiza el rebase de `new-feature` sobre `main` con los siguientes comandos

![](https://i.imgur.com/dk4APW6.png)

Fusionar y completar el proceso de git rebase
![](https://i.imgur.com/RVPgraT.png)

#### Parte 2: **git cherry-pick para la integración selectiva de commit**

![](https://i.imgur.com/gPkSXz2.png)

**Tarea: Haz cherry-pick de un commit de add-base-documents a main:**

![](https://i.imgur.com/kg3rI4i.png)


1. ¿Por qué se considera que rebase es más útil para mantener un historial de proyecto lineal en comparación con merge?
En mi experiencia con rebase se puede tener un historial más ordenado, teniendo el historial de los commits realizados en la otra rama y de este modo se ve como un proyecto lineal tal y como se menciona. Esto es demasiado útil en proyectos reales en caso se quiera hacer reset. También he utilizado anteriores veces `git pull --rebase`
y ayuda mucho tener un historial lineal incluso cuando traes las últimas modificaciones de una rama. En comparación con merge solo tendríamos un commit que menciona tal fusión sin embargo no cada commit en orden lineal.

2. ¿Qué problemas potenciales podrían surgir si haces rebase en una rama compartida con otros miembros del equipo?
Un problema que puede generar confusiones es que cuando se hace este historial lineal , el hash del commit cambia lo cual puede alterar el orden que llevaban algunos desarrolladores respecto a esto.

3. ¿En qué se diferencia cherry-pick de merge, y en qué situaciones preferirías uno sobre el otro?
Cherry pick tiene un enfoque diferente ya que permite traer un commit en específico para otra rama. Esto es preferible para situaciones en las que necesitas un cambio urgente que solo incluye cierta parte del proyecto, y no toda la demás que probablemente falte testear. Así que para tener updates rápidos se puede usar cherry pick.

4. ¿Por qué es importante evitar hacer rebase en ramas públicas?
Cuando otros desarrolladores clonan o hacen pull de la rama pública, se encuentran con un historial modificado, lo que puede ser confuso y difícil de seguir. Como los commits cambian de lugar o desaparecen, los otros miembros del equipo ya no podrán referirse a ellos de la misma manera, lo que puede dificultar la búsqueda de problemas, la revisión de código y la trazabilidad de los cambios.

#### **Ejercicios teóricos**

1. **Diferencias entre git merge y git rebase**  
    **Pregunta**: Explica la diferencia entre git merge y git rebase y describe en qué escenarios sería más adecuado utilizar cada uno en un equipo de desarrollo ágil que sigue las prácticas de Scrum.

*Git merge* combina ramas preservando el historial de ambas, creando un commit de fusión, lo que genera un historial no lineal. Por otro lado *git rebase* reescribe el historial, aplicando los commits de una rama sobre otra para un historial más limpio y lineal. En equipos ágiles que siguen Scrum, git merge es preferido para ramas compartidas como develop o master para evitar conflictos de sincronización, mientras que git rebase es útil en ramas locales o feature branches antes de integrarlas, para mantener un historial limpio sin afectar a otros miembros del equipo.



2. **Relación entre git rebase y DevOps**  
    **Pregunta**: ¿Cómo crees que el uso de git rebase ayuda a mejorar las prácticas de DevOps, especialmente en la implementación continua (CI/CD)? Discute los beneficios de mantener un historial lineal en el contexto de una entrega continua de código y la automatización de pipelines.

Git rebase optimiza los flujos de CI/CD al mantener un historial de commits lineal y limpio, lo que facilita la identificación de errores mediante bisect, mejora la trazabilidad del código y reduce los conflictos en entornos de integración continua. Esta linealidad simplifica la automatización de pipelines al eliminar la complejidad de resolver múltiples ramas divergentes, permitiendo despliegues más predecibles y la implementación eficiente de estrategias como feature flags o canary releases, y cada cambio representa una unidad atómica identificable que puede ser revisada, probada y desplegada de manera independiente.


3. **Impacto del git cherry-pick en un equipo Scrum**  
    **Pregunta**: Un equipo Scrum ha finalizado un sprint, pero durante la integración final a la rama principal (main) descubren que solo algunos commits específicos de la rama de una funcionalidad deben aplicarse a producción. ¿Cómo podría ayudar git cherry-pick en este caso? Explica los beneficios y posibles complicaciones.

El git cherry-pick permite aplicar selectivamente solo los commits necesarios de una rama de feature a main, es ideal cuando no toda la funcionalidad está lista para producción al final del sprint. Los beneficios incluyen lanzamientos incrementales sin tener que bloquear el flujo de entrega, mantener un historial de cambios limpio y facilitar la integración continua. Con esto, pueden surgir algunas complicaciones como conflictos de merge, duplicación de commits al fusionar posteriormente la rama completa, y desafíos en el seguimiento de cambios debido a diferentes hashes de commit.

#### **Ejercicios prácticos**

1. **Simulación de un flujo de trabajo Scrum con git rebase y git merge**
![](https://i.imgur.com/zqQ2rm0.png)
![](https://i.imgur.com/xhnPbdl.png)

- ¿Qué sucede con el historial de commits después del rebase?
- ¿En qué situación aplicarías una fusión fast-forward en un proyecto ágil?

Después del rebase, el historial de commits aparece como una secuencia lineal, donde los commits de feature se reescriben y se posicionan después de los commits de main, eliminando la bifurcación y creando una historia cronológica aparentemente secuencial con nuevos hashes.
La fusión fast-forward es ideal en un proyecto ágil cuando queremos mantener un historial limpio y lineal sin commits de merge adicionales, especialmente en ramas de corta duración como features pequeñas o hotfixes que queremos integrar rápidamente, permitiendo una trazabilidad clara para revisiones de código y facilitando el uso de herramientas como git bisect para debugging.

**Cherry-pick para integración selectiva en un pipeline CI/CD**

![](https://i.imgur.com/oNM5tk7.png)


![](https://i.imgur.com/xRdF3YI.png)

En un pipeline CI/CD, utilizaría cherry-pick para integrar selectivamente cambios listos a producción mediante la automatización del proceso utilizando scripts que identifiquen commits con etiquetas específicas (como "production-ready"), aplicándolos a la rama de producción después de validar que pasan todas las pruebas automatizadas, permitiendo despliegues parciales mientras el desarrollo continúa. Las ventajas de cherry-pick en DevOps incluyen liberaciones incrementales sin bloquear el desarrollo, aislamiento de funcionalidades problemáticas, capacidad para implementar hotfixes específicos sin comprometer otras características en desarrollo, y mayor flexibilidad para gestionar el riesgo en entornos críticos, permitiendo un enfoque gradual y controlado para la entrega continua.

#### **Git, Scrum y Sprints**

#### **Fase 1: Planificación del sprint (sprint planning)**

**Ejercicio 1: Crear ramas de funcionalidades (feature branches)**

![](https://i.imgur.com/ky1a7Gx.png)

**Pregunta:** ¿Por qué es importante trabajar en ramas de funcionalidades separadas durante un sprint?

Es importante para que no haya conflictos de modificaciones en la misma rama, incluso cuando son features diferentes. En general, es importante ya que el proyecto se puede dividir en diferentes features según el sprint y los desarrolladores pueden tomar una de estas. De este modo se agiliza el trabajo en el proyecto y en el tiempo de entrega.

#### **Fase 2: Desarrollo del sprint (sprint execution)**

**Ejercicio 2: Integración continua con git rebase**

![](https://i.imgur.com/kcFw4x2.png)


**Pregunta:** ¿Qué ventajas proporciona el rebase durante el desarrollo de un sprint en términos de integración continua?

Al tener un historial lineal los desarrolladores pueden estar al tanto de todos los commits realizados, y el orden de estos a lo largo del proyecto, incluso si trabajaron en diferentes ramas.
#### **Fase 3: Revisión del sprint (sprint review)**

**Ejercicio 3: Integración selectiva con git cherry-pick**

![](https://i.imgur.com/hSQINZY.png)
![](https://i.imgur.com/B2P77Tq.png)


**Pregunta:** ¿Cómo ayuda `git cherry-pick` a mostrar avances de forma selectiva en un sprint review?

Con cherry pick se puede seccionar un commit específico que está listo para revisión, de este modo se pueden tener features necesarias para el sprint cuando se requiere rapidez para la entrega.
#### **Fase 4: Retrospectiva del sprint (sprint retrospective)**

**Ejercicio 4: Revisión de conflictos y resolución**
![](https://i.imgur.com/O85YwxM.png)
![](https://i.imgur.com/PG7ewyq.png)


**Pregunta**: ¿Cómo manejas los conflictos de fusión al final de un sprint? ¿Cómo puede el equipo mejorar la comunicación para evitar conflictos grandes?

Los equipos deberían comunicarse cada vez que tienen cambios listos o para revisión, de este modo los demás están al tanto y pueden fusionar los avances de los demás sin modificarlo. Dado que cuando se intenta fusionar una rama desactualizada es cuando surgen estos conflictos. Los conflictos se soluciones comparando las diferencias y verificando la versión más reciente y estable.

#### **Fase 5: Fase de desarrollo, automatización de integración continua (CI) con git rebase**

**Ejercicio 5: Automatización de rebase con hooks de Git**

![](https://i.imgur.com/wbY5FW4.png)
![](https://i.imgur.com/PIQaeWZ.png)


**Pregunta**: ¿Qué ventajas y desventajas observas al automatizar el rebase en un entorno de CI/CD?

Ofrece ventajas como historial lineal consistente, reducción de conflictos tardíos al integrar tempranamente, mayor trazabilidad de cambios y simplificación de pipelines de despliegue. Sin embargo, presenta desventajas como la reescritura forzada del historial que requiere git push -f lo cual es riesgoso en ramas compartidas, posibles conflictos silenciosos durante el rebase automático que interrumpen el flujo de trabajo, complicaciones en hooks pre-push que pueden fallar en entornos distribuidos, y mayor complejidad para desarrolladores que deben entender las implicaciones del rebase automático. 

### **Navegando conflictos y versionado en un entorno devOps**

1. **Inicialización del proyecto y creación de ramas**
![](https://i.imgur.com/tqyvnqB.png)

**Fusión y resolución de conflictos**

![](https://i.imgur.com/IY2TcKK.png)

**Simulación de fusiones y uso de git diff**


![](https://i.imgur.com/baNXFp6.png)

**Uso de git mergetool**

![](https://i.imgur.com/Zc3Gano.png)

**Uso de git revert y git reset**
![](https://i.imgur.com/ROuGrwQ.png)


**Versionado semántico y etiquetado**

![](https://i.imgur.com/0v9qJ11.png)

**Aplicación de git bisect para depuración**
![](https://i.imgur.com/Tjztq6p.png)

#### **Preguntas**

1. **Ejercicio para git checkout --ours y git checkout --theirs**
    
    **Contexto**: En un sprint ágil, dos equipos están trabajando en diferentes ramas. Se produce un conflicto de fusión en un archivo de configuración crucial. El equipo A quiere mantener sus cambios mientras el equipo B solo quiere conservar los suyos. El proceso de entrega continua está detenido debido a este conflicto.
    
    **Pregunta**:  
    ¿Cómo utilizarías los comandos `git checkout --ours` y `git checkout --theirs` para resolver este conflicto de manera rápida y eficiente? Explica cuándo preferirías usar cada uno de estos comandos y cómo impacta en la pipeline de CI/CD. ¿Cómo te asegurarías de que la resolución elegida no comprometa la calidad del código?

En situaciones de conflicto, `git checkout --ours` mantiene los cambios de nuestra rama actual mientras `git checkout --theirs` conserva los de la rama que estamos integrando. Para el caso planteado, desde la rama del equipo A usaría `--ours` para mantener sus cambios, y desde la perspectiva del equipo B, usaría `--theirs`. Esta resolución rápida desbloquea inmediatamente el pipeline de CI/CD sin necesidad de negociaciones prolongadas. Para garantizar la calidad, implementaría pruebas automáticas que validen la configuración resultante y establecería un proceso de comunicación para informar al otro equipo sobre la decisión tomada.
    
2. **Ejercicio para git diff**
    
    **Contexto**: Durante una revisión de código en un entorno ágil, se observa que un pull request tiene una gran cantidad de cambios, muchos de los cuales no están relacionados con la funcionalidad principal. Estos cambios podrían generar conflictos con otras ramas en la pipeline de CI/CD.
    
    **Pregunta**:  
    Utilizando el comando `git diff`, ¿cómo compararías los cambios entre ramas para identificar diferencias específicas en archivos críticos? Explica cómo podrías utilizar `git diff feature-branch..main` para detectar posibles conflictos antes de realizar una fusión y cómo esto contribuye a mantener la estabilidad en un entorno ágil con CI/CD.
    
Para identificar diferencias críticas entre ramas ejecutaría `git diff feature-branch..main --name-status` para visualizar los archivos modificados y luego `git diff feature-branch..main -- path/to/critical/file` para inspeccionar cambios específicos. Esto permite detectar conflictos potenciales antes de la fusión, identificar modificaciones no relacionadas con la funcionalidad principal y mantener la estabilidad del pipeline al facilitar revisiones enfocadas que reducen el riesgo de integración.
    
3. **Ejercicio para git merge --no-commit --no-ff**
    
    **Contexto**: En un proyecto ágil con CI/CD, tu equipo quiere simular una fusión entre una rama de desarrollo y la rama principal para ver cómo se comporta el código sin comprometerlo inmediatamente en el repositorio. Esto es útil para identificar posibles problemas antes de completar la fusión.
    
    **Pregunta**:  
    Describe cómo usarías el comando `git merge --no-commit --no-ff` para simular una fusión en tu rama local. ¿Qué ventajas tiene esta práctica en un flujo de trabajo ágil con CI/CD, y cómo ayuda a minimizar errores antes de hacer commits definitivos? ¿Cómo automatizarías este paso dentro de una pipeline CI/CD?
    
El comando `git merge --no-commit --no-ff` genera una simulación de fusión sin crear un commit, proporcionando una previsualización de la integración. Esta técnica en entornos ágiles con CI/CD permite verificar la compatibilidad del código y probar localmente la integración antes de afectar al equipo. Para automatizarlo, implementaría un job específico en el pipeline que ejecute esta fusión simulada, lance pruebas sobre el resultado y genere un reporte, todo sin modificar las ramas principales hasta confirmar su estabilidad.

4. **Ejercicio para git mergetool**
    
    **Contexto**: Tu equipo de desarrollo utiliza herramientas gráficas para resolver conflictos de manera colaborativa. Algunos desarrolladores prefieren herramientas como vimdiff o Visual Studio Code. En medio de un sprint, varios archivos están en conflicto y los desarrolladores prefieren trabajar en un entorno visual para resolverlos.
    
    **Pregunta**:  
    Explica cómo configurarías y utilizarías `git mergetool` en tu equipo para integrar herramientas gráficas que faciliten la resolución de conflictos. ¿Qué impacto tiene el uso de `git mergetool` en un entorno de trabajo ágil con CI/CD, y cómo aseguras que todos los miembros del equipo mantengan consistencia en las resoluciones?

Configuraría `git mergetool` mediante `git config --global merge.tool [herramienta]` y documentaría estas configuraciones en el repositorio. Las herramientas visuales aceleran la resolución de conflictos en entornos ágiles al proporcionar contexto visual para tomar decisiones más informadas. Para mantener consistencia en el equipo, establecería estándares documentados, organizaría sesiones colaborativas para conflictos complejos e implementaría revisiones post-fusión para verificar la coherencia del código resultante.


    
5. **Ejercicio para git reset**
    
    **Contexto**: En un proyecto ágil, un desarrollador ha hecho un commit que rompe la pipeline de CI/CD. Se debe revertir el commit, pero se necesita hacerlo de manera que se mantenga el código en el directorio de trabajo sin deshacer los cambios.
    
    **Pregunta**:  
    Explica las diferencias entre `git reset --soft`, `git reset --mixed` y `git reset --hard`. ¿En qué escenarios dentro de un flujo de trabajo ágil con CI/CD utilizarías cada uno? Describe un caso en el que usarías `git reset --mixed` para corregir un commit sin perder los cambios no commiteados y cómo afecta esto a la pipeline.

Los tres modos de `git reset` tienen propósitos específicos: `--soft` deshace el commit manteniendo cambios en staging; `--mixed` deshace el commit dejando cambios en el directorio sin staging; `--hard` elimina tanto el commit como los cambios. En un flujo CI/CD, usaría `--mixed` para corregir un commit problemático conservando los cambios para refinarlos (por ejemplo, dividiendo un commit grande en varios más pequeños), sin interrumpir el pipeline mientras continúo trabajando en la solución óptima.
    
6. **Ejercicio para git revert**
    
    **Contexto**: En un entorno de CI/CD, tu equipo ha desplegado una característica a producción, pero se ha detectado un bug crítico. La rama principal debe revertirse para restaurar la estabilidad, pero no puedes modificar el historial de commits debido a las políticas del equipo.
    
    **Pregunta**:  
    Explica cómo utilizarías `git revert` para deshacer los cambios sin modificar el historial de commits. ¿Cómo te aseguras de que esta acción no afecte la pipeline de CI/CD y permita una rápida recuperación del sistema? Proporciona un ejemplo detallado de cómo revertirías varios commits consecutivos.

Para revertir sin modificar el historial, ejecutaría `git revert [commit-hash]` creando un nuevo commit que neutraliza los cambios problemáticos. Para múltiples commits consecutivos, usaría `git revert más-reciente..más-antiguo` en orden inverso para evitar conflictos. Este enfoque preserva la transparencia del historial y permite seguimiento completo. Para minimizar el impacto en CI/CD, ejecutaría pruebas completas sobre el commit de reversión y configuraría alertas para notificar al equipo sobre la acción realizada.
    
7. **Ejercicio para git stash**
    
    **Contexto**: En un entorno ágil, tu equipo está trabajando en una corrección de errores urgente mientras tienes cambios no guardados en tu directorio de trabajo que aún no están listos para ser committeados. Sin embargo, necesitas cambiar rápidamente a una rama de hotfix para trabajar en la corrección.
    
    **Pregunta**:  
    Explica cómo utilizarías `git stash` para guardar temporalmente tus cambios y volver a ellos después de haber terminado el hotfix. ¿Qué impacto tiene el uso de `git stash` en un flujo de trabajo ágil con CI/CD cuando trabajas en múltiples tareas? ¿Cómo podrías automatizar el proceso de _stashing_ dentro de una pipeline CI/CD?

Utilizaría `git stash save "descripción"` para guardar temporalmente mis cambios, cambiaría a la rama de hotfix, resolvería el problema urgente y luego recuperaría mi trabajo con `git stash pop`. Esta técnica mantiene un flujo ágil al permitir cambios de contexto sin commits prematuros. Para optimizar el proceso en CI/CD, integraría scripts pre-commit que detecten cambios de rama y ofrezcan stashing automático, con notificaciones en el sistema sobre stashes pendientes para evitar trabajo olvidado.

    
8. **Ejercicio para .gitignore**
    
    **Contexto**: Tu equipo de desarrollo ágil está trabajando en varios entornos locales con configuraciones diferentes (archivos de logs, configuraciones personales). Estos archivos no deberían ser parte del control de versiones para evitar confusiones en la pipeline de CI/CD.
    
    **Pregunta**:  
    Diseña un archivo `.gitignore` que excluya archivos innecesarios en un entorno ágil de desarrollo. Explica por qué es importante mantener este archivo actualizado en un equipo colaborativo que utiliza CI/CD y cómo afecta la calidad y limpieza del código compartido en el repositorio.

Un `.gitignore` efectivo incluiría patrones para archivos de configuración local, directorios de dependencias, archivos de build, logs, datos temporales, configuraciones IDE y credenciales. Mantenerlo actualizado es crucial en equipos con CI/CD para evitar interferencias entre configuraciones de desarrolladores, prevenir exposición de información sensible, reducir el tamaño del repositorio y acelerar operaciones del pipeline al evitar procesar archivos innecesarios, minimizando también los conflictos en archivos generados automáticamente.

#### **Ejercicios adicionales**

##### **Ejercicio 1: Resolución de conflictos en un entorno ágil**

**Contexto:**  
Estás trabajando en un proyecto ágil donde múltiples desarrolladores están enviando cambios a la rama principal cada día. Durante una integración continua, se detectan conflictos de fusión entre las ramas de dos equipos que están trabajando en dos funcionalidades críticas. Ambos equipos han modificado el mismo archivo de configuración del proyecto.

**Pregunta:**

- ¿Cómo gestionarías la resolución de este conflicto de manera eficiente utilizando Git y manteniendo la entrega continua sin interrupciones? ¿Qué pasos seguirías para minimizar el impacto en la CI/CD y asegurar que el código final sea estable?

Para gestionar eficientemente este conflicto manteniéndola la CI/CD operativa, primero crearía una rama temporal (`conflict-resolution`) específica para resolver el conflicto sin afectar la rama principal. Convocaría inmediatamente a ambos equipos para una reunión corta donde analizar el conflicto y definir qué configuraciones tienen prioridad según el impacto técnico y de negocio. Luego, con representantes de ambos equipos, resolvería el conflicto en la rama temporal utilizando herramientas visuales como `git mergetool`, ejecutaría las pruebas automatizadas completas antes de fusionar la resolución a `main`, y finalmente documentaría la decisión para referencia futura. 

##### **Ejercicio 2: Rebase vs. Merge en integraciones ágiles**

**Contexto:**  
En tu equipo de desarrollo ágil, cada sprint incluye la integración de varias ramas de características. Algunos miembros del equipo prefieren realizar merge para mantener el historial completo de commits, mientras que otros prefieren rebase para mantener un historial lineal.

**Pregunta:**

- ¿Qué ventajas y desventajas presenta cada enfoque (merge vs. rebase) en el contexto de la metodología ágil? ¿Cómo impacta esto en la revisión de código, CI/CD, y en la identificación rápida de errores?

En un contexto ágil, el merge preserva la cronología completa del desarrollo con ramificaciones explícitas (facilita el seguimiento de historias de usuario completas) pero complica el historial con commits de merge redundantes, dificultando encontrar cambios específicos. El rebase ofrece un historial lineal limpio que simplifica la revisión de código y el uso de herramientas como bisect para detectar bugs, pero reescribe la historia (problemático en ramas compartidas) y oculta el desarrollo paralelo real. Para CI/CD, merge facilita la trazabilidad pero puede complicar pipelines, mientras que rebase permite flujo lineal óptimo para integración continua pero requiere mayor disciplina del equipo y puede complicar la resolución de conflictos en cambios extensos.
##### **Ejercicio 3: Git Hooks en un flujo de trabajo CI/CD ágil**

**Contexto:**  
Tu equipo está utilizando Git y una pipeline de CI/CD que incluye tests unitarios, integración continua y despliegues automatizados. Sin embargo, algunos desarrolladores accidentalmente comiten código que no pasa los tests locales o no sigue las convenciones de estilo definidas por el equipo.

**Pregunta:**

- Diseña un conjunto de Git Hooks que ayudaría a mitigar estos problemas, integrando validaciones de estilo y tests automáticos antes de permitir los commits. Explica qué tipo de validaciones implementarías y cómo se relaciona esto con la calidad del código y la entrega continua en un entorno ágil.

Implementaría un sistema de Git Hooks que incluye: 1) `pre-commit` para ejecutar linters automáticos (ESLint/Prettier para JS, Black para Python) que verifiquen y corrijan problemas de formato y estilo; 2) `pre-push` para ejecutar tests unitarios rápidos garantizando que solo código funcional llegue al repositorio remoto; y 3) `commit-msg` para validar que los mensajes de commit sigan convenciones establecidas (conventional commits) facilitando la generación automática de changelogs.
##### **Ejercicio 4: Estrategias de branching en metodologías ágiles**

**Contexto:**  
Tu equipo de desarrollo sigue una metodología ágil y está utilizando Git Flow para gestionar el ciclo de vida de las ramas. Sin embargo, a medida que el equipo ha crecido, la gestión de las ramas se ha vuelto más compleja, lo que ha provocado retrasos en la integración y conflictos de fusión frecuentes.

**Pregunta:**

- Explica cómo adaptarías o modificarías la estrategia de branching para optimizar el flujo de trabajo del equipo en un entorno ágil y con integración continua. Considera cómo podrías integrar feature branches, release branches y hotfix branches de manera que apoyen la entrega continua y minimicen conflictos.

Optimizaría el enfoque de branching migrando de Git Flow completo a un modelo Trunk-Based simplificado donde `main` contendría siempre código estable y listo para producción. Implementaría: 1) Feature flags para integrar código incompleto a `main` pero desactivado en producción; 2) Short-lived feature branches (máximo 1-2 días) con integración frecuente para reducir conflictos; 3) Una única rama `release` temporal para preparar despliegues con etiquetas (tags) para versiones específicas; y 4) Hotfix directamente sobre `main` con despliegue inmediato tras validación. 

##### **Ejercicio 5: Automatización de reversiones con git en CI/CD**

**Contexto:**  
Durante una integración continua en tu pipeline de CI/CD, se detecta un bug crítico después de haber fusionado varios commits a la rama principal. El equipo necesita revertir los cambios rápidamente para mantener la estabilidad del sistema.

**Pregunta:**

- ¿Cómo diseñarías un proceso automatizado con Git y CI/CD que permita revertir cambios de manera eficiente y segura? Describe cómo podrías integrar comandos como `git revert` o `git reset` en la pipeline y cuáles serían los pasos para garantizar que los bugs se reviertan sin afectar el desarrollo en curso.

Diseñaría un proceso automatizado de "reversión segura" integrando: 1) Un job específico en el pipeline que monitoree métricas críticas post-despliegue (tasas de error, latencia, uso de CPU); 2) Capacidad de activar automáticamente una reversión si se superan umbrales predefinidos; 3) Script automatizado que ejecute `git revert -m 1 <commit-hash>` para crear un commit de reversión limpio preservando el historial; 4) Notificación instantánea al equipo sobre la reversión con detalles del problema; y 5) Creación automática de una rama temporal con los cambios revertidos para que el equipo pueda corregir sin presión mientras el sistema principal se mantiene estable. 