# 📖 Guía Rápida para la Revisión Técnica del Martes

## ⚡ Lectura Express (30 minutos)

Si solo tienes 30 minutos, lee **SOLO ESTOS** documentos en orden:

1. **[00-INDICE.md](./00-INDICE.md)** (2 min) - Navegación
2. **[13-FAQ-REVISION-TECNICA.md](./13-FAQ-REVISION-TECNICA.md)** (25 min) ⭐ **MUY IMPORTANTE**
3. **Este documento** (3 min) - Resumen de conceptos clave

---

## 🎯 Conceptos Clave que DEBES Dominar

### 1. Clean Architecture (Arquitectura Limpia)

**En una frase:**  
"El dominio no depende de nada; todo depende del dominio."

**Capas:**
```
📦 Domain (Entidades, Value Objects)
     ↑
📦 Application (Use Cases, DTOs)
     ↑
📦 Infrastructure (Prisma, Repositorios)
📦 Presentation (API Routes)
```

**¿Por qué?**
- ✅ Cambiar DB no afecta dominio
- ✅ Testear sin mocks
- ✅ Código mantenible

**Ejemplo cuando pregunten:**
> "Si mañana cambio de PostgreSQL a MongoDB, solo modifico Infrastructure. Domain, Application y Presentation no se tocan."

---

### 2. CQRS (Command Query Responsibility Segregation)

**En una frase:**  
"Comandos (escritura) y consultas (lectura) están separados."

**Estructura:**
```
Commands (Escritura)      Queries (Lectura)
────────────────────      ─────────────────
CreateMovementUseCase     GetMovementsUseCase
DeleteMovementUseCase     GetBalanceUseCase
```

**¿Por qué?**
- ✅ Claridad de intent
- ✅ Optimización independiente
- ✅ Preparado para escalar (bases separadas futuro)

**Ejemplo cuando pregunten:**
> "Puedo optimizar consultas (índices, cache) sin afectar comandos. Si necesito escalar, puedo tener base de lectura y base de escritura."

---

### 3. Value Objects (Objetos de Valor)

**En una frase:**  
"Objetos inmutables que encapsulan validación."

**Ejemplos en el proyecto:**
- `Money` (valida >= 0, <= 999,999,999.99)
- `Email` (valida formato RFC 5322)
- `Phone` (valida formato E.164)
- `Concept` (valida 3-200 caracteres)

**¿Por qué?**
- ✅ Validación centralizada
- ✅ Inmutabilidad
- ✅ Type safety
- ✅ Reutilizables

**Ejemplo cuando pregunten:**
> "Si cambio una validación (ej: límite de dinero), solo toco `Money.ts`. Sin VOs, tendría que buscar validaciones en 10+ archivos."

---

### 4. Repository Pattern (Patrón Repositorio)

**En una frase:**  
"Interfaz para acceso a datos, implementaciones intercambiables."

**Diagrama:**
```
Use Case
   ↓ usa
IMovementRepository (interfaz)
   ↑ implementa
PrismaMovementRepository
```

**¿Por qué?**
- ✅ Desacopla dominio de DB
- ✅ Fácil de mockear para tests
- ✅ Cambiar DB sin tocar use cases

**Ejemplo cuando pregunten:**
> "Los use cases dependen de la interfaz `IMovementRepository`. Puedo cambiar de Prisma a TypeORM solo cambiando la implementación."

---

### 5. Domain Events (Eventos de Dominio)

**En una frase:**  
"Notificaciones cuando algo importante sucede en el dominio."

**Ejemplo:**
```typescript
DomainEventDispatcher.dispatch(
  new MovementCreatedEvent(movement.id, movement.type, ...)
);
```

**¿Por qué?**
- ✅ Desacopla agregados
- ✅ Facilita auditoría
- ✅ Base para Event Sourcing

**Ejemplo cuando pregunten:**
> "Cuando un movimiento se crea, lanzo un evento. Puedo tener handlers que envíen emails, actualicen estadísticas, etc. Sin tocar el código de creación."

---

## 📊 Atributos de Calidad: Qué Ganas y Qué Pierdes

### ✅ Ganas

| Atributo | Por qué |
|----------|---------|
| **Mantenibilidad** | Código desacoplado, fácil de modificar |
| **Testabilidad** | 198 tests, sin mocks para dominio |
| **Escalabilidad** | Preparado para microservicios, CQRS completo |
| **Flexibilidad** | Cambiar tecnologías sin afectar dominio |

### ⚠️ Sacrificas

| Atributo | Mitigación |
|----------|------------|
| **Velocidad inicial** | ROI positivo después del mes 2 |
| **Simplicidad aparente** | Documentación exhaustiva |
| **Memoria (~20%)** | Cache, lazy loading |
| **Performance (~10ms)** | Índices, optimización de queries |

---

## 🎤 Preguntas Probables y Respuestas Rápidas

### P: "¿No es over-engineering?"

**R:** "No, porque el proyecto tiene requisitos de testabilidad, mantenibilidad y longevidad. Si fuera un prototipo de 1 semana, sí sería over-engineering. Pero este es un proyecto de producción con 198 tests automatizados y CI/CD."

---

### P: "¿Por qué Clean Architecture?"

**R:** "Por tres razones: (1) Testabilidad sin mocks, (2) Independencia de frameworks y DB, (3) Mantenibilidad a largo plazo. Puedo cambiar de Next.js a NestJS o de PostgreSQL a MongoDB sin tocar el dominio."

---

### P: "¿Cómo escalas?"

**R:** "Múltiples dimensiones: (1) Microservicios (cada use case puede ser un servicio), (2) CQRS completo (bases separadas lectura/escritura), (3) Cache layer (decorador de repositorio), (4) Sharding de DB por userId."

---

### P: "¿Por qué CQRS sin bases separadas?"

**R:** "CQRS no requiere bases separadas. Lo uso para claridad (separar intent) y escalabilidad futura. Si necesito escalar, puedo evolucionar a Commands → PostgreSQL, Queries → MongoDB/Redis."

---

### P: "¿Por qué Value Objects?"

**R:** "Encapsulan validación, garantizan inmutabilidad, type safety y expresan el lenguaje del dominio. Si cambio una validación, solo toco 1 archivo."

---

### P: "¿Qué pasa si cambias de base de datos?"

**R:** "Creo un nuevo repositorio (ej: `MongoMovementRepository`) que implementa `IMovementRepository`. Cambio 1 línea en `ApplicationService`. Domain, Application y Presentation no cambian."

---

### P: "¿Cuál es la parte más compleja?"

**R:** "El mapeo entre capas (Prisma → Domain → DTO → JSON). Lo mitigo con mapper classes, tests de mapeo y TypeScript para type safety."

---

### P: "¿Cómo testeas con esta arquitectura?"

**R:** "4 niveles: (1) Unitarios de domain (sin mocks), (2) Unitarios de use cases (con mocks), (3) Integración (con DB test), (4) E2E (API completa). 198 tests en 5 segundos."

---

## 🏗️ Stack Tecnológico (Memoriza)

| Capa | Tecnología | Versión |
|------|-----------|---------|
| Frontend | Next.js + React + TypeScript | 15, 18, 5.7 |
| Estilos | Tailwind CSS | 3.4 |
| Backend | Next.js API Routes | 15 |
| ORM | Prisma | 6.15 |
| DB | PostgreSQL | - |
| Auth | Better Auth | 1.1 |
| Testing | Jest | 30.2 |
| Deploy | Vercel | - |
| CI/CD | GitHub Actions | - |

---

## 📐 Principios SOLID Aplicados

| Principio | Cómo lo aplicas |
|-----------|----------------|
| **S**RP | Cada use case tiene UNA responsabilidad |
| **O**CP | Agregar features sin modificar existentes |
| **L**SP | Implementaciones de repos son intercambiables |
| **I**SP | Interfaces pequeñas y específicas |
| **D**IP | Application depende de interfaces, no implementaciones |

---

## 🎯 Frases Clave para Usar

Durante la reunión, usa estas frases (suenan profesionales):

1. **"Separación de responsabilidades"**  
   Cuando hables de capas o componentes.

2. **"Inversión de dependencias"**  
   Cuando hables de repositorios o interfaces.

3. **"Testabilidad sin mocks"**  
   Cuando hables de tests de dominio.

4. **"Preparado para escalar"**  
   Cuando hables de CQRS o arquitectura.

5. **"Código mantenible a largo plazo"**  
   Cuando justifiques la complejidad inicial.

6. **"Independencia de frameworks"**  
   Cuando hables de Clean Architecture.

7. **"Encapsulación de validación"**  
   Cuando hables de Value Objects.

8. **"Lenguaje ubicuo del dominio"**  
   Cuando hables de DDD o Value Objects.

---

## 📚 Estructura del Proyecto (Memoriza)

```
lib/server/
├── domain/                  # Lógica de negocio pura
│   ├── entities/           # User, Movement
│   ├── value-objects/      # Money, Email, Phone
│   └── events/             # Domain Events
│
├── application/            # Casos de uso
│   ├── use-cases/
│   │   ├── commands/       # Escritura (CQRS)
│   │   └── queries/        # Lectura (CQRS)
│   ├── repositories/       # Interfaces (ports)
│   └── shared/             # Result Pattern
│
├── infrastructure/         # Detalles técnicos
│   └── repositories/       # Implementaciones (adapters)
│
└── presentation/           # API HTTP
    └── middlewares/        # Auth, Role, ErrorHandling
```

---

## ⏰ Timeline de Lectura Recomendado

### Noche antes (2 horas)
1. Lee [13-FAQ-REVISION-TECNICA.md](./13-FAQ-REVISION-TECNICA.md) completo
2. Repasa este documento
3. Dibuja la arquitectura en papel

### Mañana del martes (30 min)
1. Relee preguntas del FAQ (solo las respuestas cortas)
2. Repasa "Conceptos Clave" de arriba
3. Repasa "Preguntas Probables"

### Antes de la reunión (10 min)
1. Respira profundo 😌
2. Repasa "Frases Clave para Usar"
3. Mentaliza el flujo: User → API → Use Case → Repository → DB

---

## 💡 Tips para la Reunión

### ✅ HAZ:
- Empieza con el "Por Qué" antes del "Qué"
- Usa ejemplos concretos
- Menciona trade-offs antes de que pregunten
- Conecta con principios SOLID
- Sé honesto sobre limitaciones

### ❌ NO HAGAS:
- Mentir o inventar cosas que no existen
- Usar buzzwords sin explicar
- Ser defensivo ante críticas constructivas
- Divagar sin llegar al punto

---

## 🚀 Estructura de Respuesta Ideal

```
1. Respuesta directa (1 frase)
   ↓
2. Razón principal (1-2 frases)
   ↓
3. Ejemplo concreto (código o diagrama)
   ↓
4. Beneficio (1 frase)
```

**Ejemplo:**

**P:** "¿Por qué usas Value Objects?"

**R:**  
1️⃣ "Los Value Objects encapsulan validación y garantizan inmutabilidad."  
2️⃣ "Si cambio el límite de dinero de $999M a $9B, solo toco `Money.ts`."  
3️⃣ "Sin VOs, tendría que buscar validaciones en `CreateMovementUseCase`, `UpdateMovementUseCase`, API routes, frontend, etc."  
4️⃣ "Esto reduce bugs y acelera desarrollo a largo plazo."

---

## 🎯 Última Checklist

Antes de la reunión, asegúrate de poder responder:

- [ ] ¿Qué es Clean Architecture?
- [ ] ¿Por qué se usa CQRS?
- [ ] ¿Qué problemas resuelven los Value Objects?
- [ ] ¿Cómo funciona el Repository Pattern?
- [ ] ¿Qué ganas con esta arquitectura?
- [ ] ¿Qué sacrificas y cómo lo mitigas?
- [ ] ¿Cómo testeas el sistema?
- [ ] ¿Cómo escalarías el sistema?
- [ ] ¿Qué pasaría si cambias la base de datos?
- [ ] ¿Cuál es la parte más compleja?

Si puedes responder estas 10 preguntas, **estás listo** ✅

---

## 📞 Recordatorio Final

**Confía en tu trabajo.** Has construido un sistema sólido con:
- ✅ 198 tests automatizados
- ✅ Arquitectura escalable
- ✅ Código limpio y mantenible
- ✅ Documentación exhaustiva
- ✅ CI/CD funcional
- ✅ Producción en Vercel

**¡Éxito el martes! 🚀**

---

## 📖 Documentación Completa

### Para Lectura Rápida (30 min)
- [00-INDICE.md](./00-INDICE.md)
- [13-FAQ-REVISION-TECNICA.md](./13-FAQ-REVISION-TECNICA.md) ⭐

### Para Estudio Profundo (3-4 horas)
1. [01-VISION-GENERAL.md](./01-VISION-GENERAL.md)
2. [02-ARQUITECTURA.md](./02-ARQUITECTURA.md)
3. [03-PATRONES-DISENO.md](./03-PATRONES-DISENO.md)
4. [04-ATRIBUTOS-CALIDAD.md](./04-ATRIBUTOS-CALIDAD.md)
5. [05-ARQUITECTURA-FRONTEND.md](./05-ARQUITECTURA-FRONTEND.md)
6. [11-COMPLEJIDADES.md](./11-COMPLEJIDADES.md)
7. [13-FAQ-REVISION-TECNICA.md](./13-FAQ-REVISION-TECNICA.md)

---

**Última actualización:** Febrero 2026  
**Autor:** Tu equipo de documentación técnica 😊
