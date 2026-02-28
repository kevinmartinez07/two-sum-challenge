# 2️⃣ Arquitectura del Sistema

## � Antes de Empezar: Explicación Simple

### 🟢 Analogía: La Arquitectura es Como un Hospital

Imagina un **hospital**:

- **Pacientes** (datos) entran por **recepción** (Presentation Layer)
- **Enfermeras** (Application Layer) los dirigen al **doctor correcto**
- **Doctores** (Domain Layer) aplican su **conocimiento médico** (lógica de negocio)
- **Laboratorio y Farmacia** (Infrastructure) son **servicios de apoyo**

**Regla clave:** El doctor NO sabe cómo funciona el laboratorio. Solo pide análisis y recibe resultados. Si cambias el equipo de laboratorio, el doctor no necesita reentrenarse.

Esta es la esencia de Clean Architecture: **las capas internas no conocen las externas**.

### 🟢 ¿Por Qué Tantas Capas?

**Sin capas (código espagueti):**
```
📄 Un archivo gigante con:
   - Conexión a BD
   - Validaciones
   - Lógica de negocio
   - HTML
   - Todo junto y acoplado
```

**Problema:** Si cambias la base de datos, tienes que revisar TODO el código.

**Con capas (Clean Architecture):**
```
📁 Domain      → Solo lógica de negocio (qué hace)
📁 Application → Solo orquestación (cómo lo hace)
📁 Infrastructure → Solo detalles técnicos (con qué lo hace)
📁 Presentation → Solo interfaz (cómo se ve)
```

**Beneficio:** Si cambias la base de datos, solo tocas Infrastructure.

---

## 🏛️ Visión General Arquitectónica

### 🔵 Explicación Técnica

Este proyecto implementa **Clean Architecture** (Robert C. Martin, 2012). El principio central es la **Regla de Dependencia**: el código fuente solo puede apuntar hacia adentro.

**Terminología equivalente (mismo concepto, diferentes autores):**
- **Clean Architecture** = Uncle Bob (Robert C. Martin)
- **Hexagonal Architecture / Ports & Adapters** = Alistair Cockburn  
- **Onion Architecture** = Jeffrey Palermo

Todas expresan: **el dominio en el centro, la infraestructura afuera**.

---

## 🎯 ¿Por Qué Clean Architecture?

### 🟢 Explicación Simple

Imagina tu negocio de pizza. Tu **receta secreta** (dominio/lógica de negocio) no debería cambiar porque compraste un horno nuevo (infraestructura). El horno es intercambiable, la receta es el corazón.

Clean Architecture protege tu "receta" de cambios en "hornos" (bases de datos, frameworks).

### 🔵 Explicación Técnica

Clean Architecture implementa los principios SOLID:
- **DIP (Dependency Inversion)**: Capas internas definen interfaces, externas las implementan
- **SRP (Single Responsibility)**: Cada capa tiene una responsabilidad clara
- **OCP (Open/Closed)**: Abierto a extensión, cerrado a modificación

### Objetivos Principales
1. **Independencia de Frameworks**: El dominio no depende de Next.js, Prisma, ni ninguna librería externa
2. **Testabilidad**: Las reglas de negocio se pueden testear sin UI, BD, ni servicios externos
3. **Independencia de la UI**: La UI puede cambiar sin afectar el dominio
4. **Independencia de la Base de Datos**: Podemos cambiar PostgreSQL por MongoDB sin tocar el dominio
5. **Independencia de Agentes Externos**: La lógica de negocio no conoce APIs externas

### Regla de Dependencia
> **Las dependencias solo apuntan HACIA DENTRO, nunca hacia fuera**

```
📦 Presentación (API)
     ↓ depende de
📦 Application (Use Cases)
     ↓ depende de
📦 Domain (Entidades, Value Objects)
     ↑ NO depende de nada

🚫 Infrastructure NO es conocida por Domain ni Application
✅ Infrastructure IMPLEMENTA interfaces definidas en Application
```

---

## 🧱 Capas de la Arquitectura

### Estructura de Carpetas

```
lib/server/
├── domain/                    # 🟦 CAPA DE DOMINIO
│   ├── entities/              # Entidades del negocio
│   │   ├── Movement.ts        # Entidad Movement
│   │   └── User.ts            # Entidad User
│   ├── value-objects/         # Value Objects inmutables
│   │   ├── Money.ts           # Validación monetaria
│   │   ├── Email.ts           # Validación de email
│   │   ├── Phone.ts           # Validación de teléfono
│   │   ├── Concept.ts         # Validación de concepto
│   │   ├── MovementType.ts    # Enum type-safe
│   │   └── Role.ts            # Roles del sistema
│   └── events/                # Domain Events
│       ├── DomainEvent.ts     # Clase base abstracta
│       ├── MovementEvents.ts  # Eventos de Movement
│       ├── UserEvents.ts      # Eventos de User
│       └── index.ts
│
├── application/               # 🟨 CAPA DE APLICACIÓN
│   ├── ApplicationService.ts  # Punto de entrada (Facade)
│   ├── repositories/          # Interfaces (Ports)
│   │   ├── IMovementRepository.ts
│   │   └── IUserRepository.ts
│   ├── use-cases/             # Casos de uso (CQRS)
│   │   ├── movements/
│   │   │   ├── commands/      # Comandos (escritura)
│   │   │   │   ├── CreateMovementUseCase.ts
│   │   │   │   └── DeleteMovementUseCase.ts
│   │   │   ├── queries/       # Consultas (lectura)
│   │   │   │   ├── GetMovementsUseCase.ts
│   │   │   │   └── GetBalanceUseCase.ts
│   │   │   └── dtos/          # Data Transfer Objects
│   │   └── users/
│   │       ├── commands/
│   │       │   ├── UpdateUserUseCase.ts
│   │       │   └── DeleteUserUseCase.ts
│   │       ├── queries/
│   │       │   └── GetUsersUseCase.ts
│   │       └── dtos/
│   └── shared/                # Utilidades compartidas
│       └── Result.ts          # Result Pattern
│
├── infrastructure/            # 🟧 CAPA DE INFRAESTRUCTURA
│   ├── prisma/                # Cliente de Prisma
│   │   └── prismaClient.ts
│   └── repositories/          # Implementaciones (Adapters)
│       ├── PrismaMovementRepository.ts
│       └── PrismaUserRepository.ts
│
└── presentation/              # 🟥 CAPA DE PRESENTACIÓN
    ├── middlewares/           # Middlewares de Next.js
    │   ├── withAuth.ts        # Autenticación
    │   ├── withRole.ts        # Autorización
    │   └── withErrorHandling.ts
    ├── helpers/               # Helpers de API
    │   └── ApiResponse.ts     # Formato de respuestas
    └── types/                 # Tipos de API
```

---

## 🟦 CAPA 1: Domain (Dominio)

### Responsabilidades
- **Contiene las reglas de negocio puras**
- **NO depende de nada** (ni frameworks, ni librerías)
- **Altamente testeable** (sin mocks necesarios)

### Componentes

#### 1. Entidades (`entities/`)
**¿Qué son?** Objetos con identidad única que persisten en el tiempo.

**Ejemplo: Movement**
```typescript
export class Movement {
  private readonly _type: MovementTypeVO;
  private _amount: Money;
  private _concept: Concept;

  constructor(
    public readonly id: string,
    typeValue: MovementType,
    amountValue: number,
    conceptValue: string,
    public date: Date,
    public readonly userId: string,
    public readonly createdAt: Date,
    public updatedAt: Date
  ) {
    // Validación en construcción
    this._type = MovementTypeVO.fromString(typeValue);
    this._amount = Money.create(amountValue);
    this._concept = Concept.create(conceptValue);
  }

  // Factory method
  static create(props: {...}): Movement { ... }

  // Getters con validación
  get amount(): number {
    return this._amount.amount;
  }

  set amount(value: number) {
    this._amount = Money.create(value); // Re-validación
  }
}
```

**Características:**
- ✅ ID único (`id: string`)
- ✅ Validación en setters
- ✅ Usa Value Objects internamente
- ✅ Lanza Domain Events

#### 2. Value Objects (`value-objects/`)
**¿Qué son?** Objetos inmutables sin identidad, definidos por sus atributos.

**Ejemplo: Money**
```typescript
export class Money {
  private readonly _amount: number;
  private static readonly MAX_AMOUNT = 999999999.99;

  private constructor(amount: number) {
    this._amount = amount;
  }

  static create(amount: number): Money {
    if (amount < 0) {
      throw new Error('El monto no puede ser negativo');
    }
    if (amount > Money.MAX_AMOUNT) {
      throw new Error(`Monto máximo excedido`);
    }
    return new Money(Math.round(amount * 100) / 100);
  }

  add(other: Money): Money {
    return Money.create(this._amount + other._amount);
  }

  subtract(other: Money): Money { ... }
  multiply(factor: number): Money { ... }
}
```

**Características:**
- ✅ Inmutables (no hay setters)
- ✅ Validación en creación
- ✅ Operaciones retornan nuevas instancias
- ✅ Comparación por valor

**Value Objects en el proyecto:**
| Value Object | Propósito | Validaciones |
|-------------|-----------|--------------|
| `Money` | Cantidades monetarias | >= 0, <= 999,999,999.99, 2 decimales |
| `Email` | Direcciones de email | Formato RFC 5322 |
| `Phone` | Números de teléfono | Formato E.164 (+código país) |
| `Concept` | Concepto del movimiento | 3-200 caracteres |
| `MovementType` | Tipo de movimiento | INCOME o EXPENSE |
| `Role` | Rol de usuario | ADMIN o USER |

#### 3. Domain Events (`events/`)
**¿Qué son?** Eventos que representan algo que pasó en el dominio.

```typescript
export abstract class DomainEvent {
  abstract eventName(): string;
  timestamp = new Date();
}

export class MovementCreatedEvent extends DomainEvent {
  eventName() { return 'MovementCreated'; }
  
  constructor(
    public readonly movementId: string,
    public readonly type: string,
    public readonly amount: number,
    public readonly userId: string,
    public readonly date: Date
  ) {
    super();
  }
}

// Dispatcher simple (puede evolucionar a event bus)
export class DomainEventDispatcher {
  static dispatch(event: DomainEvent): void {
    console.log(`[Event] ${event.eventName()}`, event);
    // Aquí pueden agregarse handlers
  }
}
```

**Uso:**
- Comunicación entre agregados
- Auditoría
- Triggers para side-effects (emails, notificaciones)

---

## 🟨 CAPA 2: Application (Aplicación)

### Responsabilidades
- **Orquesta los casos de uso**
- **Define interfaces (puertos)** para infraestructura
- **Transforma datos** (DTOs)
- **NO contiene lógica de negocio** (eso va en Domain)

### Componentes

#### 1. Use Cases (`use-cases/`)
**¿Qué son?** Acciones que el usuario puede realizar.

**Patrón CQRS** (Command Query Responsibility Segregation):
```
Commands (Escritura)          Queries (Lectura)
─────────────────────         ─────────────────
CreateMovementUseCase    →    GetMovementsUseCase
DeleteMovementUseCase         GetBalanceUseCase
UpdateUserUseCase             GetUsersUseCase
DeleteUserUseCase
```

**Ejemplo: CreateMovementUseCase**
```typescript
export class CreateMovementUseCase {
  constructor(private repository: IMovementRepository) {}

  async execute(input: CreateMovementRequest): Promise<Result<CreateMovementResponse>> {
    try {
      // 1. Validación (puede delegar a Domain)
      // 2. Llamar al repositorio
      const movement = await this.repository.create(input);
      
      // 3. Mapear a DTO de respuesta
      const response: CreateMovementResponse = {
        id: movement.id,
        type: movement.type,
        amount: movement.amount,
        // ...
      };
      
      // 4. Retornar Result
      return Result.ok(response);
    } catch (error) {
      return Result.fail((error as Error).message);
    }
  }
}
```

**Características:**
- ✅ Una responsabilidad por clase (SRP)
- ✅ Depende de interfaces, no implementaciones (DIP)
- ✅ Retorna `Result<T>` para manejo explícito de errores
- ✅ Usa DTOs para comunicación

#### 2. Repositories (Interfaces) (`repositories/`)
**¿Qué son?** Contratos (puertos) que definen cómo acceder a datos.

```typescript
export interface IMovementRepository {
  create(data: CreateMovementData): Promise<Movement>;
  findById(id: string): Promise<Movement | null>;
  findAll(filters?: MovementFilters): Promise<Movement[]>;
  update(id: string, data: UpdateMovementData): Promise<Movement>;
  delete(id: string): Promise<void>;
  getTotalBalance(userId?: string): Promise<number>;
}
```

**¿Por qué interfaces?**
- ✅ Inversión de dependencias (DIP)
- ✅ Fácil de testear (mocks)
- ✅ Cambiar implementación sin tocar use cases

#### 3. DTOs (`dtos/`)
**¿Qué son?** Objetos para transferir datos entre capas.

```typescript
export interface CreateMovementRequest {
  type: MovementType;
  amount: number;
  concept: string;
  date: Date;
  userId: string;
}

export interface CreateMovementResponse {
  id: string;
  type: MovementType;
  amount: number;
  concept: string;
  date: Date;
  userId: string;
  createdAt: Date;
  updatedAt: Date;
}
```

#### 4. Application Service (`ApplicationService.ts`)
**¿Qué es?** Facade que centraliza todos los use cases.

```typescript
class ApplicationService {
  private readonly movementRepository = new PrismaMovementRepository();
  private readonly userRepository = new PrismaUserRepository();

  // Commands
  public readonly createMovement = new CreateMovementUseCase(this.movementRepository);
  public readonly deleteMovement = new DeleteMovementUseCase(this.movementRepository);
  
  // Queries
  public readonly getMovements = new GetMovementsUseCase(this.movementRepository);
  public readonly getBalance = new GetBalanceUseCase(this.movementRepository);
}

export const appService = new ApplicationService(); // Singleton
```

**Ventajas:**
- ✅ Punto de entrada único
- ✅ Inyección de dependencias centralizada
- ✅ Fácil de localizar casos de uso

---

## 🟧 CAPA 3: Infrastructure (Infraestructura)

### Responsabilidades
- **Implementa las interfaces de Application**
- **Conecta con servicios externos** (BD, APIs, email)
- **Contiene detalles técnicos**

### Componentes

#### 1. Repositorios Concretos (`repositories/`)
**Implementan las interfaces definidas en Application.**

```typescript
export class PrismaMovementRepository implements IMovementRepository {
  async create(data: CreateMovementData): Promise<Movement> {
    const prismaMovement = await prisma.movement.create({
      data: {
        type: data.type,
        amount: data.amount,
        concept: data.concept,
        date: data.date,
        userId: data.userId,
      },
      include: { user: true },
    });
    
    // Mapear de Prisma a entidad de dominio
    return Movement.create({
      id: prismaMovement.id,
      type: prismaMovement.type,
      amount: Number(prismaMovement.amount),
      concept: prismaMovement.concept,
      date: prismaMovement.date,
      userId: prismaMovement.userId,
      createdAt: prismaMovement.createdAt,
      updatedAt: prismaMovement.updatedAt,
    });
  }
  
  async findAll(filters?: MovementFilters): Promise<Movement[]> {
    const where: Prisma.MovementWhereInput = {};
    
    if (filters?.type) where.type = filters.type;
    if (filters?.startDate) where.date = { gte: filters.startDate };
    if (filters?.endDate) where.date = { ...where.date, lte: filters.endDate };
    
    const prismaMovements = await prisma.movement.findMany({
      where,
      include: { user: true },
      orderBy: { date: 'desc' },
    });
    
    return prismaMovements.map(pm => Movement.create({ ... }));
  }
}
```

**Características:**
- ✅ Conoce Prisma (detalles técnicos)
- ✅ Mapea entre tipos de Prisma y entidades de dominio
- ✅ Maneja transacciones de BD

#### 2. Prisma Client (`prisma/prismaClient.ts`)
```typescript
import { PrismaClient } from '@prisma/client';

const globalForPrisma = global as unknown as { prisma: PrismaClient };

export const prisma = globalForPrisma.prisma || new PrismaClient();

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma;
```

---

## 🟥 CAPA 4: Presentation (Presentación)

### Responsabilidades
- **API Routes de Next.js**
- **Validación de requests HTTP**
- **Middlewares** (auth, roles, errors)
- **Formato de respuestas**

### Componentes

#### 1. API Routes (`pages/api/`)
```typescript
// pages/api/movements/index.ts
const handler = async (req: NextApiRequest, res: NextApiResponse) => {
  if (req.method === 'GET') {
    const { type, startDate, endDate } = req.query;
    const filters = { type, startDate, endDate };
    
    const result = await appService.getMovements.execute(filters);
    
    if (result.isFailure) {
      return res.status(500).json(ApiResponse.error(result.error));
    }
    
    return res.status(200).json(ApiResponse.success(result.value));
  }
  
  if (req.method === 'POST') {
    // Validación de rol
    if (req.user?.role !== 'ADMIN') {
      return res.status(403).json(ApiResponse.forbidden());
    }
    
    const result = await appService.createMovement.execute(req.body);
    // ...
  }
};

export default withAuth(withErrorHandling(handler));
```

#### 2. Middlewares (`presentation/middlewares/`)

**withAuth**: Verifica que el usuario esté autenticado
```typescript
export function withAuth(handler: NextApiHandler): NextApiHandler {
  return async (req, res) => {
    const session = await getSession(req);
    
    if (!session) {
      return res.status(401).json(ApiResponse.unauthorized());
    }
    
    req.user = session.user;
    return handler(req, res);
  };
}
```

**withRole**: Verifica que el usuario tenga el rol requerido
```typescript
export function withRole(roles: string[]) {
  return (handler: NextApiHandler): NextApiHandler => {
    return async (req, res) => {
      if (!roles.includes(req.user.role)) {
        return res.status(403).json(ApiResponse.forbidden());
      }
      return handler(req, res);
    };
  };
}
```

**withErrorHandling**: Captura errores no manejados
```typescript
export function withErrorHandling(handler: NextApiHandler): NextApiHandler {
  return async (req, res) => {
    try {
      return await handler(req, res);
    } catch (error) {
      console.error(error);
      return res.status(500).json(ApiResponse.error('Internal server error'));
    }
  };
}
```

---

## 🔄 Flujo de Datos Completo

### Ejemplo: Crear un Movimiento

```
┌──────────────┐
│   USUARIO    │
│  (Frontend)  │
└──────┬───────┘
       │ 1. POST /api/movements
       │    { type, amount, concept, date }
       ▼
┌────────────────────────────────────────┐
│   API Route (pages/api/movements)      │
│                                        │
│  2. withAuth: Verifica sesión         │
│  3. withRole: Verifica rol ADMIN      │
│  4. Validación de request             │
└──────┬─────────────────────────────────┘
       │ 5. appService.createMovement.execute(data)
       ▼
┌────────────────────────────────────────┐
│   CreateMovementUseCase                │
│                                        │
│  6. Validación de lógica de negocio   │
│  7. repository.create(data)           │
└──────┬─────────────────────────────────┘
       │
       ▼
┌────────────────────────────────────────┐
│   PrismaMovementRepository             │
│                                        │
│  8. Construir entidad Movement        │
│     - Valida Money (amount)           │
│     - Valida Concept                  │
│     - Valida MovementType             │
│  9. prisma.movement.create()          │
│  10. Lanza MovementCreatedEvent       │
└──────┬─────────────────────────────────┘
       │
       ▼
┌────────────────────────────────────────┐
│   PostgreSQL                           │
│                                        │
│  11. INSERT INTO movement ...         │
└──────┬─────────────────────────────────┘
       │ 12. Retorna entidad creada
       ▼
       (Retorna por todas las capas)
       │
       ▼
┌────────────────────────────────────────┐
│   API Response                         │
│                                        │
│  13. { success: true, data: {...} }   │
└──────┬─────────────────────────────────┘
       │
       ▼
┌──────────────┐
│   USUARIO    │
│  (Frontend)  │
└──────────────┘
```

---

## 🎯 Principios SOLID Aplicados

### 1. **S**ingle Responsibility Principle (SRP)
- ✅ Cada use case tiene UNA responsabilidad
- ✅ Cada capa tiene su propósito específico

### 2. **O**pen/Closed Principle (OCP)
- ✅ Extender comportamiento sin modificar código existente
- ✅ Nuevos use cases no cambian Application Service

### 3. **L**iskov Substitution Principle (LSP)
- ✅ Implementaciones de repositorios son intercambiables

### 4. **I**nterface Segregation Principle (ISP)
- ✅ Interfaces pequeñas y específicas

### 5. **D**ependency Inversion Principle (DIP)
- ✅ Application depende de interfaces, no de implementaciones concretas
- ✅ Domain no conoce detalles de infraestructura

---

## 📚 Continúa Leyendo

➡️ **Siguiente documento**: [03 - Patrones de Diseño](./03-PATRONES-DISENO.md)

---

**Última actualización:** Febrero 2026
