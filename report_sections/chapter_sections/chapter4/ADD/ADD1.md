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