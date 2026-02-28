# Clean Architecture - Visión General

## ¿Qué es Clean Architecture?

Clean Architecture es un patrón arquitectónico creado por Robert C. Martin (Uncle Bob) que organiza el código en capas concéntricas, donde las dependencias apuntan **siempre hacia adentro** (hacia el dominio).

## Principios Fundamentales

### 1. Independencia de Frameworks
El dominio no depende de Next.js, React o Prisma. Son herramientas intercambiables.

### 2. Testeable
La lógica de negocio se puede probar sin UI, base de datos o servidor web.

### 3. Independencia de UI
Puedes cambiar de Next.js Pages a App Router, o a Vue/Angular sin tocar la lógica de negocio.

### 4. Independencia de Base de Datos
Puedes cambiar de PostgreSQL a MongoDB sin modificar las reglas de negocio.

### 5. Regla de Dependencia
**Nada en un círculo interno puede saber sobre algo en un círculo externo.**

```
┌─────────────────────────────────────────┐
│         4. PRESENTATION (API/UI)        │  ← Frameworks externos
├─────────────────────────────────────────┤
│     3. INFRASTRUCTURE (Prisma/DB)       │  ← Implementaciones concretas
├─────────────────────────────────────────┤
│  2. APPLICATION (Use Cases/Servicios)   │  ← Casos de uso específicos
├─────────────────────────────────────────┤
│    1. DOMAIN (Entities/Value Objects)   │  ← Reglas de negocio puras
└─────────────────────────────────────────┘
    Las flechas de dependencia van →→→ HACIA ADENTRO
```

## Capas en Nuestro Proyecto

### 1. Domain Layer (`lib/server/domain/`)
**Núcleo del negocio. NO depende de nada.**

- **Entities**: `User`, `Movement` - objetos con identidad y ciclo de vida
- **Value Objects**: `Email`, `Money`, `Phone` - inmutables, validación integrada
- **Events**: `MovementCreatedEvent` - comunicación entre agregados

**Ejemplo**: `Money` valida que el monto esté entre 0.01 y 999,999,999.99

---

### 2. Application Layer (`lib/server/application/`)
**Orquesta la lógica de negocio. Solo depende del Domain.**

- **Use Cases**: `CreateMovementUseCase`, `GetBalanceUseCase` - un caso de uso = una acción del usuario
- **Repository Interfaces**: `IMovementRepository` - contratos (sin implementación)
- **Shared**: `Result<T>` - patrón para manejar éxito/fallo sin excepciones

**Ejemplo**: `CreateMovementUseCase` llama a `Money.create()`, luego a `repository.create()`, retorna `Result<Movement>`

---

### 3. Infrastructure Layer (`lib/server/infrastructure/`)
**Implementaciones concretas. Depende de Application y Domain.**

- **Prisma**: Cliente de base de datos, schema, migraciones
- **Repository Implementations**: `PrismaMovementRepository` - implementa `IMovementRepository` usando Prisma
- **Conversión**: Transforma modelos de Prisma a entidades de Domain

**Ejemplo**: `PrismaMovementRepository.create()` guarda en PostgreSQL y retorna un `Movement` de Domain

---

### 4. Presentation Layer (`lib/server/presentation/`)
**Capa de entrada/salida. Depende de Application.**

- **Middlewares**: `withAuth`, `withRole` - autenticación y autorización
- **Helpers**: `ApiResponse` - formato estándar de respuestas HTTP
- **Types**: DTOs específicos de la presentación
- **Docs**: Especificación OpenAPI

**Ejemplo**: `withAuth` verifica el token y pasa el usuario al endpoint

---

### 5. API Routes (Controllers) (`pages/api/`)
**Punto de entrada HTTP. Coordina todo.**

- Recibe request HTTP
- Llama a Use Cases
- Maneja Result Pattern
- Retorna respuestas con ApiResponse

**Ejemplo**:
```typescript
// pages/api/movements/index.ts
const result = await createMovementUseCase.execute(data);
if (result.isFailure) {
  return ApiResponse.validationErrors(res, [result.error]);
}
return ApiResponse.success(res, result.value);
```

---

## Flujo Completo de una Petición

```
1. Usuario → POST /api/movements
                ↓
2. Middleware withAuth → Valida token
                ↓
3. API Route → Extrae datos del body
                ↓
4. Use Case → CreateMovementUseCase.execute()
                ↓
5. Repository → PrismaMovementRepository.create()
                ↓
6. Prisma → INSERT INTO movements
                ↓
7. Domain Entity → new Movement(...)
                ↓
8. Value Objects → Money.create(), Concept.create()
                ↓
9. Result<Movement> → Retorna al Use Case
                ↓
10. API Route → ApiResponse.success(res, movement)
                ↓
11. Usuario ← { success: true, data: {...} }
```

---

## Validación de Arquitectura

### ✅ Correcto
```typescript
// Use Case depende de Repository Interface (Domain)
class CreateMovementUseCase {
  constructor(private repo: IMovementRepository) {}
}

// Infrastructure implementa la interfaz
class PrismaMovementRepository implements IMovementRepository {
  // Usa Prisma internamente
}
```

### ❌ Incorrecto
```typescript
// Use Case NO debe importar Prisma directamente
import { PrismaClient } from '@prisma/client'; // ❌ VIOLACIÓN

// Domain NO debe importar Next.js
import { NextApiRequest } from 'next'; // ❌ VIOLACIÓN
```

---

## Ventajas en Este Proyecto

1. **Cambio de ORM**: Si migramos de Prisma a TypeORM, solo cambiamos Infrastructure
2. **Testing**: Los Use Cases se testean sin base de datos (mocks de repositories)
3. **Múltiples interfaces**: Podemos agregar GraphQL sin tocar la lógica
4. **Escalabilidad**: Cada capa crece independientemente
5. **Mantenibilidad**: Cambios aislados, menos bugs en cascada

---

## Próximos Pasos

Lee cada archivo en orden:
1. **01-domain-layer.md** - Empieza aquí, el corazón del sistema
2. **02-application-layer.md** - Casos de uso y orquestación
3. **03-infrastructure-layer.md** - Integración con Prisma/PostgreSQL
4. **04-presentation-layer.md** - API y respuestas HTTP
5. **05-frontend-architecture.md** - React, hooks y clientes HTTP
