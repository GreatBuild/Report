## 4.3. ADD Iterations

### 4.3.1. Iteration 1: Definición del Core Arquitectónico de ClearCost

#### 4.3.1.1. Architectural Design Backlog 1

En este backlog, nos enfocaremos en desarrollar y detallar las características arquitectónicas clave que sustentarán el éxito y la sostenibilidad de **ClearCost**. Esto incluirá elementos críticos como la **Seguridad**, para proteger los datos financieros y de los proyectos; la **Disponibilidad**, para garantizar que los equipos puedan operar sin interrupciones; y la **Mantenibilidad**, para permitir que el sistema evolucione rápidamente según las necesidades del negocio. A través de historias de usuario, tareas específicas y criterios de aceptación, este backlog establecerá la hoja de ruta para el desarrollo arquitectónico de ClearCost.

---

#### **Seguridad**

* **Historias de Usuario (User Stories):**
    * Como **Contratista**, quiero que los datos financieros de mis proyectos estén protegidos para mantener la confidencialidad frente a mis clientes y competidores.
    * Como **Entidad Contratante**, necesito tener la certeza de que solo las personas autorizadas pueden ver y modificar la información de mi proyecto para sentirme seguro al usar la aplicación.

* **Tareas:**
    * Implementar autenticación centralizada utilizando un proveedor de identidad externo (ej. Auth0 o Azure AD) mediante el protocolo OIDC.
    * Utilizar un **API Gateway** como punto único de entrada para validar los tokens JWT en cada petición, denegando el acceso a peticiones no autorizadas.
    * Implementar cifrado de datos sensibles (contratos, datos financieros) tanto en tránsito (HTTPS) como en reposo.
    * Implementar un sistema de logging que registre todos los intentos de acceso, exitosos y fallidos, para auditoría.

* **Criterios de Aceptación:**
    * Las pruebas de penetración no deben revelar vulnerabilidades críticas antes del lanzamiento.
    * Cumplimiento con la Ley de Protección de Datos Personales de Perú (Ley N.º 29733).
    * El 100% de las operaciones sensibles deben ser registradas en el log de auditoría.

---

#### **Disponibilidad**

* **Historias de Usuario (User Stories):**
    * Como **Especialista de Área**, quiero que el servicio esté disponible el 99.5% del tiempo durante mi horario laboral, independientemente de fallos puntuales en otros módulos.
    * Como **Contratista**, necesito que la plataforma se recupere rápidamente de fallos para minimizar el tiempo de inactividad y no afectar el cronograma del proyecto.

* **Tareas:**
    * Implementar **replicación de servicios críticos** (ej. Project Service, Finance Service) en múltiples zonas de disponibilidad en Azure.
    * Establecer **políticas de failover automáticas** y *health checks* para que el orquestador (ej. Kubernetes) reinicie instancias caídas sin intervención manual.
    * Aplicar el patrón **Circuit Breaker** en las llamadas entre servicios para evitar que la falla de un microservicio (ej. Notificaciones) cause una falla en cascada en los servicios que dependen de él.
    * Utilizar **comunicación asíncrona** con un *message broker* para operaciones no críticas, de modo que si un servicio consumidor no está disponible, el mensaje quede en cola hasta que se recupere.

* **Criterios de Aceptación:**
    * Redundancia demostrada en todos los componentes críticos del sistema (API Gateway, microservicios clave, bases de datos).
    * El sistema cumple con el **SLA objetivo del 99.5%** medido mensualmente.
    * Pruebas de recuperación ante desastres (failover) demuestran que el sistema se recupera dentro del RTO establecido de 2 horas.

---

#### **Mantenibilidad (Modificabilidad)**

* **Historias de Usuario (User Stories):**
    * Como **Developer** del equipo de GreatBuild, quiero poder modificar la lógica de un dominio de negocio (ej. Finanzas) sin afectar a otros dominios (ej. Proyectos) para entregar nuevas funcionalidades más rápido.
    * Como **Arquitecto**, necesito que la arquitectura permita que diferentes equipos trabajen en paralelo sobre distintos módulos para escalar la capacidad de desarrollo.

* **Tareas:**
    * Diseñar la arquitectura siguiendo un estilo de **Microservicios**, donde cada servicio se alinee con un **Bounded Context** de DDD (ej. `FinanceService`, `ProjectService`).
    * Implementar el patrón **Database per Service**, asegurando que cada microservicio gestione su propia base de datos para minimizar el acoplamiento.
    * Definir **contratos de API versionados** y claros (usando OpenAPI) para la comunicación entre servicios, asegurando que los cambios sean predecibles.
    * Crear una **pipeline de CI/CD** que permita a cada equipo desplegar su microservicio de forma independiente y automatizada.

* **Criterios de Aceptación:**
    * Se demuestra que un cambio en la lógica de cálculo de costos (dentro del `FinanceService`) se puede implementar y desplegar en **menos de 4 horas** sin necesidad de redesplegar otros servicios.
    * Las interfaces entre microservicios están documentadas y no presentan acoplamiento a nivel de base de datos.
    * Cada microservicio puede ser desplegado de forma independiente en un entorno de pruebas.

#### 4.3.1.2. Establish Iteration Goal by Selecting Drivers

En esta iteración, se seleccionarán los drivers clave para establecer metas y objetivos concretos que garanticen la efectividad, seguridad y evolución de la plataforma **ClearCost**. Las metas se definirán a partir de los pilares de **Seguridad**, **Disponibilidad** y **Mantenibilidad**, identificados como fundamentales en el *Architectural Design Backlog* para cumplir con las expectativas de los usuarios y los objetivos de negocio de GreatBuild.

---

##### **Meta de Seguridad**

* **Objetivo:** Fortalecer la infraestructura de seguridad de ClearCost para proteger la integridad de los datos financieros y de los proyectos, así como las transacciones dentro de la plataforma, generando confianza en todos los actores.
* **Acciones Clave:**
  * Implementar autenticación centralizada para todos los usuarios, integrando un proveedor de identidad externo (Azure AD).
  * Aplicar cifrado robusto para los datos sensibles tanto en tránsito (HTTPS) como en reposo (bases de datos y almacenamiento de archivos).
  * Establecer un sistema de logging y auditoría para registrar las operaciones críticas y los intentos de acceso.

---

##### **Meta de Alta Disponibilidad**

* **Objetivo:** Mantener la disponibilidad continua del servicio ClearCost, asegurando una mínima interrupción incluso durante fallos para que los equipos de construcción puedan operar sin impedimentos.
* **Acciones Clave:**
  * Implementar replicación de los servicios críticos en múltiples zonas de disponibilidad.
  * Establecer y probar políticas de *failover* automáticas para asegurar una rápida recuperación ante fallos.
  * Utilizar patrones de resiliencia como *Circuit Breaker* para evitar fallos en cascada entre microservicios.

---

##### **Meta de Mantenibilidad (Modificabilidad)**

* **Objetivo:** Diseñar una arquitectura que permita una evolución rápida y desacoplada del sistema, facilitando que los equipos de desarrollo puedan entregar nuevas funcionalidades de manera eficiente y en paralelo.
* **Acciones Clave:**
  * Diseñar los servicios basándose en los **Bounded Contexts** definidos (Finanzas, Proyectos, Colaboración, Identidad y Accesos).
  * Implementar el patrón **Database per Service** para garantizar la autonomía de cada microservicio.
  * Establecer contratos de API claros y versionados para asegurar una comunicación predecible entre los servicios.

---

##### **Objetivo de la Iteración**

* **Seguridad:** El objetivo es robustecer la protección mediante la implementación de autenticación centralizada y el cifrado de datos sensibles, garantizando así la seguridad integral de la información y la confidencialidad de los proyectos.
* **Alta Disponibilidad:** El objetivo es asegurar una operatividad continua con mínimas interrupciones, implementando sistemas de replicación de servicios y políticas de *failover* efectivas para una rápida recuperación ante fallos.
* **Mantenibilidad:** Nos proponemos diseñar una arquitectura de microservicios alineada con los dominios del negocio que facilite la evolución del sistema y la entrega continua de valor. Esto se logrará mediante la implementación de límites claros entre servicios y bases de datos independientes.

#### 4.3.1.3. Choose One or More Elements of the System to Refine

Para continuar con el proceso de desarrollo de **ClearCost**, y basándonos en los objetivos de la iteración y los drivers previamente establecidos, el siguiente paso es seleccionar uno o más elementos del sistema que requieren refinamiento. Estos elementos se eligen con el propósito de mejorar la **Seguridad**, la **Disponibilidad** y la **Mantenibilidad** de la plataforma. A continuación, se detallan los elementos seleccionados para el refinamiento:

---

* **Autenticación y Seguridad de Datos:**
  * **Elemento a Refinar:** Sistema de autenticación y mecanismos de cifrado de datos.
  * **Razón para el Refinamiento:** Asegurar que todos los aspectos de la seguridad de la información cumplan con los estándares actuales y protejan eficazmente la data financiera y contractual contra amenazas externas e internas.
  * **Esperado:** Implementación de una autenticación centralizada y robusta (integrada con Azure AD), junto con la actualización de los protocolos de cifrado para datos en reposo y en tránsito.

* **Arquitectura de Microservicios:**
  * **Elemento a Refinar:** Descomposición de la aplicación en microservicios alineados a los Bounded Contexts.
  * **Razón para el Refinamiento:** Mejorar la **mantenibilidad** y la **escalabilidad** del sistema, permitiendo que diferentes dominios funcionales (Proyectos, Finanzas, etc.) se desarrollen y desplieguen de manera independiente.
  * **Esperado:** Un diseño de microservicios bien estructurado que optimice la evolución del producto y la velocidad de entrega de nuevas funcionalidades.

* **Sistemas de Replicación y Failover:**
  * **Elemento a Refinar:** Mecanismos de replicación de servicios y políticas de *failover*.
  * **Razón para el Refinamiento:** Minimizar el tiempo de inactividad y garantizar una alta **disponibilidad** (SLA del 99.5%) incluso durante incidentes no planificados.
  * **Esperado:** Configuración de replicación en múltiples zonas de disponibilidad y pruebas de *failover* automáticas que garanticen la continuidad del servicio.

* **Comunicación entre Servicios:**
  * **Elemento a Refinar:** Diseño de la comunicación síncrona (vía API Gateway) y asíncrona (vía Message Broker).
  * **Razón para el Refinamiento:** Aumentar la resiliencia y **disponibilidad** del sistema, desacoplando los servicios para que el fallo de un componente no crítico (ej. Notificaciones) no afecte a los componentes centrales (ej. Gestión de Proyectos).
  * **Esperado:** Una implementación clara de patrones como **API Gateway** y **Comunicación Asíncrona** que asegure un sistema robusto y resiliente.

#### 4.3.1.4. Choose One or More Design Concepts That Satisfy the Selected Drivers

Tras identificar los elementos del sistema que requieren refinamiento, el siguiente paso es seleccionar los conceptos de diseño adecuados que satisfagan los drivers arquitectónicos seleccionados. Estos conceptos de diseño son esenciales para guiar el desarrollo del sistema y asegurar que los objetivos de la iteración se cumplan eficientemente. A continuación, se detallan los conceptos de diseño seleccionados para cada uno de los drivers clave:

---

#### **Seguridad**

* **Concepto de Diseño: Autenticación y Autorización Centralizada**
  * [cite_start]**Descripción:** Emplear un proveedor de identidad externo (Azure AD) y un modelo de Control de Acceso Basado en Roles (RBAC) para gestionar permisos de usuario. [cite: 5542]
  * **Justificación:** Esta decisión satisface la restricción del uso de Azure AD y centraliza la lógica de seguridad, evitando que cada microservicio la reimplemente. Minimiza el riesgo de accesos no autorizados y apoya el driver de seguridad.

* **Concepto de Diseño: Gateway de API Seguro (API Gateway)**
  * [cite_start]**Descripción:** Utilizar un API Gateway que actúe como un punto único de control de seguridad para gestionar la validación de tokens, las autorizaciones y el cifrado de las comunicaciones. [cite: 5466]
  * **Justificación:** Proporciona una capa adicional de seguridad para las interacciones entre los clientes y el back-end, fortaleciendo la protección contra ataques externos y simplificando la gestión de la seguridad.

---

#### **Alta Disponibilidad**

* **Concepto de Diseño: Sistemas Tolerantes a Fallos**
  * [cite_start]**Descripción:** Emplear tácticas de redundancia (múltiples instancias de cada servicio) y replicación de datos para garantizar que el sistema siga operativo incluso si una parte falla. [cite: 5533, 5536]
  * **Justificación:** Aumenta la resiliencia del sistema y minimiza el tiempo de inactividad, asegurando una alta disponibilidad para cumplir con el SLA del 99.5%.

* **Concepto de Diseño: Comunicación Asíncrona**
  * [cite_start]**Descripción:** Utilizar un Message Broker para la comunicación entre servicios que no requieren una respuesta inmediata. [cite: 957, 5472]
  * **Justificación:** Desacopla los servicios, permitiendo que el sistema siga funcionando incluso si un servicio consumidor está temporalmente caído. [cite_start]Esto mejora la disponibilidad general y la percepción de rendimiento. [cite: 1417, 1488]

* **Concepto de Diseño: Patrón Circuit Breaker**
  * [cite_start]**Descripción:** Implementar un mecanismo de *Circuit Breaker* para evitar que las llamadas a servicios que están fallando se propaguen en cascada. [cite: 1113, 5468]
  * **Justificación:** Permite que el sistema se degrade de forma controlada en lugar de fallar por completo, aislando el problema y dando tiempo para la recuperación.

---

#### **Mantenibilidad (Modificabilidad)**

* **Concepto de Diseño: Arquitectura de Microservicios y Domain-Driven Design (DDD)**
  * [cite_start]**Descripción:** Descomponer la aplicación en servicios pequeños y autónomos, donde cada uno se alinea con un Bounded Context del negocio (Finanzas, Proyectos, Colaboración, etc.). [cite: 3131, 5455]
  * **Justificación:** Reduce drásticamente la complejidad de cada módulo. Permite que equipos independientes desarrollen, prueben y desplieguen sus servicios sin afectar a los demás, cumpliendo así el objetivo de implementar cambios en menos de 4 horas.

* **Concepto de Diseño: Base de Datos por Servicio (Database per Service)**
  * [cite_start]**Descripción:** Asignar a cada microservicio su propia base de datos, evitando el acceso directo a la base de datos de otros servicios. [cite: 5470]
  * **Justificación:** Es la táctica clave para lograr un bajo acoplamiento. Garantiza que el esquema de datos de un servicio pueda evolucionar sin romper otros servicios, lo que es fundamental para la mantenibilidad a largo plazo.

---

##### **Objetivo de los Conceptos de Diseño**

Para la **seguridad**, la Autenticación Centralizada y el API Gateway aseguran que solo usuarios autorizados accedan a los datos. Para la **alta disponibilidad**, el uso de Sistemas Tolerantes a Fallos, Comunicación Asíncrona y el patrón Circuit Breaker implementan redundancia y resiliencia para garantizar la operación continua. Para la **mantenibilidad**, la Arquitectura de Microservicios alineada con DDD y el patrón de Base de Datos por Servicio permiten que el sistema evolucione de forma rápida y segura, facilitando el desarrollo paralelo y los despliegues independientes.

#### 4.3.1.5. Instantiate Architectural Elements, Allocate Responsibilities, and Define Interfaces

En esta fase del diseño, se instancian los elementos arquitectónicos basados en los conceptos previamente seleccionados. Se definen las responsabilidades de cada módulo y las interfaces a través de las cuales interactuarán. Este proceso asegura que cada componente cumpla con una función específica y se integre de manera cohesiva en la arquitectura general de **ClearCost**, satisfaciendo los drivers de **Seguridad**, **Disponibilidad** y **Mantenibilidad**.

---

* **Módulo de API Gateway**
  * **Elementos Arquitectónicos:** Servidor de API Gateway (ej. Spring Cloud Gateway), Lógica de enrutamiento, Filtros de seguridad.
  * **Responsabilidades:**
    * Ser el único punto de entrada para todas las peticiones externas.
    * Validar los tokens de autenticación (JWT) en cada solicitud.
    * Enrutar las peticiones a los microservicios internos correspondientes.
    * Aplicar políticas de seguridad transversales (ej. Rate Limiting).
  * **Interfaces:** API REST expuesta a los clientes (SPA, Móvil) con endpoints versionados. Comunicación interna con los microservicios vía HTTPS o gRPC.

* **Módulo de Arquitectura de Microservicios (Estilo Principal)**
  * **Elementos Arquitectónicos:** Contenedores de servicios independientes por cada Bounded Context (`IdentityService`, `ProjectService`, `FinanceService`, `CollaborationService`).
  * **Responsabilidades:**
    * [cite_start]Cada servicio encapsula una capacidad de negocio específica y completa[cite: 5751].
    * [cite_start]Cada servicio gestiona su propio estado y persistencia de datos[cite: 8094].
    * [cite_start]Los servicios se despliegan de forma independiente[cite: 5752].
  * **Interfaces:** Cada servicio expone una API REST/gRPC bien definida para ser consumida por el API Gateway u otros servicios. Se suscriben y publican eventos en el Message Broker.

* **Módulo de Comunicación Asíncrona**
  * **Elementos Arquitectónicos:** Message Broker (ej. Azure Service Bus, RabbitMQ), Canales de eventos (Topics/Queues).
  * **Responsabilidades:**
    * [cite_start]Gestionar la cola de mensajes para desacoplar la comunicación entre microservicios[cite: 8879].
    * Garantizar la entrega de eventos incluso si los servicios consumidores no están disponibles temporalmente.
    * [cite_start]Soportar patrones como Publish/Subscribe para notificaciones[cite: 8796].
  * **Interfaces:** Interfaz para publicar eventos (ej. `TareaCreada`, `PresupuestoAprobado`) y para suscribirse a dichos eventos.

* **Módulo de Diseño de Sistemas Tolerantes a Fallos**
  * **Elementos Arquitectónicos:** Orquestador de contenedores (ej. Kubernetes en Azure AKS), Múltiples instancias (réplicas) de cada microservicio, Health Check endpoints.
  * **Responsabilidades:**
    * [cite_start]Mantener la disponibilidad del sistema mediante la replicación de componentes críticos[cite: 8578].
    * Detectar y reiniciar automáticamente instancias de servicios que han fallado.
    * Distribuir la carga de trabajo entre las instancias disponibles.
  * **Interfaces:** Endpoints `/health` en cada microservicio que el orquestador consume para verificar el estado del servicio.

* **Módulo de Persistencia de Datos**
  * **Elementos Arquitectónicos:** Bases de datos PostgreSQL independientes para cada microservicio (Patrón Database per Service).
  * **Responsabilidades:**
    * [cite_start]Cada base de datos es propiedad exclusiva de un único microservicio, que es el único que puede acceder a ella directamente[cite: 8094].
    * Garantizar la integridad y consistencia de los datos dentro de su propio Bounded Context.
  * **Interfaces:** Interfaces de Repositorio (ej. `ProjectRepository`) dentro de cada microservicio que abstraen el acceso a los datos.

#### 4.3.1.6. Sketch Views (C4 & UML) and Record Design Decisions

![Foto](/img/chapter4/ContenedorDiagram.png) 

![Foto](/img/chapter4/ComponentDiagram.png)

##### Análisis de los Diagramas

Los siguientes diagramas visualizan la arquitectura de **ClearCost** aplicando el Modelo C4. Cada diagrama ofrece un nivel de abstracción distinto, permitiendo comunicar las decisiones de diseño a diferentes audiencias.

**Análisis del Diagrama de Contenedores (C2)**

Este diagrama es la columna vertebral de la arquitectura y valida visualmente las decisiones estratégicas tomadas para satisfacer los drivers arquitectónicos:

* **Punto de Entrada Único y Seguro:** Se observa cómo todo el tráfico de los usuarios (desde la SPA) se canaliza a través de un único **API Gateway**. Esta táctica es fundamental para el driver de **Seguridad**, ya que centraliza la autenticación y la aplicación de políticas de seguridad antes de que cualquier petición alcance la lógica de negocio.
* **Separación por Dominio (Alta Mantenibilidad):** La descomposición en microservicios (`Identity & Access Service`, `Finance Service`, `Project Service`, `Collaboration Service`) está claramente definida. Esto materializa nuestra meta de **Mantenibilidad**, ya que permite que los equipos puedan desarrollar, probar y desplegar cada dominio de forma independiente.
* **Aislamiento de Datos y Resiliencia:** Cada microservicio posee su propia base de datos, como lo demuestra la relación uno a uno (ej. `Project Service` -> `Project DB`). Este patrón (`Database per Service`) es clave para lograr un bajo acoplamiento y alta **Disponibilidad**, ya que la falla en una base de datos solo impacta a su servicio correspondiente.
* **Comunicación Asíncrona para la Disponibilidad:** El `Message Broker` actúa como un intermediario que desacopla los servicios. Por ejemplo, el `Project Service` puede publicar un evento como "TareaCompletada" sin necesidad de esperar a que el `Collaboration Service` lo procese para enviar una notificación. Esto mejora la **Disponibilidad** y el **Rendimiento** del sistema.

**Análisis del Diagrama de Componentes (C3) - Project Service**

Este diagrama ofrece una vista detallada para los desarrolladores que trabajarán dentro del **Project Service**, mostrando una arquitectura interna limpia y bien estructurada:

* **Separación de Responsabilidades:** Se evidencia una clara división de responsabilidades siguiendo los principios de una arquitectura limpia:
  * El **API Controller** gestiona exclusivamente las peticiones web (HTTP).
  * La **Domain Logic** contiene las reglas de negocio, aislada de las preocupaciones de la infraestructura.
  * El **Data Repository** encapsula la lógica de acceso a la base de datos, haciendo que el dominio sea agnóstico a la tecnología de persistencia.
* **Patrón Adapter para Mantenibilidad:** Los componentes `S3 Adapter` y `Event Publisher` actúan como adaptadores. Aíslan la lógica de dominio de los detalles de implementación de sistemas externos (Amazon S3 y el Message Broker). Si en el futuro se decidiera cambiar el proveedor de almacenamiento o de mensajería, solo habría que modificar o reemplazar estos adaptadores, sin tocar el núcleo del negocio, lo que refuerza enormemente la **Mantenibilidad**.

