# Actividad 3

## A. Cuestionario
### Motivaciones para la nube

#### (a) ¿Qué problemas o limitaciones existían antes del surgimiento de la computación en la nube y cómo los solucionó la centralización de servidores en data centers?

Existia del problema de la dependencia de hardware y servidores físicos, estos estaban restringidos por el tamaño del espacio físico donde se almacenaba el hardware lo cual limitaba mucho a las empresas en su crecimiento y escalabilidad ademas un gran problema tambien estaba en la optimizacion, mantenimiento y manipulacion de estos.

La centralización de servidores soluciono estos problemas siendo que agrupar estos recursos, red y almacenamiento para crear un recurso central lo hace mas flexible para poder reasignar los recursos en función de las necesidades requeridas, además de que las empresas ya no tienen que preocuparse por el mantenimiento  de los servidores dejando esto para los proveedores de nube.

#### (b) ¿Por qué se habla de “The Power Wall” y cómo influyó la aparición de procesadores multi-core en la evolución hacia la nube?

Se habla de The Power Wall como la limitacion que tenian los procesadores para aumentar su velocidad debido a limitaciones de consumo de energia, de disipacion del calor y limitaciones fisicas.  
Para poder superar estas limitaciones en los procesadores es que se empezaron a crear los procesadores multi nucleo el cual mejoro el rendimiento sin tener que aumentar la frecuencia de reloj del nucleo en ves de eso se distribuia la carga entre los diferentes nucleos.  
La influencia de los procesadores multi-core en la evolucion hacia la nube fue grande pues facilitiba el procesamiento en paralelo lo cual es fundamental para la infraestructura de la nube, la virtualizacion tambie se hizo mas practica y eficiente con una posibilidad de ejecutar multples instancias de maquinas virtuales o contenedores en un unico servidor fisico, asu vez hay un mayor rendimiento con un menor consumo de energia por que los procesadores multi nucleo permiten aumentar la cantidad de trabajo sin aumentar proporcionalmente el consumo de energia.

### Clusters y load balancing

#### (a) Explica cómo la necesidad de atender grandes volúmenes de tráfico en sitios web condujo a la adopción de clústeres y balanceadores de carga.

Para poder manejar de mejor la menera la alta demanda de usuarios asi como picos de usuarios en algunas temporadas  los clusters y los balanceadores de carga se empezaron, pues  ayuda a distribuir la carga de trabajo entre múltiples recursos, lo que reduce la carga en cada recurso de la aplicación y mejora el rendimiento general del sistema,a su vez tambien permite una facil escalabilidad hacia arriba y hacia abajo según las necesidades del momento, además los balanceadores de carga brindan una capa adicional de protección contra ataques DDoS de red y aplicaciones y protegen las aplicaciones de solicitudes maliciosas,tambien garantiza que no haya un único punto de falla en el sistema, lo que proporciona una alta disponibilidad y tolerancia a fallas para manejar las fallas del servidor de aplicaciones y en casos en los que es necesario mantener la conexión del usuario con el mismo servidor durante toda su sesión. El balanceador de carga puede configurarse para asignar una sesión persistente a un servidor específico, asegurando la continuidad de la experiencia del usuario.

#### (b) Describe un ejemplo práctico de cómo un desarrollador de software puede beneficiarse del uso de load balancers para una aplicación web.

Un desarrollador que tiene una aplicación que tiene una alta demanda de usuarios  puede servirle para poder distribuir las peticiones en diferentes instancias de la aplicación y servidores para poder tener un mejor rendimiento y evitar caídas de los servidores por el altro trafico.

Tambien en caso de que un desarrollador quiera lanzar una aplicacion web la cual sera utilizada en diferentes regiones del mundo, el uso de load balancers va a ser crucial para poder redirigir el trafico de usuarios de cada region a un servidor con una instancia de la aplicación que tenga mejor rendimiento para ese usuario ya sea por la cercania al servidor o que presenta mejor rendimiento con cierto servidor que tenga cerca.

### Elastic computing

#### (a) Define con tus propias palabras el concepto de Elastic Computing.

El Elastic Computing hace referencia a la capacidad de un sistema de adquirir dinamicamente recursos informáticos como almacenamiento y memoria, escalando hacia arriba o hacia abajo dependiendo de la necesidad del sistema y soportar una carga de trabajo variable, para lograr esto lo que se hace es normalmente apagar los nodos que no se estan usando y encenderlos cuando estos sean requeridos.

#### (b) ¿Por qué la virtualización es una pieza clave para la elasticidad en la nube?

La virtualizacion juega un papel clave en la elasticidad en la nube pues permite un uso eficiente de los recursos fisicos de hardware pues permite crear multiples instancias de maquinas virtuales o contenedores haciendo que un solo servidor puede alojar multiples servidores virtuales, en escalabilidad con la virtualizacion los sistemas pueden escalar tanto como arriba como hacia abajo segun la demanda de recursos, la virtualizacion permite tambien un aislamiento entre todas instancias virtuales asegurando que cada carga de trabajo trabaje sin interferencia de las otras haciendola asi mas segura y estable, la flexibilidad es una caracteristica que tambien se da gracias a la virtualizacion pues se puede implementar diferente sistemas operativos, maquinas virtuales o contenedores adaptándose asi a requisitos fisicos, tambien al permitir multiples instancias de servidores virtuales en uno fisico reduce los costos y la cantidad de servidores fisicos necesarios.

#### (c) Menciona un escenario donde, desde la perspectiva de desarrollo, sería muy difícil escalar la infraestructura sin un entorno elástico.

Un ejemplo seria un Eccomerce que en fechas como navidad o celebraciones especiales la demanda se multiplique por muchas veces y al no tener escalabilidad la pagina podria presentar fallos o lentitud para los usuarios haciendo que se pierdan muchos posibles clientes lo cual facilmente podria evitarse con un entorno elastico pues este nos daria los recursos que necesitamos para esos momentos de mayor demanda.

### Modelos de servicio (IaaS, PaaS, SaaS, DaaS)

#### (a) Diferencia cada uno de estos modelos. ¿En qué casos un desarrollador optaría por PaaS en lugar de IaaS?

Un desarrollador podría optar por PaaS sobre IaaS cuando necesita centrarse en el desarrollo y no en la gestión de infraestructura. Además puede requerir un rápido despliegue y escalabilidad automática la cuál podría obtenerla de manera más rápida con PaaS. También se puede tomar en consideración que esta elección puede incluir una reducción de costos operativos de administración de servidores  
Por ejemplo Shopify es el SaaS más conocido para ecommerce los cuales permiten a personas sin conocimiento técnico poder tener su propia web de maneraintuitiva ofreciendo servicios de hosting y dominio. En sus inicios utilizaron PaaS, siendo específicos Heroku para momentos de alta demanda como fechas de black friday. Esta elección se dio dado que como estaban empezando lo importante era concentrarse en la funcionalidad sobre la infraestructura. Sin embargo hoy en día ya cuentan con Infraestructura propia dado que escalaron muy rápido y tienen alta demanda.

#### (b) Enumera tres ejemplos concretos de proveedores o herramientas que correspondan a cada tipo de servicio.

**IaaS:**

- AWS EC2: Servidores virtuales escalables en la nube de Amazon
- Google Compute Engine: Máquinas virtuales de alto rendimiento en infraestructura de Google
- Microsoft Azure Virtual Machines: Recursos computacionales personalizables en la nube de Microsoft

**PaaS:**

- Heroku: Plataforma basada en contenedores para despliegue y gestión de aplicaciones web
- Google App Engine: Servicio para desarrollo y alojamiento de aplicaciones web sin gestión de servidores
- Microsoft Azure App Service: Plataforma para crear y desplegar aplicaciones web y APIs

**SaaS:**

- Salesforce: CRM y plataforma de gestión de relaciones con clientes basada en la nube
- Microsoft 365: Suite de productividad, comunicación y colaboración empresarial
- Google Workspace: Conjunto de herramientas de colaboración y productividad en línea

**DaaS:**

- Snowflake: Almacén de datos en la nube con arquitectura separada de computación y almacenamiento
- MongoDB Atlas: Servicio de base de datos NoSQL totalmente gestionado
- Amazon RDS: Servicio de bases de datos relacionales gestionado que simplifica la administración

### Tipos de nubes (Pública, Privada, Híbrida, Multi-Cloud)

#### (a) ¿Cuáles son las ventajas de implementar una nube privada para una organización grande?

Las nubes privadas proporcionan a organizaciones grandes control total sobre su infraestructura, permitiendo cumplimiento estricto con requisitos regulatorios sectoriales específicos (HIPAA, PCI DSS, GDPR) mediante aislamiento físico de recursos. Ofrecen mayor personalización para cargas de trabajo especializadas con requisitos específicos de rendimiento, además de predictibilidad de costos a largo plazo sin variaciones por consumo como en nubes públicas. La seguridad mejorada a través de perímetros definidos, VLANs dedicadas y configuraciones personalizadas de hardware reduce la superficie de ataque, mientras que el control sobre la ubicación física de los datos ayuda a cumplir requisitos de soberanía de datos y residencia geográfica específica.

#### (b) ¿Por qué una empresa podría verse afectada por el “provider lock-in”?

Una empresa puede verse afectada por el "provider lock-in" cuando sus aplicaciones, datos y procesos dependen excesivamente de servicios propietarios específicos de un proveedor cloud, imposibilitando la migración sin refactorización significativa. Los costos de salida se vuelven prohibitivos debido a tarifas de transferencia de datos, incompatibilidades entre APIs propietarias, y dependencia de servicios gestionados sin equivalentes directos en otras plataformas. A nivel arquitectónico, las aplicaciones suelen evolucionar aprovechando características específicas del proveedor (como Lambda en AWS o BigQuery en GCP), creando dependencias técnicas que requieren reescritura sustancial para migrar, mientras que los contratos comerciales frecuentemente incluyen descuentos por compromiso de uso que penalizan la diversificación, obligando a las empresas a permanecer con un proveedor aunque surjan alternativas más eficientes o económicas.

#### (c) ¿Qué rol juegan los “hyperscalers” en el ecosistema de la nube?

Los hyperscalers (AWS, Microsoft Azure, Google Cloud) actúan como motores de innovación tecnológica en el ecosistema cloud, estableciendo estándares de facto para arquitecturas cloud-native y prácticas operacionales mientras definen la economía de escala del sector. Su capacidad para desplegar infraestructura masiva globalmente permite entregar fiabilidad y rendimiento consistentes a nivel mundial, sosteniendo tecnologías emergentes como IA/ML, IoT y edge computing mediante inversiones multimillonarias en investigación. Además, forman el núcleo de la economía digital moderna al proporcionar plataformas donde operan la mayoría de las aplicaciones SaaS, creando ecosistemas completos de servicios interconectados con marketplaces de terceros y programas de partners que facilitan la distribución global de soluciones tecnológicas, desde startups hasta corporaciones multinacionales.

## B. Actividades de investigación y aplicación
### Estudio de casos

Busca dos o tres casos de empresas (startups o grandes organizaciones) que hayan migrado parte de su infraestructura a la nube. Describe:
- Sus motivaciones para la migración.
- Los beneficios obtenidos (por ejemplo, reducción de costos, escalabilidad, flexibilidad).
- Los desafíos o dificultades enfrentadas (ej. seguridad, cumplimiento normativo).

### Comparativa de modelos de servicio

#### Caso 1: Netflix

**Motivaciones para la migración**

- Limitaciones de escalabilidad en sus centros de datos propios
- Frecuentes interrupciones del servicio por fallos en hardware
- Necesidad de expansión internacional rápida
- Demanda creciente de streaming que requería infraestructura flexible

**Beneficios obtenidos**

- Escalabilidad masiva para soportar millones de transmisiones simultáneas
- Mayor resiliencia con arquitectura distribuida en múltiples regiones
- Reducción de costos operativos a largo plazo
- Capacidad para innovar más rápidamente con nuevas características
- Mejor experiencia de usuario con menor latencia global

**Desafíos enfrentados**

- Migración de enormes volúmenes de datos sin interrumpir el servicio
- Rediseño de aplicaciones para arquitectura nativa en la nube
- Gestión de costos variables en AWS
- Implementación de nuevos protocolos de seguridad para contenido protegido por derechos
- Cumplimiento de regulaciones de privacidad en diferentes regiones geográficas

#### Caso 2: Capital One

**Motivaciones para la migración**

- Reducir dependencia de centros de datos heredados costosos
- Necesidad de mayor agilidad para competir con fintechs
- Mejorar capacidades de análisis de datos y personalización
- Modernizar la arquitectura de TI para innovación continua

**Beneficios obtenidos**

- Reducción del 40% en costos de infraestructura
- Tiempo de desarrollo reducido de meses a semanas
- Mejor análisis de datos para detección de fraude y personalización
- Mayor resiliencia ante picos de demanda (temporadas fiscales)
- Capacidades mejoradas de recuperación ante desastres

**Desafíos enfrentados**

- Estrictos requisitos regulatorios del sector financiero
- Necesidad de garantizar seguridad de datos sensibles de clientes
- Resistencia interna al cambio organizacional
- Reentrenamiento significativo del personal técnico
- Integración compleja con sistemas bancarios heredados

#### Caso 3: Spotify

**Motivaciones para la migración**

- Crecimiento exponencial de usuarios y contenido de audio
- Limitaciones de su infraestructura para soportar personalización avanzada
- Necesidad de análisis de datos más sofisticados
- Expansión internacional rápida

**Beneficios obtenidos**

- Capacidad para escalar a más de 400 millones de usuarios
- Implementación de recomendaciones personalizadas en tiempo real
- Flexibilidad para experimentar con nuevas características
- Reducción de latencia en reproducción de audio
- Mayor velocidad de despliegue de actualizaciones

**Desafíos enfrentados**

- Mantenimiento de experiencia consistente durante la migración
- Gestión de transferencia de enormes bibliotecas de música
- Balanceo entre servicios de varios proveedores (Google Cloud y AWS)
- Adaptación a diferentes legislaciones de privacidad por región
- Desarrollo de nuevas habilidades en equipos de ingeniería

## 2. Comparativa de modelos de servicio
Realiza un cuadro comparativo en el que muestres las responsabilidades del desarrollador, del proveedor y del equipo de operaciones en los distintos modelos (IaaS, PaaS, SaaS). Incluye aspectos como: instalación de S.O., despliegue de aplicaciones, escalado automático, parches de seguridad, etc.

**Dev**: Equipo de Desarrolladores  
**Ops**: Equipo de Operaciones  
**Proveedor**

![](https://i.imgur.com/jM7FjcT.png)

## 3. Armar una estrategia multi-cloud o híbrida

Imagina que trabajas en una empresa mediana que tiene una parte de su infraestructura en un data center propio y otra parte en un proveedor de nube pública.

Diseña una estrategia (de forma teórica) para migrar el 50% de tus cargas de trabajo a un segundo proveedor de nube, con el fin de no depender exclusivamente de uno.

Explica dónde iría la base de datos, cómo manejarías la configuración de red y cuál sería el plan de contingencia si un proveedor falla.

### Respuesta:

Para implementar una estrategia multi-cloud identificamos qué cargas de trabajo pueden migrar a un segundo proveedor de nube para distribuir el 50% de la carga. Los datos críticos se mantienen en el data center propio para asegurar el máximo control, mientras que los datos no críticos se distribuyen entre las nubes públicas, en este caso, escogimos AWS y Azure, almacenando backups de los datos críticos en modo solo lectura en ambas nubes para garantizar redundancia.

Para migrar el 50% de la carga de trabajo, en AWS aprovechamos servicios de microservicios y procesamiento de pagos con AWS App Runner, mientras que en Azure usamos Azure App Service para gestionar APIs y manejo de usuarios.

La conectividad entre la nube privada y AWS se realiza mediante AWS Direct Connect, mientras que con Azure se logra a través de Azure ExpressRoute. La conexión entre las nubes públicas se establece mediante una VPN segura entre AWS Transit Gateway y Azure VPN Gateway, garantizando un tráfico seguro.

En caso de falla de AWS, redirigimos el tráfico hacia Azure usando un balanceador de carga global, utilizando la réplica de la base de datos en Azure para mantener la disponibilidad. Si Azure falla, el tráfico se redirige a AWS, aprovechando la réplica en RDS. Al no depender de un solo proveedor, esta estrategia permite migrar servicios según conveniencia, garantizando alta disponibilidad y continuidad operativa.

![](https://i.imgur.com/RLobnOl.png)

## 4. Debate sobre costos
Prepara un breve análisis de los pros y contras de cada tipo de nube (pública, privada, híbrida, multi-cloud) considerando:
- Costos iniciales (CAPEX vs. OPEX).
- Flexibilidad y escalabilidad a mediano y largo plazo.
- Cumplimiento con normativas (p.ej. GDPR, HIPAA).
- Barreras o complejidades al cambiar de proveedor.

### Definiciones Previas
**Capital Expenditures**: Gasto en la inversión a largo plazo en activos físicos o recursos que proporcionarán beneficios a la empresa durante varios años.  
**Operational Expenditures**: Gasto en las operaciones actividades diarias de la empresa para mantener su funcionamiento.  
**GDPR**: General Data Protection Regulation  
**HIPAA**: Health Insurance Portability and Accountability Act

![](https://i.imgur.com/fOnMz58.png)

![](https://i.imgur.com/FcNk6Yb.png)

## C. Ejercicio de presentación de "mini-proyecto"
Como parte del aprendizaje práctico, forma equipos y presenten un "Mini-proyecto de arquitectura en la nube":

### Objetivo del sistema:
Cada equipo define brevemente la aplicación o servicio (por ejemplo, un e-commerce, un sistema de reservas, una plataforma de contenido).

Nuestra plataforma está dedicada a la venta de accesorios de moda para mujeres, ofreciendo una amplia variedad de productos que incluyen joyería, bolsos, gafas de sol y otros complementos. Nos enfocamos en brindar una experiencia de compra rápida y segura, facilitando el pago con múltiples métodos, incluyendo tarjetas de crédito/débito y PayPal. El e-commerce tiene un tráfico promedio de 50 a 300 visitas diarias, con un aumento considerable durante los fines de semana. Sin embargo, en eventos especiales como Black Friday, Día de la Mujer y otros eventos relevantes, el número de visitas puede dispararse significativamente. Aunque el mercado objetivo principal es América Latina, queremos que la plataforma esté disponible en otras regiones del mundo a medida que aumente la demanda. Como es un proyecto que está comenzando, contamos con recursos financieros limitados, lo que nos impulsa a optimizar los costos desde el inicio.

### Selección de modelo de servicio:
Explica si se utilizará IaaS, PaaS o SaaS, y justifica por qué.

**PaaS**  
Optamos por utilizar el modelo PaaS debido a que permite al equipo de desarrollo concentrarse en el código sin preocuparse por gestionar la infraestructura. Además facilita la implementación de pipelines CI/CD para despliegues rápidos y actualizaciones. También, facilita la escalabilidad según el tráfico. Por ejemplo, podemos usar Azure App Service para alojar microservicios y Google App Engine para manejar tareas específicas como el procesamiento de pagos.

### Tipo de nube:
Decide si vas a desplegar la aplicación en una nube pública, privada, híbrida o multi-cloud. Argumenta con un análisis de ventajas y desventajas.

**Nube pública**  
Usar una nube pública nos permite optimizar costos con el pago por uso, permitiendo escalar sin una gran inversión inicial, podemos aumentar recursos según la demanda sin tener que invertir en infraestructura propia.

### Esquema de escalabilidad:
Describe cómo la aplicación escalaría en caso de aumento de demanda.

**Horizontal**  
Para eventos de alto tráfico durante el año, optamos por un escalado horizontal agregando más instancias para distribuir la carga de manera efectiva, además es más económico añadir máquinas de tamaño estándar que aumentar los recursos de una sola.

### Costos y riesgos:
Menciona los principales costos (directos o indirectos) y los riesgos asociados a tu elección (p.ej., dependencia del proveedor, requerimientos de seguridad).

**Costos**  
- Para el frontend del Ecommerce, se utilizará una instancia EC2 t3.small con 2 vCPUs y 2GB de RAM, cuyo costo es $0.0208 por hora.
- Para los microservicios del backend, cada microservicio se desplegará en una instancia EC2 t3.medium con 2 vCPUs y 4GB de RAM, cuyo costo es $0.0376 por hora.
- El almacenamiento de objetos se realizará en Amazon S3, con un costo de $0.023 por GB/mes para almacenamiento estándar y un costo adicional por solicitudes.
- Para la base de datos relacional, se utilizará Amazon Aurora con una instancia db.r5.large (2 vCPUs y 16GB de RAM), cuyo costo es $0.096 por hora.
- El servicio CDN será Amazon CloudFront, cuyo costo depende de la transferencia de datos, aproximadamente $0.085 por GB para la salida de datos. Las solicitudes se cobran a $0.0075 por cada 10,000 solicitudes.

**Riesgos**  
- **Dependencia**: Al tener dependencia de AWS para todos los servicios corremos el riesgo de estar atados al pricing  y limitaciones de AWS.
- **Bloqueo Tecnológico**: Se puede tener dificultad al querer migrar los servicios o a otro proveedor sin incurrir a grandes costos ya que AWS utiliza tecnologías y servicios propietarios.
- **Costos no previsibles**: Si de un momento a otro aumenta el tráfico en nuestro ecommerce puede hacer que los gastos se incrementen rápidamente.

**Gastos operacionales OPEX**: Pago por uso de nube.

![](https://i.imgur.com/xL5H7MO.png)

En este diagrama tenemos 4 partes:

1. **Usuario**: Es el punto de acceso donde los clientes interactúan con la página web.

2. **Entrada**:
   - **Amazon CloudFront (CDN)** se utiliza para distribuir contenido estático (imágenes de productos, etc) a los usuarios de modo que tiene baja latencia.
   - **Api Gateway** es un servicio de AWS que actúa como el punto único de entrada para todas las solicitudes y necesidades del cliente. Este distribuye el tráfico entre los microservicios.

3. **Microservicios**:
   La Api Gateway es responsable de enrutar las solicitudes a cada microservicio según sea necesario para la ecommerce. Cada uno es gestionado de manera independiente.
   Estos son contenedores que se encargan de funciones específicas.

4. **Persistencia**:
   - **Amazon Aurora** es una base de datos relacional que es gestionada y ofrece alta escalabilidad. Se utiliza para almacenar información crítica como los usuarios, transacciones, inventarios, etc.
   - **Amazon S3** se usa para almacenar archivos estáticos no estructurados, como imágenes de productos, archivos multimedia, etc. Responde a las solicitudes de acceso a contenido estático como imágenes o documentos cuando se requiera.
