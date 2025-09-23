# Capítulo IV: Product Architecture Design

## 4.1. Design Concepts, ViewPoints & ER Diagrams

### 4.1.1. Principles Statements

A partir de la visión arquitectónica y los objetivos de negocio de **ClearCost**, se definen los siguientes principios que orientarán el desarrollo y evolución de la plataforma, garantizando coherencia y sostenibilidad a largo plazo:  

- **Transparencia como eje central**: toda la información financiera y de gestión de proyectos debe ser clara, verificable y fácilmente accesible para usuarios internos y clientes.  
- **Disponibilidad 24/7**: la plataforma debe garantizar un acceso constante, desde cualquier lugar y dispositivo, asegurando continuidad en las operaciones de obra.  
- **Escalabilidad modular**: la solución debe construirse con una arquitectura modular que facilite la incorporación de nuevas funcionalidades en fases futuras sin comprometer la estabilidad.  
- **Simplicidad y usabilidad**: la interfaz debe priorizar la facilidad de uso, reduciendo la curva de aprendizaje para contratistas, especialistas y entidades contratantes.  
- **Seguridad y privacidad de datos**: el sistema debe implementar prácticas sólidas de protección de la información financiera y documental, respetando la confidencialidad de cada usuario.  
- **Colaboración integrada**: ClearCost debe favorecer la comunicación fluida entre equipos y áreas, centralizando tareas, cronogramas y documentos en un mismo entorno.  
- **Estandarización de procesos**: las funcionalidades deben fomentar la uniformidad en la elaboración de expedientes técnicos y en la gestión financiera, reduciendo errores y reprocesos.  


### 4.1.2. Approaches Statements Architectural Styles & Patterns

#### A. Approaches Statements
Enfoques que guiarán el diseño y la evolución de **ClearCost**:

- **Domain-Driven Design (DDD)**  
  Modelar el dominio (expedientes, presupuestos, contratos, tareas, hitos, reuniones) en **bounded contexts** claros (Finanzas, Proyectos, Colaboración, Identidad & Accesos), con contratos explícitos entre dominios.
  
- **Arquitectura Evolutiva y entrega incremental**  
  Roadmap por incrementos funcionales; decisiones reversibles y *fitness functions* para validar atributos de calidad (disponibilidad 24/7, trazabilidad, desempeño).

- **Twelve-Factor App**  
  Configuración por entorno, dependencias explícitas, *build/release/run* separados y logs como *streams* para portabilidad entre nubes.

- **DevOps & CI/CD**  
  Automatización de *build*, pruebas y despliegues; *feature flags* para habilitar capacidades sin relanzar; *blue/green* o *rolling updates* para minimizar downtime.

- **Observabilidad desde el diseño**  
  *Tracing* distribuido, métricas (SLO/SLA) y *structured logging* por servicio para diagnosticar cuellos de botella y cumplir objetivos de disponibilidad.

- **Security & Privacy by Design**  
  Autenticación y autorización centralizada, mínimos privilegios, cifrado en tránsito y en reposo, segregación de datos por cliente y auditoría de acceso.

- **Infraestructura como Código (IaC)**  
  Definir entornos reproducibles (provisión, redes, seguridad) con plantillas versionadas para asegurar consistencia y escalabilidad.

- **APIs primero**  
  Contratos bien definidos (p. ej., OpenAPI) y gestión del ciclo de vida de APIs para habilitar integraciones graduales con terceros en fases futuras.

---

#### B. Architectural Styles & Patterns

**Estilo principal: Microservicios**  
Servicios autónomos por dominio de negocio, con datos propios y comunicación principalmente asíncrona. Beneficios buscados: escalabilidad independiente, despliegue aislado, resiliencia y alineamiento con equipos multifuncionales.

**Patrones de integración y resiliencia**
- **API Gateway**: único punto de entrada (agregación, *rate limiting*, *authz*); expone APIs públicas y orquesta llamadas hacia servicios internos.
- **Service Mesh** (opcional/etapa futura): *mTLS*, *traffic shaping*, *retries* y *circuit breaking* sin cambiar código de negocio.
- **Circuit Breaker & Retry/Backoff**: evitar cascadas de fallos y mejorar tolerancia a errores transitorios entre servicios.
- **Bulkhead**: aislamiento de recursos por servicio/cola para contener fallos.

**Patrones de datos y mensajería**
- **Database per Service**: cada microservicio es dueño de su esquema para reducir acoplamiento.
- **Outbox + Event Relay**: consistencia entre operaciones locales y publicación de eventos (evita pérdida/duplicidad).
- **Event-Driven Architecture** (mensajería/colas): propagar cambios entre Finanzas, Proyectos y Colaboración sin acoplamiento fuerte.
- **CQRS** (selectivo): separar comandos/lecturas cuando se requiera alto rendimiento en consultas (p. ej., paneles financieros).
- **Saga** (coreografía/orquestación): coordinar transacciones de larga duración (p. ej., creación de proyecto + presupuesto + permisos).

**Patrones de acceso y seguridad**
- **AuthN/AuthZ centralizado**: proveedor de identidad (OIDC) + **RBAC** por rol (contratista, especialista, entidad contratante, admin).
- **Tenant Isolation**: segmentación lógica/física de datos por cliente; políticas de retención y auditoría.

**Patrones para experiencia y colaboración**
- **Backend for Frontend (BFF)**: adaptaciones por público (equipo interno vs. cliente) para optimizar payloads y permisos.
- **Scheduler/Worker**: trabajos programados (recordatorios, cortes de período, conciliaciones) fuera del *request/response*.

**Patrones de evolución**
- **Strangler Fig**: migrar o incorporar módulos gradualmente, permitiendo sustituir componentes sin interrumpir a los usuarios.
- **Feature Toggle**: activar funcionalidades a grupos piloto y reducir riesgo en lanzamientos.

**Asignación sugerida de bounded contexts (ejemplo)**
- **Finanzas**: Presupuestos, valorizaciones, liquidaciones, contratos, reportes.
- **Proyectos**: Expediente, hitos, cronogramas, tareas, adjuntos, control de cambios.
- **Colaboración**: Mensajes, reuniones, notificaciones, recordatorios.
- **Identidad & Accesos**: Usuarios, roles, permisos, auditoría.

**Atributos de calidad soportados por la arquitectura**
- **Disponibilidad 24/7**: despliegues sin caída, escalado horizontal, *health checks* y *self-healing*.
- **Seguridad**: cifrado, principio de mínimo privilegio y trazabilidad de acceso.
- **Escalabilidad**: servicios y almacenes que escalan de forma independiente según la carga (p. ej., reportes financieros).
- **Mantenibilidad**: módulos pequeños con límites claros; contratos API versionados.
- **Observabilidad**: *tracing* y métricas por servicio para detectar anomalías y cumplir SLOs.

> Nota: la adopción de patrones como **CQRS**, **Service Mesh** o **Sagas** puede ser progresiva. La primera entrega priorizará API Gateway, *database per service*, mensajería para eventos clave, *circuit breaker* y observabilidad básica; los patrones avanzados se incorporarán conforme crezca la carga y el alcance funcional.

### 4.1.3. Context Diagram

Se adjuntó diagrama de contexto del sistema ***ClearCost*** realizado con Visual Paradigm.
