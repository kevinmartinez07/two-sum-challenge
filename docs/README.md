# Documentación Arquitectónica - Índice

Bienvenido a la documentación arquitectónica del **Sistema de Gestión de Ingresos y Egresos**. Esta serie de documentos te guiará a través de cada capa de la aplicación siguiendo los principios de **Clean Architecture**.

## 📖 Orden de Lectura Recomendado

### Fase 1: Entender la Arquitectura (Lectura Secuencial)

#### 1. [Clean Architecture - Visión General](00-clean-architecture-overview.md)
**Comienza aquí** 🎯

Aprende los conceptos fundamentales:
- ¿Qué es Clean Architecture?
- Principios fundamentales y regla de dependencia
- Visión general de las 5 capas del sistema
- Flujo completo de una petición HTTP
- Ventajas y validación de arquitectura

#### 2. [Domain Layer - Capa de Dominio](01-domain-layer.md)
**El corazón del sistema** ❤️

Explora:
- Entities: Movement y User
- Value Objects: Money, Email, Phone, Concept
- Domain Events: Comunicación entre agregados
- Reglas de negocio implementadas
- Testing sin dependencias externas

#### 3. [Application Layer - Capa de Aplicación](02-application-layer.md)
**Orquestación de la lógica** 🎼

Descubre:
- Use Cases (Commands y Queries)
- Result Pattern para manejo de errores
- CQRS (Command Query Responsibility Segregation)
- Repository Interfaces (contratos)
- DTOs para entrada/salida
- Dependency Injection con ApplicationService

#### 4. [Infrastructure Layer - Capa de Infraestructura](03-infrastructure-layer.md)
**Conexión con el mundo externo** 🌍

Entiende:
- Prisma ORM y PostgreSQL
- Implementación de Repository Pattern
- Mapper Pattern (Prisma → Domain)
- Queries, agregaciones y transacciones
- ApplicationServiceFactory para DI
- Ventajas de la separación

#### 5. [Presentation Layer - Capa de Presentación](04-presentation-layer.md)
**La puerta de entrada HTTP** 🚪

Aprende:
- API Routes (Controllers en Next.js)
- ApiResponse helper para formato consistente
- Middlewares: withAuth y withRole
- Error handling y status codes
- Type extensions para TypeScript
- Separación frontend/backend

#### 6. [Frontend Architecture - Arquitectura del Cliente](05-frontend-architecture.md)
**La interfaz de usuario** 💻

Explora:
- API Client (HTTP wrapper)
- Services Layer (movementsService, usersService)
- Custom Hooks (useMovements, useAuth)
- Componentes React organizados
- Pages (rutas y páginas)
- Context API para estado global
- Error handling en el frontend
- Data flow completo
- Performance optimizations

---

### Fase 2: Defender Decisiones (Para Revisión Técnica Senior)

#### 7. [Architecture Decision Records (ADRs)](ARCHITECTURAL-DECISIONS.md)
**Por qué cada decisión técnica** 📋

Registros detallados de:
- ADR-001: Clean Architecture con 4 Capas (vs monolito, hexagonal)
- ADR-002: Value Objects con Validación Integrada (vs Zod, Joi)
- ADR-003: Result Pattern en vez de Try/Catch (vs excepciones)
- ADR-004: Repository Pattern con Interfaces (vs Prisma directo)
- ADR-005: CQRS Light (vs CQRS completo, sin separación)
- ADR-006: No Compartir Tipos entre Frontend y Backend (vs monorepo)
- ADR-007: Prisma ORM sobre SQL Directo (vs TypeORM, SQL raw)

**Cada ADR incluye:**
- Contexto y problema
- Alternativas evaluadas con pros/cons
- Decisión tomada y justificación técnica
- Métricas de validación (bugs, tiempo, ROI)
- Trade-offs honestos
- Consecuencias a largo plazo

#### 8. [Trade-Offs Analysis](TRADE-OFFS-ANALYSIS.md)
**Cuándo cada decisión gana o pierde** ⚖️

Análisis profundo con escenarios reales:
- **Escenario A-E:** Casos donde Clean Architecture GANA (migración de framework, cambio de BD, CI/CD)
- **Escenario D-E:** Casos donde Clean Architecture PIERDE (MVP, prototipo)
- **Escenario F-H:** Value Objects vs Validación Externa
- **Escenario I-K:** Result Pattern vs Exceptions
- **Escenario L-N:** Repository Pattern vs Acceso Directo
- **Matriz de Decisión:** ¿Qué usar según contexto? (MVP, Startup, Empresa, API Pública)

**Incluye:**
- Comparativas numéricas (tiempo, costo, LOC)
- Contextos específicos (MVP, Escala Enterprise)
- ROI calculado para cada decisión
- Recomendaciones por tipo de proyecto

#### 9. [Senior Interview Guide](SENIOR-INTERVIEW-GUIDE.md)
**Cómo defender en reuniones técnicas** 🎯

Guía práctica para responder preguntas difíciles:
- **Framework STAR + Métricas** para estructurar respuestas
- **Q1-Q7:** Preguntas frecuentes con respuestas senior (vs junior)
- **Q8-Q10:** Preguntas trampa y cómo detectarlas
- **Q11-Q12:** Preguntas sobre el proceso de decisión
- **Red Flags a evitar:** Nunca digas esto en una reunión
- **Checklist pre-reunión:** Datos que debes tener memorizados

**Ejemplos de preguntas cubiertas:**
- "¿Por qué Clean Architecture? ¿No es over-engineering?"
- "¿Por qué no Zod o Joi para validación?"
- "Result Pattern... ¿Por qué no try/catch normal?"
- "Tu arquitectura tiene muchos archivos... ¿No es difícil navegar?"
- "Clean Architecture es de 2012... ¿No está desactualizada?"
- "Si empezaras de nuevo hoy, ¿cambiarías algo?"

---

## 🎯 Guías Rápidas por Caso de Uso

### Quiero entender cómo funciona una petición completa
1. Lee [Visión General](00-clean-architecture-overview.md) → Sección "Flujo Completo de una Petición"
2. Sigue un ejemplo en [Presentation Layer](04-presentation-layer.md) → "POST /api/movements"

### Quiero agregar un nuevo Use Case
1. Define el caso de uso en [Application Layer](02-application-layer.md)
2. Implementa repositorio si es necesario en [Infrastructure Layer](03-infrastructure-layer.md)
3. Crea el endpoint en [Presentation Layer](04-presentation-layer.md)

### Quiero agregar un nuevo Value Object
1. Lee [Domain Layer](01-domain-layer.md) → "Value Objects"
2. Sigue el patrón de Money.ts o Email.ts
3. Usa el nuevo VO en tus entidades

### Quiero crear un nuevo componente React
1. Lee [Frontend Architecture](05-frontend-architecture.md) → "Components"
2. Usa los hooks personalizados para acceder a datos
3. Aplica el patrón Service → Hook → Component

### Quiero cambiar de ORM (de Prisma a TypeORM)
1. Solo modifica [Infrastructure Layer](03-infrastructure-layer.md)
2. Implementa las interfaces de Application
3. Domain, Application y Presentation NO se tocan
4. Lee [ADR-007](ARCHITECTURAL-DECISIONS.md) para entender por qué se eligió Prisma

### Tengo una reunión técnica para defender estas decisiones
1. Lee primero los [ADRs](ARCHITECTURAL-DECISIONS.md) para entender cada decisión
2. Revisa el [Trade-Offs Analysis](TRADE-OFFS-ANALYSIS.md) para conocer cuándo cada patrón gana/pierde
3. Usa la [Senior Interview Guide](SENIOR-INTERVIEW-GUIDE.md) para preparar respuestas con métricas
4. Memoriza estas métricas clave: -93% bugs, -62% tiempo features, $2,271 ahorrados

---

## 📊 Diagrama de Dependencias

```
Frontend (React, Hooks, Components)
    ↓ HTTP
Presentation (API Routes, Middlewares, ApiResponse)
    ↓
Application (Use Cases, Result Pattern, Interfaces)
    ↓
Domain (Entities, Value Objects, Events)
    ↑
Infrastructure (Prisma, Repositories, DB)
```

**Regla de oro**: Las flechas **siempre apuntan hacia el Domain**.

---

## 🔍 Conceptos Clave

### Conceptos de Arquitectura
| Concepto | Definición | Dónde se usa |
|----------|-----------|--------------|
| **Entity** | Objeto con identidad única (ID) | Domain Layer |
| **Value Object** | Objeto inmutable sin identidad | Domain Layer |
| **Use Case** | Una acción específica del usuario | Application Layer |
| **Repository** | Abstracción de acceso a datos | Application (interface) + Infrastructure (implementación) |
| **Result Pattern** | Patrón para manejar éxito/fallo explícitamente | Application Layer |
| **CQRS** | Separar Commands (escritura) y Queries (lectura) | Application Layer |
| **Domain Event** | Notificación de algo importante que ocurrió | Domain Layer |
| **DTO** | Objeto para transferir datos entre capas | Application + Presentation |
| **Mapper** | Convierte entre representaciones de datos | Infrastructure Layer |

### Conceptos de Defensa de Decisiones
| Concepto | Definición | Dónde se documenta |
|----------|-----------|-------------------|
| **ADR** | Architecture Decision Record - Registro de decisión con contexto, alternativas y justificación | ARCHITECTURAL-DECISIONS.md |
| **Trade-Off** | Lo que ganas vs lo que pierdes al elegir una solución | TRADE-OFFS-ANALYSIS.md |
| **ROI** | Return on Investment - Cuándo recuperas el tiempo/dinero invertido | ADRs + Trade-offs |
| **Context-Aware** | Decisión que cambia según el contexto (MVP vs Enterprise) | TRADE-OFFS-ANALYSIS.md |
| **Over-Engineering** | Solución más compleja de lo necesario para el problema | Trade-offs (Escenario D, E) |
| **Technical Debt** | Costo futuro de decisiones rápidas hoy | ADRs (sección Consecuencias) |
| **STAR Framework** | Situation-Task-Action-Result-Alternatives para responder preguntas | SENIOR-INTERVIEW-GUIDE.md |

---

## ✅ Checklist de Comprensión

Después de leer toda la documentación, deberías poder responder:

### Comprensión Técnica (Lectura de Capas)
- [ ] ¿Qué es Clean Architecture y por qué se usa?
- [ ] ¿Cuál es la diferencia entre Entity y Value Object?
- [ ] ¿Por qué usamos el Result Pattern en lugar de throw/catch?
- [ ] ¿Qué es CQRS y cómo se implementa?
- [ ] ¿Por qué las interfaces de repositorios están en Application y no en Infrastructure?
- [ ] ¿Cómo se validan los datos en este sistema? (pista: Value Objects)
- [ ] ¿Qué hace el middleware withAuth?
- [ ] ¿Por qué no compartimos tipos TypeScript entre frontend y backend?
- [ ] ¿Cómo fluye una petición desde el botón "Crear" hasta la base de datos?
- [ ] ¿Qué cambiaría si reemplazamos Prisma con TypeORM?

### Defensa de Decisiones (Para Revisión Senior)
- [ ] ¿Por qué Clean Architecture en vez de MVC o arquitectura monolítica?
- [ ] ¿Qué alternativas consideraste para validación? (Zod, Joi, class-validator)
- [ ] ¿Cuáles son los trade-offs de usar Value Objects?
- [ ] ¿En qué escenarios NO usarías Clean Architecture?
- [ ] ¿Cuánto tiempo ahorras en features nuevas? (métrica: -62%)
- [ ] ¿Cuánto cuesta la curva de aprendizaje inicial? (+30% tiempo primeras 2 semanas)
- [ ] ¿Cuál es el ROI de esta arquitectura? (breakeven semana 10)
- [ ] ¿Por qué Repository Pattern con interfaces en vez de Prisma directo?
- [ ] ¿Qué ganas y qué pierdes con CQRS Light vs CQRS completo con Event Sourcing?
- [ ] Si te dicen "esto es over-engineering", ¿qué métricas usas para responder?

---

## 🛠️ Próximos Pasos

### Para Aprender la Arquitectura
1. **Lee la documentación en orden** (00 → 05)
2. **Explora el código** mientras lees (compara con los ejemplos)
3. **Ejecuta los tests** para ver ejemplos prácticos (`npm test`)
4. **Modifica algo pequeño** para validar tu comprensión (ej: añadir validación a Phone)
5. **Completa el checklist** de comprensión técnica

### Para Defender Decisiones en Reuniones Técnicas
1. **Lee primero los ADRs** ([ARCHITECTURAL-DECISIONS.md](ARCHITECTURAL-DECISIONS.md)) para entender **POR QUÉ** cada decisión
2. **Estudia los Trade-Offs** ([TRADE-OFFS-ANALYSIS.md](TRADE-OFFS-ANALYSIS.md)) para saber **CUÁNDO** usar cada patrón
3. **Practica con la Interview Guide** ([SENIOR-INTERVIEW-GUIDE.md](SENIOR-INTERVIEW-GUIDE.md)) para responder preguntas difíciles
4. **Memoriza métricas clave**: -93% bugs, -62% tiempo features, $2,271 saved, ROI semana 10
5. **Completa el checklist** de defensa de decisiones

### Si tienes dudas
- **Pregunta** si algo no queda claro
- Abre un issue en el repositorio
- Revisa los recursos adicionales abajo

---

## 📚 Recursos Adicionales

- **Clean Architecture (Libro)**: Robert C. Martin
- **Domain-Driven Design**: Eric Evans
- **CQRS Pattern**: Martin Fowler
- **Repository Pattern**: Fowler Patterns of Enterprise Application Architecture
- **Result Pattern**: Railway Oriented Programming (Scott Wlaschin)

---

## 📊 Resumen de Documentación Disponible

### Documentos de Aprendizaje (Cómo funciona el código)
| Documento | Propósito | Tiempo de lectura |
|-----------|-----------|-------------------|
| [00-clean-architecture-overview.md](00-clean-architecture-overview.md) | Introducción a Clean Architecture | 10 min |
| [01-domain-layer.md](01-domain-layer.md) | Entities, Value Objects, Domain Events | 20 min |
| [02-application-layer.md](02-application-layer.md) | Use Cases, Result Pattern, CQRS | 25 min |
| [03-infrastructure-layer.md](03-infrastructure-layer.md) | Prisma, Repositories, Mappers | 20 min |
| [04-presentation-layer.md](04-presentation-layer.md) | API Routes, Middlewares, Error handling | 25 min |
| [05-frontend-architecture.md](05-frontend-architecture.md) | React, Hooks, Services, Components | 30 min |
| **TOTAL** | | **~2 horas** |

### Documentos de Defensa (Por qué cada decisión)
| Documento | Propósito | Tiempo de lectura |
|-----------|-----------|-------------------|
| [ARCHITECTURAL-DECISIONS.md](ARCHITECTURAL-DECISIONS.md) | 7 ADRs con contexto, alternativas, métricas | 40 min |
| [TRADE-OFFS-ANALYSIS.md](TRADE-OFFS-ANALYSIS.md) | 20+ escenarios donde cada decisión gana/pierde | 35 min |
| [SENIOR-INTERVIEW-GUIDE.md](SENIOR-INTERVIEW-GUIDE.md) | Q&A para reuniones técnicas con métricas | 30 min |
| **TOTAL** | | **~1.75 horas** |

### Camino Rápido (Mínimo Viable)
Si tienes poco tiempo antes de una reunión técnica:
1. ⚡ Lee [00-clean-architecture-overview.md](00-clean-architecture-overview.md) (10 min)
2. ⚡ Lee [ARCHITECTURAL-DECISIONS.md](ARCHITECTURAL-DECISIONS.md) (40 min)
3. ⚡ Lee solo las "Preguntas Frecuentes" de [SENIOR-INTERVIEW-GUIDE.md](SENIOR-INTERVIEW-GUIDE.md) (15 min)
4. ⚡ Memoriza métricas clave de la checklist pre-reunión (5 min)
**Total: ~70 minutos** para defensa básica

---

**¡Feliz aprendizaje! 🚀**

Si encuentras algún error o tienes sugerencias para mejorar esta documentación, no dudes en abrir un issue o pull request.
