# 3️⃣ Patrones de Diseño

## 🎨 Introducción

Este proyecto implementa múltiples patrones de diseño que trabajan en conjunto para crear una arquitectura robusta, mantenible y escalable.

Cada patrón incluye:
- 🟢 **Explicación simple** - Analogía fácil de entender
- 🔵 **Explicación técnica** - Definición formal
- 💻 **Implementación** - Código del proyecto

---

## 📋 Índice de Patrones Implementados

1. [Repository Pattern](#1-repository-pattern)
2. [CQRS (Command Query Responsibility Segregation)](#2-cqrs-command-query-responsibility-segregation)
3. [Domain Events Pattern](#3-domain-events-pattern)
4. [Value Object Pattern](#4-value-object-pattern)
5. [Factory Pattern](#5-factory-pattern)
6. [Result Pattern](#6-result-pattern)
7. [Dependency Injection](#7-dependency-injection)
8. [Facade Pattern](#8-facade-pattern)
9. [Strategy Pattern](#9-strategy-pattern)
10. [Middleware Pattern](#10-middleware-pattern)

---

## 1. Repository Pattern

### 🟢 Explicación Simple
> **Analogía**: Es como un bibliotecario que sabe dónde están todos los libros. Tú le pides "dame el libro de Juan" y él te lo trae, sin que tú tengas que saber en qué estante está.
>
> El repositorio es el intermediario que sabe cómo guardar y buscar datos. Tu código solo dice "guárdame esto" o "tráeme aquello", sin saber si los datos están en PostgreSQL, MongoDB, o un archivo.

### 🔵 Explicación Técnica
Patrón de diseño de la capa de persistencia descrito por Martin Fowler en "Patterns of Enterprise Application Architecture" (2002). Implementa una abstracción entre el dominio y la capa de datos, proporcionando una interfaz tipo colección (Collection-like) que permite al código de negocio trabajar con objetos de dominio sin conocer los detalles de persistencia. Esto permite cumplir con el Principio de Inversión de Dependencias (DIP) de SOLID.

### 🎯 Propósito
Abstraer el acceso a datos y proporcionar una interfaz tipo "colección" para trabajar con entidades de dominio.

### ✅ Ventajas
- Desacopla el dominio de la persistencia
- Facilita el testing (mocks)
- Permite cambiar la BD sin afectar el dominio
- Centraliza la lógica de acceso a datos

### 📝 Implementación

#### Paso 1: Definir la interfaz (Application Layer)
```typescript
// lib/server/application/repositories/IMovementRepository.ts
export interface IMovementRepository {
  create(data: CreateMovementData): Promise<Movement>;
  findById(id: string): Promise<Movement | null>;
  findAll(filters?: MovementFilters): Promise<Movement[]>;
  update(id: string, data: UpdateMovementData): Promise<Movement>;
  delete(id: string): Promise<void>;
  getTotalBalance(userId?: string): Promise<number>;
  getTotalIncome(userId?: string): Promise<number>;
  getTotalExpense(userId?: string): Promise<number>;
}
```

#### Paso 2: Implementar con tecnología específica (Infrastructure Layer)
```typescript
// lib/server/infrastructure/repositories/PrismaMovementRepository.ts
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
    
    return this.toDomain(prismaMovement);
  }
  
  private toDomain(prismaMovement: any): Movement {
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
}
```

#### Paso 3: Usar en Use Cases
```typescript
export class CreateMovementUseCase {
  constructor(private repository: IMovementRepository) {} // ← Interfaz, no implementación
  
  async execute(input: CreateMovementRequest): Promise<Result<CreateMovementResponse>> {
    const movement = await this.repository.create(input);
    return Result.ok(movement);
  }
}
```

### 🔄 Flujo del Patrón
```
Use Case
    ↓ usa
IMovementRepository (interfaz)
    ↑ implementa
PrismaMovementRepository
    ↓ usa
Prisma ORM
    ↓ usa
PostgreSQL
```

### 🎓 Variante: En Memoria (Para Testing)
```typescript
export class InMemoryMovementRepository implements IMovementRepository {
  private movements: Movement[] = [];
  
  async create(data: CreateMovementData): Promise<Movement> {
    const movement = Movement.create({ ...data, id: uuid() });
    this.movements.push(movement);
    return movement;
  }
  
  async findAll(): Promise<Movement[]> {
    return this.movements;
  }
}

// En test
const repository = new InMemoryMovementRepository();
const useCase = new CreateMovementUseCase(repository);
```

---

## 2. CQRS (Command Query Responsibility Segregation)

### 🟢 Explicación Simple
> **Analogía**: En un restaurante, hay personas que toman pedidos (comandos/escritura) y personas que entregan comida (consultas/lectura). Separarlos hace que cada equipo sea más eficiente.
>
> En código: separamos las operaciones que MODIFICAN datos (crear, actualizar, eliminar) de las que SOLO LEEN. Así podemos optimizar cada tipo por separado.

### 🔵 Explicación Técnica
Patrón arquitectónico propuesto por Greg Young (2010), derivado del principio CQS (Command-Query Separation) de Bertrand Meyer. Segrega la responsabilidad de modelos de lectura (Query) y escritura (Command) en objetos separados. Permite optimización independiente ya que las escrituras pueden usar un modelo normalizado mientras las lecturas usan modelos desnormalizados optimizados para consultas.

### 🎯 Propósito
Separar las operaciones de **escritura** (Commands) de las de **lectura** (Queries).

### ✅ Ventajas
- Optimización independiente (lectura vs escritura)
- Escalabilidad: bases de datos separadas si es necesario
- Claridad: intent explícito (comando vs consulta)
- Seguridad: diferentes permisos para leer/escribir

### 📝 Implementación

#### Estructura de Carpetas
```
use-cases/
├── movements/
│   ├── commands/          # Comandos (ESCRITURA)
│   │   ├── CreateMovementUseCase.ts
│   │   └── DeleteMovementUseCase.ts
│   ├── queries/           # Consultas (LECTURA)
│   │   ├── GetMovementsUseCase.ts
│   │   └── GetBalanceUseCase.ts
│   └── dtos/
└── users/
    ├── commands/
    │   ├── UpdateUserUseCase.ts
    │   └── DeleteUserUseCase.ts
    └── queries/
        └── GetUsersUseCase.ts
```

#### Commands (Escritura)
```typescript
// CreateMovementUseCase.ts - COMMAND
export class CreateMovementUseCase {
  async execute(input: CreateMovementRequest): Promise<Result<CreateMovementResponse>> {
    // 1. Validación
    // 2. Creación en BD
    // 3. Lanzar eventos
    const movement = await this.repository.create(input);
    return Result.ok(movement);
  }
}
```

#### Queries (Lectura)
```typescript
// GetMovementsUseCase.ts - QUERY
export class GetMovementsUseCase {
  async execute(filters?: MovementFilters): Promise<Result<MovementQueryResponse[]>> {
    // Solo lectura, sin side-effects
    const movements = await this.repository.findAll(filters);
    return Result.ok(movements);
  }
}
```

### 🔮 Evolución Futura: CQRS Completo
```
┌─────────────────────────┐
│  Commands               │
│  (Escritura)            │
│  ↓                      │
│  PostgreSQL (Write DB)  │
│  ↓                      │
│  Domain Events          │
│  ↓                      │
│  Event Bus              │
└─────────────────────────┘
            ↓
            ↓ sincroniza
            ↓
┌─────────────────────────┐
│  Queries                │
│  (Lectura)              │
│  ↓                      │
│  MongoDB/Redis (Read DB)│
└─────────────────────────┘
```

---

## 3. Domain Events Pattern

### 🟢 Explicación Simple
> **Analogía**: Es como un grupo de WhatsApp donde avisas "ya llegué al restaurante" y todos los interesados reciben la notificación. No tienes que llamar a cada uno individualmente.
>
> Cuando algo importante pasa (un movimiento se crea), se "anuncia" a todo el sistema. Cualquier parte interesada puede escuchar y reaccionar (enviar email, actualizar estadísticas, etc.).

### 🔵 Explicación Técnica
Patrón descrito por Eric Evans en "Domain-Driven Design" (2003). Un Domain Event representa algo que sucedió en el dominio que es de interés para otros dominios. Permite desacoplar componentes usando el principio de publicar-suscribir (Pub/Sub). Es fundamental para comunicación entre Aggregates, audit trails, y es la base del Event Sourcing.

### 🎯 Propósito
Notificar a otras partes del sistema cuando algo importante sucede en el dominio.

### ✅ Ventajas
- Desacopla agregados
- Facilita auditoría
- Habilita side-effects (emails, notificaciones)
- Base para Event Sourcing

### 📝 Implementación

#### Paso 1: Clase Base
```typescript
// lib/server/domain/events/DomainEvent.ts
export abstract class DomainEvent {
  abstract eventName(): string;
  timestamp = new Date();
}
```

#### Paso 2: Eventos Específicos
```typescript
// lib/server/domain/events/MovementEvents.ts
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

export class MovementDeletedEvent extends DomainEvent {
  eventName() { return 'MovementDeleted'; }
  
  constructor(public readonly movementId: string) {
    super();
  }
}
```

#### Paso 3: Dispatcher
```typescript
// lib/server/domain/events/index.ts
export class DomainEventDispatcher {
  private static handlers: Map<string, ((event: DomainEvent) => void)[]> = new Map();
  
  static subscribe(eventName: string, handler: (event: DomainEvent) => void) {
    const handlers = this.handlers.get(eventName) || [];
    handlers.push(handler);
    this.handlers.set(eventName, handlers);
  }
  
  static dispatch(event: DomainEvent): void {
    console.log(`[Event] ${event.eventName()}`, event);
    
    const handlers = this.handlers.get(event.eventName()) || [];
    handlers.forEach(handler => handler(event));
  }
}
```

#### Paso 4: Uso en Entidades
```typescript
// lib/server/domain/entities/Movement.ts
export class Movement {
  static create(props: {...}): Movement {
    const movement = new Movement(...);
    
    // Lanzar evento
    DomainEventDispatcher.dispatch(
      new MovementCreatedEvent(
        movement.id,
        movement.type,
        movement.amount,
        movement.userId,
        movement.date
      )
    );
    
    return movement;
  }
}
```

#### Paso 5: Handlers (Opcional)
```typescript
// Registrar handler
DomainEventDispatcher.subscribe('MovementCreated', (event: MovementCreatedEvent) => {
  // Enviar email
  // Actualizar estadísticas
  // Notificar a otros sistemas
  console.log('Movement created:', event.movementId);
});
```

---

## 4. Value Object Pattern

### 🟢 Explicación Simple
> **Analogía**: Piensa en un billete de $100. No te importa cuál billete específico tienes, solo te importa que vale $100. Un billete de $100 es igual a cualquier otro billete de $100.
>
> Lo mismo con Email, Money, Phone en el código: no tienen identidad única, solo valor. `$100 === $100`, sin importar "cuál" $100 sea.

### 🔵 Explicación Técnica
Concepto de Domain-Driven Design (Eric Evans, 2003). Un Value Object es un objeto inmutable que se define por sus atributos, no por una identidad única. Dos Value Objects son iguales si todos sus atributos son iguales. Encapsulan validación y comportamiento relacionado al concepto que representan. Son fundamentales para un modelo de dominio rico (Rich Domain Model).

### 🎯 Propósito
Representar conceptos del dominio que no tienen identidad, solo valor.

### ✅ Ventajas
- Encapsula validación
- Inmutabilidad
- Código autodocumentado
- Reutilización

### 📝 Implementación

#### Ejemplo 1: Money
```typescript
export class Money {
  private readonly _amount: number;
  private static readonly MAX_AMOUNT = 999999999.99;
  private static readonly DECIMALS = 2;

  private constructor(amount: number) {
    this._amount = amount;
  }

  static create(amount: number): Money {
    if (typeof amount !== 'number' || isNaN(amount)) {
      throw new Error('El monto debe ser un número válido');
    }
    if (amount < 0) {
      throw new Error('El monto no puede ser negativo');
    }
    if (amount > Money.MAX_AMOUNT) {
      throw new Error(`El monto no puede ser mayor a ${Money.MAX_AMOUNT}`);
    }
    
    const rounded = Math.round(amount * 100) / 100;
    return new Money(rounded);
  }

  get amount(): number {
    return this._amount;
  }

  add(other: Money): Money {
    return Money.create(this._amount + other._amount);
  }

  subtract(other: Money): Money {
    const result = this._amount - other._amount;
    if (result < 0) throw new Error('Resultado negativo');
    return Money.create(result);
  }

  equals(other: Money): boolean {
    return this._amount === other._amount;
  }
}
```

#### Ejemplo 2: Email
```typescript
export class Email {
  private readonly _value: string;
  private static readonly REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  private constructor(value: string) {
    this._value = value;
  }

  static create(value: string): Email {
    const cleaned = value.trim().toLowerCase();
    
    if (!cleaned) {
      throw new Error('El email no puede estar vacío');
    }
    
    if (!Email.REGEX.test(cleaned)) {
      throw new Error('Email inválido');
    }
    
    return new Email(cleaned);
  }

  get value(): string {
    return this._value;
  }

  equals(other: Email): boolean {
    return this._value === other._value;
  }
}
```

#### Características Clave
```typescript
// ✅ Constructor privado
private constructor(value: T) { }

// ✅ Factory method con validación
static create(value: T): ValueObject { }

// ✅ Inmutabilidad (solo getters, no setters)
get value(): T { return this._value; }

// ✅ Operaciones retornan nuevas instancias
add(other: Money): Money {
  return Money.create(this._amount + other._amount);
}

// ✅ Comparación por valor
equals(other: ValueObject): boolean {
  return this._value === other._value;
}
```

---

## 5. Factory Pattern

### 🟢 Explicación Simple
> **Analogía**: Es como una fábrica de autos que ensambla todas las piezas por ti. Tú no tienes que saber cómo se construye el motor o se montan las ruedas, solo dices "quiero un Toyota rojo" y la fábrica lo arma completo.
>
> En código: en lugar de `new Movement(...)` con muchos parámetros, usas `Movement.create(props)` que hace todas las validaciones y configuraciones internas.

### 🔵 Explicación Técnica
Patrón creacional del libro "Gang of Four" (1994). Factory Method define una interfaz para crear objetos, pero deja que las subclases decidan qué clase instanciar. En nuestra implementación usamos la variante "Static Factory Method" dentro de la misma clase, que encapsula la lógica de construcción y validación, permitiendo también lanzar Domain Events en el momento de creación.

### 🎯 Propósito
Encapsular la lógica de creación de objetos complejos.

### 📝 Implementación

```typescript
export class Movement {
  // Constructor privado o protegido
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
    this._type = MovementTypeVO.fromString(typeValue);
    this._amount = Money.create(amountValue);
    this._concept = Concept.create(conceptValue);
  }

  // Factory method (punto de entrada recomendado)
  static create(props: {
    id: string;
    type: MovementType;
    amount: number;
    concept: string;
    date: Date;
    userId: string;
    createdAt: Date;
    updatedAt: Date;
  }): Movement {
    // Validaciones adicionales antes de construir
    if (!props.id) throw new Error('ID requerido');
    if (!props.userId) throw new Error('UserID requerido');
    
    const movement = new Movement(
      props.id,
      props.type,
      props.amount,
      props.concept,
      props.date,
      props.userId,
      props.createdAt,
      props.updatedAt
    );

    // Lanzar eventos
    DomainEventDispatcher.dispatch(
      new MovementCreatedEvent(...)
    );

    return movement;
  }
}
```

### ✅ Ventajas
- ✅ Punto de creación único y claro
- ✅ Validaciones centralizadas
- ✅ Facilita lanzar eventos
- ✅ Flexibilidad para crear variantes (ej: `createFromPrisma()`)

---

## 6. Result Pattern

### 🟢 Explicación Simple
> **Analogía**: En lugar de que una operación "explote" cuando algo sale mal (excepción), te devuelve una caja que dice claramente "éxito" o "error" con un mensaje.
>
> Es como pedir un paquete: en lugar de que el repartidor desaparezca si no encuentra tu casa, te deja una nota diciendo "no pude entregar porque: dirección no encontrada".

### 🔵 Explicación Técnica
Patrón inspirado en lenguajes funcionales (Result/Either en Rust, Scala, Haskell). Implementa el concepto de "Railway-Oriented Programming" donde las funciones retornan un objeto que encapsula éxito o fallo. Evita el uso de excepciones para control de flujo (antipatrón), hace explícito el manejo de errores en el sistema de tipos, y fuerza al llamador a manejar ambos casos.

### 🎯 Propósito
Manejo explícito de errores sin excepciones (alternativa a try-catch en ciertos casos).

### ✅ Ventajas
- Código autodocumentado (retorno explícito de éxito/error)
- Evita excepciones no capturadas
- Type-safe con TypeScript
- Facilita testing

### 📝 Implementación

```typescript
// lib/server/application/shared/Result.ts
export class Result<T> {
  private constructor(
    private readonly _isSuccess: boolean,
    private readonly _value?: T,
    private readonly _error?: string,
    private readonly _errors?: string[]
  ) {}

  get isSuccess(): boolean {
    return this._isSuccess;
  }

  get isFailure(): boolean {
    return !this._isSuccess;
  }

  get value(): T {
    if (!this._isSuccess) {
      throw new Error('Cannot get value from failed result');
    }
    return this._value!;
  }

  get error(): string {
    return this._error || '';
  }

  get errors(): string[] {
    return this._errors || [];
  }

  static ok<U>(value: U): Result<U> {
    return new Result<U>(true, value);
  }

  static fail<U>(error: string): Result<U> {
    return new Result<U>(false, undefined, error, [error]);
  }

  static failWithErrors<U>(errors: string[]): Result<U> {
    return new Result<U>(false, undefined, errors[0], errors);
  }
}
```

### 🔧 Uso

```typescript
// En Use Case
export class CreateMovementUseCase {
  async execute(input: CreateMovementRequest): Promise<Result<CreateMovementResponse>> {
    try {
      const movement = await this.repository.create(input);
      return Result.ok(movement); // ✅ Éxito
    } catch (error) {
      return Result.fail((error as Error).message); // ❌ Error
    }
  }
}

// En API Route
const result = await appService.createMovement.execute(data);

if (result.isFailure) {
  return res.status(400).json({ error: result.error });
}

return res.status(201).json({ data: result.value });
```

### 🎯 Cuándo Usar
- ✅ Errores de negocio esperados (validación, reglas)
- ❌ Errores técnicos inesperados (mejor usar try-catch)

---

## 7. Dependency Injection

### 🟢 Explicación Simple
> **Analogía**: En lugar de que un chef cultive sus propias verduras, el restaurante se las entrega. El chef no depende de saber cultivar, solo de cocinar con lo que le llega.
>
> En código: en lugar de que una clase cree sus propias dependencias (`new Database()`), se las pasamos desde afuera. Así podemos cambiar la dependencia sin tocar la clase.

### 🔵 Explicación Técnica
Técnica de Inversión de Control (IoC) donde las dependencias de un componente son suministradas externamente en lugar de ser instanciadas internamente. Implementa el Principio de Inversión de Dependencias (DIP) de SOLID. Puede implementarse manualmente (constructor injection) o con contenedores IoC (InversifyJS, tsyringe). El proyecto usa inyección manual a través de constructores.

### 🎯 Propósito
Inyectar dependencias en lugar de crearlas dentro de la clase.

### ✅ Ventajas
- Desacoplamiento
- Testabilidad (mocks fáciles)
- Flexibilidad

### 📝 Implementación

#### Manual (Usado en el proyecto)
```typescript
// ❌ MAL: Dependencia hardcodeada
export class CreateMovementUseCase {
  private repository = new PrismaMovementRepository(); // ← Acoplamiento
}

// ✅ BIEN: Inyección en constructor
export class CreateMovementUseCase {
  constructor(private repository: IMovementRepository) {} // ← Interfaz
}

// Uso
const repository = new PrismaMovementRepository();
const useCase = new CreateMovementUseCase(repository);
```

#### Centralizado en ApplicationService
```typescript
class ApplicationService {
  // Repositorios (pueden ser configurables)
  private readonly movementRepository = new PrismaMovementRepository();
  private readonly userRepository = new PrismaUserRepository();

  // Use Cases con inyección
  public readonly createMovement = new CreateMovementUseCase(
    this.movementRepository
  );
  
  public readonly getMovements = new GetMovementsUseCase(
    this.movementRepository
  );
}
```

---

## 8. Facade Pattern

### 🟢 Explicación Simple
> **Analogía**: Es como la recepción de un hotel. Tú solo hablas con el recepcionista para todo: habitación, restaurante, taxi. Él conoce toda la complejidad del hotel y te simplifica la vida.
>
> `ApplicationService` es nuestra recepción: un solo punto donde accedes a todos los use cases sin saber cómo están conectados internamente.

### 🔵 Explicación Técnica
Patrón estructural del libro "Gang of Four" (1994). Proporciona una interfaz unificada a un conjunto de interfaces de un subsistema. Define una interfaz de alto nivel que hace que el subsistema sea más fácil de usar. Reduce el acoplamiento entre clientes y la complejidad interna del sistema.

### 🎯 Propósito
Proporcionar una interfaz simplificada a un sistema complejo.

### 📝 Implementación

```typescript
// ApplicationService actúa como Facade
class ApplicationService {
  // Oculta la complejidad de repositorios y use cases
  public readonly createMovement = new CreateMovementUseCase(...);
  public readonly deleteMovement = new DeleteMovementUseCase(...);
  public readonly getMovements = new GetMovementsUseCase(...);
  public readonly getBalance = new GetBalanceUseCase(...);
  
  public readonly updateUser = new UpdateUserUseCase(...);
  public readonly deleteUser = new DeleteUserUseCase(...);
  public readonly getUsers = new GetUsersUseCase(...);
}

export const appService = new ApplicationService(); // Singleton

// Uso simple
const result = await appService.createMovement.execute(data);
```

### ✅ Ventajas
- ✅ Punto de entrada único
- ✅ Oculta complejidad interna
- ✅ Fácil de usar para API Routes

---

## 9. Strategy Pattern

### 🟢 Explicación Simple
> **Analogía**: Es como tener varios métodos de pago: efectivo, tarjeta, Bitcoin. El cajero no cambia su proceso, solo "enchufa" el método de pago que elijas.
>
> En nuestro código: el mismo Use Case puede usar PostgreSQL hoy y MongoDB mañana. Solo "enchufamos" el repositorio correcto sin cambiar la lógica de negocio.

### 🔵 Explicación Técnica
Patrón comportamental del libro "Gang of Four" (1994). Define una familia de algoritmos, encapsula cada uno, y los hace intercambiables. Strategy permite que el algoritmo varíe independientemente de los clientes que lo usan. En nuestro proyecto, se implementa implícitamente a través del Repository Pattern donde diferentes implementaciones pueden ser intercambiadas.

### 🎯 Propósito
Encapsular algoritmos intercambiables.

### 📝 Implementación (Implícita con Repositories)

```typescript
// Estrategia 1: PostgreSQL
class PrismaMovementRepository implements IMovementRepository {
  async findAll(): Promise<Movement[]> {
    return prisma.movement.findAll();
  }
}

// Estrategia 2: MongoDB (futuro)
class MongoMovementRepository implements IMovementRepository {
  async findAll(): Promise<Movement[]> {
    return mongoClient.collection('movements').find().toArray();
  }
}

// Estrategia 3: In-Memory (testing)
class InMemoryMovementRepository implements IMovementRepository {
  private movements: Movement[] = [];
  async findAll(): Promise<Movement[]> {
    return this.movements;
  }
}

// Uso (intercambiable)
const useCase = new GetMovementsUseCase(new PrismaMovementRepository());
// o
const useCase = new GetMovementsUseCase(new InMemoryMovementRepository());
```

---

## 10. Middleware Pattern

### 🟢 Explicación Simple
> **Analogía**: Es como pasar por seguridad en un aeropuerto: primero verifican tu pasaporte, luego escanean tu maleta, luego te revisan. Cada estación hace UNA cosa y te pasa a la siguiente.
>
> En código: cada request pasa por varios "filtros": primero `withAuth` verifica login, luego `withRole` verifica permisos, luego `withErrorHandling` captura errores. Cada middleware hace una cosa y pasa el control al siguiente.

### 🔵 Explicación Técnica
Variante del patrón "Chain of Responsibility" del libro "Gang of Four" (1994), popularizado en frameworks web como Express.js. Cada middleware es un Higher-Order Function (HOF) que envuelve al handler, permitiendo ejecutar código antes y/o después de la lógica principal. Los middlewares se componen de forma anidada, creando una "cebolla" donde el request atraviesa capas de entrada y salida.

### 🎯 Propósito
Cadena de responsabilidades para procesar requests.

### 📝 Implementación

```typescript
// Middleware 1: Auth
export function withAuth(handler: NextApiHandler): NextApiHandler {
  return async (req, res) => {
    const session = await getSession(req);
    if (!session) return res.status(401).json({ error: 'Unauthorized' });
    req.user = session.user;
    return handler(req, res);
  };
}

// Middleware 2: Role
export function withRole(roles: string[]) {
  return (handler: NextApiHandler): NextApiHandler => {
    return async (req, res) => {
      if (!roles.includes(req.user.role)) {
        return res.status(403).json({ error: 'Forbidden' });
      }
      return handler(req, res);
    };
  };
}

// Middleware 3: Error Handling
export function withErrorHandling(handler: NextApiHandler): NextApiHandler {
  return async (req, res) => {
    try {
      return await handler(req, res);
    } catch (error) {
      console.error(error);
      return res.status(500).json({ error: 'Internal server error' });
    }
  };
}

// Composición
export default withAuth(
  withRole(['ADMIN'])(
    withErrorHandling(handler)
  )
);
```

---

## 📊 Resumen de Patrones

| Patrón | Capa | Propósito Principal |
|--------|------|---------------------|
| **Repository** | Infrastructure | Abstracción de persistencia |
| **CQRS** | Application | Separar lectura de escritura |
| **Domain Events** | Domain | Comunicación desacoplada |
| **Value Object** | Domain | Validación encapsulada |
| **Factory** | Domain | Creación controlada |
| **Result** | Application | Manejo explícito de errores |
| **Dependency Injection** | Todas | Desacoplamiento |
| **Facade** | Application | Interfaz simplificada |
| **Strategy** | Infrastructure | Algoritmos intercambiables |
| **Middleware** | Presentation | Cadena de responsabilidades |

---

## 📚 Continúa Leyendo

➡️ **Siguiente documento**: [04 - Atributos de Calidad](./04-ATRIBUTOS-CALIDAD.md)

---

**Última actualización:** Febrero 2026
