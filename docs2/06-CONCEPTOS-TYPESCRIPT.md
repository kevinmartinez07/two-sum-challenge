# 📘 Conceptos de TypeScript/JavaScript Usados

## 🎯 Introducción

Este documento explica patrones y conceptos de TypeScript/JavaScript que usamos en el proyecto. Cada concepto tiene:
- 🟢 **Explicación Simple** - Para entender el concepto rápidamente
- 🔵 **Explicación Técnica** - Detalles profundos y terminología correcta
- 💻 **Ejemplos del Proyecto** - Código real de esta aplicación

---

## 📋 Índice

1. [Barrel Exports (index.ts)](#1-barrel-exports-indexts)
2. [Path Aliases (@/)](#2-path-aliases-)
3. [Type Annotations](#3-type-annotations)
4. [Generics](#4-generics)
5. [Interfaces vs Types](#5-interfaces-vs-types)
6. [Async/Await y Promises](#6-asyncawait-y-promises)
7. [Destructuring](#7-destructuring)
8. [Optional Chaining (?.)](#8-optional-chaining-)
9. [Nullish Coalescing (??)](#9-nullish-coalescing-)
10. [Export Default vs Named Exports](#10-export-default-vs-named-exports)
11. [Clases en TypeScript](#11-clases-en-typescript)
12. [Modificadores de Acceso](#12-modificadores-de-acceso)
13. [readonly y const](#13-readonly-y-const)
14. [Union Types y Literal Types](#14-union-types-y-literal-types)
15. [Type Guards](#15-type-guards)

---

## 1. Barrel Exports (index.ts)

### 🟢 Explicación Simple

**Analogía:** Imagina una tienda con muchos productos. En lugar de decirle al cliente "ve al pasillo 3, estante 2, sección B para el champú", simplemente dices "ve a productos de higiene". El `index.ts` es como ese letrero que agrupa todo.

**¿Por qué hay `index.ts` en todas las carpetas?**

El archivo `index.ts` es un **punto de entrada único** que re-exporta todo lo de una carpeta. Así no necesitas saber exactamente dónde está cada archivo.

### 🔵 Explicación Técnica

El **Barrel Pattern** (o "Re-export Pattern") es una técnica de organización de módulos en JavaScript/TypeScript donde un archivo `index.ts` actúa como una **fachada pública** (Public API) para un módulo o carpeta.

**Principios que implementa:**
- **Encapsulamiento**: Oculta la estructura interna del módulo
- **Acoplamiento Bajo**: Los consumidores dependen del barrel, no de archivos específicos
- **Ley de Demeter**: "No hables con extraños" - interactúa solo con el punto de entrada

**Especificación técnica**: Según el algoritmo de resolución de módulos de Node.js (y TypeScript), cuando importas de una carpeta, automáticamente busca `index.{ts,js,tsx,jsx}`.

### 🔴 Problema SIN Barrel Export

```typescript
// ❌ Sin index.ts - Imports largos y frágiles
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { Modal } from '@/components/ui/Modal';
import { Badge } from '@/components/ui/Badge';
import { Input } from '@/components/ui/input';
```

**Problemas técnicos:**
- **Acoplamiento alto**: Conoces la estructura interna del módulo
- **Refactoring costoso**: Mover un archivo rompe N imports
- **Imports verbosos**: Líneas de código innecesarias
- **Autocompletado pobre**: IDE no sabe qué es "público"

### 🟢 Solución CON Barrel Export

**Archivo `components/ui/index.ts`:**
```typescript
// Re-exporta todo desde un solo lugar
export { Badge } from './Badge';
export { Button } from './Button';
export { Card, CardHeader, StatCard } from './Card';
export { Modal, ConfirmModal, AlertModal } from './Modal';
export { Input } from './input';
export { Label } from './label';
export { Select, SelectItem, SelectTrigger } from './select';
```

**Ahora puedes importar así:**
```typescript
// ✅ Con index.ts - Un solo import limpio
import { Button, Card, Modal, Badge, Input } from '@/components/ui';
```

### 💻 Ejemplos Reales del Proyecto

**1. Hooks (`hooks/index.ts`):**
```typescript
// Barrel export de todos los hooks
export { useAuth } from './useAuth';
export { useMovements } from './useMovements';
export { useUsers } from './useUsers';
export { useReports } from './useReports';
export { useRegister } from './useRegister';
export { useGithubAuth } from './useGithubAuth';

// Uso:
import { useAuth, useMovements } from '@/hooks';
```

**2. Services (`lib/client/services/index.ts`):**
```typescript
export { movementsService } from './movements.service';
export { usersService } from './users.service';
export { reportsService } from './reports.service';

// Uso:
import { movementsService, usersService } from '@/lib/client/services';
```

**3. Domain Events (`lib/server/domain/events/index.ts`):**
```typescript
export { DomainEvent } from './DomainEvent';
export { MovementCreatedEvent, MovementDeletedEvent } from './MovementEvents';
export { UserCreatedEvent, UserUpdatedEvent } from './UserEvents';
```

### 🎯 Resolución de Módulos - Cómo Funciona Internamente

```typescript
import { something } from '@/components/ui';
```

TypeScript/Node.js busca en este orden:
1. `@/components/ui.ts` - ¿Archivo directo? ❌
2. `@/components/ui.tsx` - ¿Archivo JSX? ❌
3. `@/components/ui/index.ts` - ✅ **Lo encuentra aquí**
4. `@/components/ui/index.js`
5. `@/components/ui/package.json` → `main` field

### 📁 Todos los Barrel Exports del Proyecto

| Archivo | Propósito | Qué exporta |
|---------|-----------|-------------|
| `components/ui/index.ts` | UI Kit | Badge, Button, Card, Modal, Input, etc. |
| `components/movements/index.ts` | Feature Movements | MovementForm, MovementTable, MovementRow |
| `components/users/index.ts` | Feature Users | UserTable, UserRow, UserEditForm |
| `components/reports/index.ts` | Feature Reports | Charts, stats, tables |
| `hooks/index.ts` | Custom Hooks | useAuth, useMovements, useUsers, etc. |
| `lib/client/services/index.ts` | API Services | movementsService, usersService |
| `lib/client/types/index.ts` | TypeScript Types | Todos los tipos del cliente |
| `lib/server/domain/events/index.ts` | Domain Events | Eventos del dominio |
| `lib/auth/index.ts` | Auth utilities | auth, signIn, signOut |

### 💡 Cuándo Crear un index.ts

✅ **CREAR cuando:**
- Tienes 3+ archivos relacionados en una carpeta
- Los archivos se importan frecuentemente juntos
- Quieres definir una API pública clara
- Quieres ocultar detalles de implementación

❌ **NO CREAR cuando:**
- Solo hay 1-2 archivos
- Cada archivo es independiente
- Es una carpeta de configuración (raíz)
- Causaría dependencias circulares

### ⚠️ Cuidado: Dependencias Circulares

```typescript
// ❌ PROBLEMA: Dependencia circular
// components/index.ts
export { ComponentA } from './ComponentA';
export { ComponentB } from './ComponentB';

// components/ComponentA.tsx
import { ComponentB } from './index'; // Circular!

// ✅ SOLUCIÓN: Import directo dentro del mismo módulo
// components/ComponentA.tsx
import { ComponentB } from './ComponentB'; // Directo, sin barrel
```

### 📝 Variantes de Re-exportación

```typescript
// Variante 1: Re-exportar específicamente (RECOMENDADO)
export { Button } from './Button';
export { Card } from './Card';

// Variante 2: Re-exportar todo (CUIDADO - exporta TODO)
export * from './Button';  // Incluye exports internos

// Variante 3: Re-exportar con alias
export { Button as PrimaryButton } from './Button';
export { default as Button } from './Button'; // Re-exportar default como named

// Variante 4: Re-exportar y añadir
export { Button } from './Button';
export { Card } from './Card';
export const VERSION = '1.0.0'; // Añadir algo nuevo al barrel
```

---

## 2. Path Aliases (@/)

### 🟢 Explicación Simple

**Analogía:** Es como tener un GPS con direcciones guardadas. En lugar de escribir "Calle Principal #123, Ciudad X, País Y", solo dices "ir a Casa". El `@/` es tu atajo para decir "desde la raíz del proyecto".

**¿Qué significa `@/` en los imports?**
Es un **atajo** configurado para evitar escribir rutas largas con muchos `../../../`.

### 🔵 Explicación Técnica

Los **Path Aliases** (o **Module Path Aliases**) son mapeos configurados en `tsconfig.json` que el compilador de TypeScript resuelve en tiempo de compilación. Transforman rutas virtuales en rutas reales del sistema de archivos.

**Configuración en `tsconfig.json` del proyecto:**
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

**Esto significa:**
- `baseUrl: "."` → La raíz para resolver paths es el directorio del proyecto
- `"@/*": ["./*"]` → `@/` se mapea a la raíz del proyecto
- El `*` es un wildcard que captura cualquier ruta después de `@/`

### 🔴 Problema SIN Path Alias

```typescript
// ❌ Imports relativos - Difíciles de leer y mantener
// Archivo: pages/api/movements/[id].ts
import { prisma } from '../../../lib/server/infrastructure/prisma/prismaClient';
import { Movement } from '../../../lib/server/domain/entities/Movement';
import { formatMoney } from '../../../lib/format';
import { useAuth } from '../../../hooks/useAuth';

// ¿Cuántos ../ necesitas? Depende de dónde estés 😵
```

**Problemas:**
- **Frágil**: Mover un archivo rompe todos sus imports
- **Confuso**: ¿Cuántos `../` necesitas?
- **Diff unfriendly**: Git diffs muestran cambios de imports innecesarios
- **Refactoring costoso**: Reorganizar carpetas es doloroso

### 🟢 Solución CON Path Alias

```typescript
// ✅ Imports con alias - Claros y estables
// Archivo: pages/api/movements/[id].ts
import { prisma } from '@/lib/server/infrastructure/prisma/prismaClient';
import { Movement } from '@/lib/server/domain/entities/Movement';
import { formatMoney } from '@/lib/format';
import { useAuth } from '@/hooks/useAuth';

// Siempre desde la raíz, sin importar dónde estés 🎯
```

### 💻 Ejemplos Reales del Proyecto

```typescript
// En cualquier archivo del proyecto:
import { useAuth } from '@/hooks';                    // hooks/index.ts
import { Button, Card } from '@/components/ui';       // components/ui/index.ts
import { movementsService } from '@/lib/client/services';
import { Movement } from '@/lib/server/domain/entities/Movement';
import { prisma } from '@/lib/server/infrastructure/prisma/prismaClient';
import { withAuth } from '@/lib/server/presentation/middlewares/withAuth';
```

### 🔧 Cómo Funciona la Resolución

**Cuando TypeScript ve:**
```typescript
import { Button } from '@/components/ui';
```

**Proceso de resolución:**
1. TypeScript lee `tsconfig.json`
2. Encuentra el mapeo `"@/*": ["./*"]`
3. Reemplaza `@/` con `./` (raíz del proyecto)
4. Resultado: `./components/ui`
5. Busca `./components/ui/index.ts`

### 📖 Otros Aliases Comunes (no usados aquí, pero útiles)

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"],                       // Raíz
      "@components/*": ["components/*"],    // Componentes
      "@hooks/*": ["hooks/*"],              // Hooks
      "@lib/*": ["lib/*"],                  // Librerías
      "@server/*": ["lib/server/*"],        // Atajo a server
      "@domain/*": ["lib/server/domain/*"], // Directo al dominio
      "@test/*": ["__tests__/*"]            // Tests
    }
  }
}
```

### ⚙️ Configuración Completa para Next.js

**Importante:** Next.js soporta path aliases nativamente. Solo necesitas `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "baseUrl": ".",           // 👈 IMPORTANTE
    "paths": {
      "@/*": ["./*"]          // 👈 El alias
    }
  }
}
```

### ⚠️ Errores Comunes

```typescript
// ❌ ERROR: Olvidar la barra
import { Button } from '@components/ui'; // Sin la /
// Solución: import { Button } from '@/components/ui';

// ❌ ERROR: Usar en archivo .js sin configuración
// Los archivos .js no entienden paths de TypeScript por defecto

// ❌ ERROR: Jest no resuelve el alias
// Solución: Configurar moduleNameMapper en jest.config.js
{
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1'
  }
}
```

---

## 3. Type Annotations

### 🟢 Explicación Simple

**Analogía:** Es como poner etiquetas a tus contenedores en la cocina. El contenedor dice "Azúcar" para que no lo confundas con sal. TypeScript etiqueta variables para que no confundas un número con un texto.

**¿Qué son los `: string`, `: number`, etc.?**
Son **etiquetas de tipo** que le dicen a TypeScript qué tipo de dato espera una variable o función. Si pones el tipo incorrecto, TypeScript te avisa ANTES de ejecutar el código.

### 🔵 Explicación Técnica

Las **Type Annotations** son metadatos estáticos que especifican el tipo de una expresión en TypeScript. Son verificadas en **tiempo de compilación** (compile-time) por el **type checker** y son completamente eliminadas en la transpilación a JavaScript (zero runtime cost).

**Características:**
- **Estáticas**: No existen en runtime
- **Inferidas**: TypeScript puede deducirlas automáticamente
- **Explícitas**: Puedes declararlas manualmente para claridad
- **Estructurales**: TypeScript usa "duck typing" (si parece pato y camina como pato...)

### 📝 Tipos Primitivos

```typescript
// Tipos básicos de JavaScript
const name: string = "Juan";           // Texto
const age: number = 25;                // Número (int o float, no hay distinción)
const isActive: boolean = true;        // Booleano
const nothing: null = null;            // Null explícito
const notDefined: undefined = undefined; // Undefined explícito

// 🔵 Técnico: TypeScript infiere tipos automáticamente
const inferredString = "Hola";  // TypeScript infiere: string
const inferredNumber = 42;      // TypeScript infiere: number
// No necesitas escribir `: string` si es obvio
```

### 📝 Arrays y Tuplas

```typescript
// Arrays - dos sintaxis equivalentes
const numbers: number[] = [1, 2, 3];
const names: Array<string> = ["Ana", "Luis"];  // Forma genérica

// Arrays mixtos (Union Type)
const mixed: (string | number)[] = ["Ana", 25, "Luis", 30];

// Tuplas - arrays de tamaño fijo con tipos específicos por posición
const coordinate: [number, number] = [10, 20];
const userTuple: [string, number, boolean] = ["Juan", 25, true];

// 🔵 Técnico: Las tuplas son útiles para retornos múltiples
// React useState retorna una tupla: [valor, setter]
const [count, setCount]: [number, (n: number) => void] = useState(0);
```

### 📝 Objetos

```typescript
// Objeto con shape explícito
const user: { name: string; age: number; email?: string } = {
  name: "Juan",
  age: 25
  // email es opcional (?)
};

// 🔵 Técnico: Record<K, V> para objetos dinámicos
const scores: Record<string, number> = {
  math: 95,
  science: 88,
  history: 92
};

// Index Signatures para propiedades dinámicas
interface Dictionary {
  [key: string]: string;
}
```

### 📝 Funciones

```typescript
// Función con tipos de parámetros y retorno
function greet(name: string): string {
  return `Hola ${name}`;
}

// Arrow function con tipos
const add = (a: number, b: number): number => a + b;

// Función que no retorna nada (void)
const logMessage = (msg: string): void => {
  console.log(msg);
};

// Función que nunca retorna (never)
const throwError = (msg: string): never => {
  throw new Error(msg);
};

// Parámetros opcionales y defaults
function createUser(
  name: string,
  age: number = 18,        // Default
  email?: string           // Opcional
): User {
  return { name, age, email };
}

// 🔵 Técnico: Function types
type ClickHandler = (event: MouseEvent) => void;
type Calculator = (a: number, b: number) => number;
```

### 📝 Async Functions y Promises

```typescript
// Promise con tipo genérico
const fetchData = (): Promise<string> => {
  return Promise.resolve("data");
};

// Async function - siempre retorna Promise
async function getUserById(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}

// 🔵 Técnico: Awaited<T> para extraer tipo de Promise
type ResolvedType = Awaited<Promise<string>>; // string
```

### 💻 Ejemplos del Proyecto

```typescript
// lib/server/domain/entities/Movement.ts
export class Movement {
  private readonly _type: MovementTypeVO;      // Value Object
  private _amount: Money;                       // Value Object
  private _concept: Concept;                    // Value Object

  constructor(
    public readonly id: string,                 // readonly = inmutable
    typeValue: MovementType,                    // Enum
    amountValue: number,                        // Primitivo
    conceptValue: string,                       // Primitivo
    public date: Date,                          // Date object
    public readonly userId: string,
    public readonly createdAt: Date,
    public updatedAt: Date
  ) { ... }
}

// hooks/useMovements.ts
const [movements, setMovements] = useState<Movement[]>([]);
const [error, setError] = useState<string | null>(null);
const [isLoading, setIsLoading] = useState<boolean>(false);
```

### 🎯 ¿Por Qué Usar Tipos?

```typescript
// ❌ Sin tipos (JavaScript puro) - Error en RUNTIME
function sum(a, b) {
  return a + b;
}
sum("10", 20); // "1020" - concatenación, no suma! 🐛
// No te enteras hasta que el usuario lo ve

// ✅ Con tipos (TypeScript) - Error en COMPILE TIME
function sum(a: number, b: number): number {
  return a + b;
}
sum("10", 20); // ❌ Error: Argument of type 'string' is not assignable
// TypeScript te avisa ANTES de ejecutar
```

### ⚠️ Cuándo Anotar Explícitamente

```typescript
// ✅ ANOTAR cuando TypeScript no puede inferir
function parseConfig(config: unknown): Config { ... }

// ✅ ANOTAR parámetros de funciones (siempre)
function greet(name: string): string { ... }

// ✅ ANOTAR APIs públicas para documentación
export function calculateBalance(movements: Movement[]): number { ... }

// ❌ NO ANOTAR cuando es obvio (dejar que infiera)
const name = "Juan";  // ✅ TypeScript infiere string
const name: string = "Juan";  // ❌ Redundante
```

---

## 4. Generics

### 🟢 Explicación Simple

**Analogía:** Es como una caja de "lo que sea". Puedes tener una "caja de juguetes", una "caja de libros", o una "caja de herramientas". La caja es la misma estructura, pero el contenido cambia. `<T>` es ese "lo que sea" que defines cuando usas la caja.

**¿Qué significa `<T>` en el código?**
Es un **placeholder** (marcador de posición) para un tipo que se especifica después. Permite crear funciones y clases que funcionan con CUALQUIER tipo.

### 🔵 Explicación Técnica

Los **Generics** (o **Type Parameters**) son una forma de escribir código **polimórfico parametrizado**. Permiten definir componentes que:
- Trabajan con múltiples tipos de datos
- Mantienen seguridad de tipos (type-safe)
- Evitan duplicación de código

**Terminología técnica:**
- `<T>` - Type parameter (por convención: T = Type, K = Key, V = Value, E = Element)
- **Generic constraint** - `<T extends SomeType>` limita qué tipos acepta T
- **Generic inference** - TypeScript deduce T del contexto

### 📝 Generics Básicos

```typescript
// ❌ Sin generics: Duplicación de código
function getFirstString(arr: string[]): string { return arr[0]; }
function getFirstNumber(arr: number[]): number { return arr[0]; }
function getFirstUser(arr: User[]): User { return arr[0]; }
// Necesitas N funciones para N tipos 😩

// ✅ Con generics: Una función universal
function getFirst<T>(arr: T[]): T {
  return arr[0];
}

// El tipo se especifica al llamar (o TypeScript lo infiere)
const firstString = getFirst<string>(["a", "b", "c"]); // T = string
const firstNumber = getFirst([1, 2, 3]);               // T inferido = number
const firstUser = getFirst<User>([user1, user2]);     // T = User
```

### 📝 Múltiples Type Parameters

```typescript
// Función con dos tipos genéricos
function makePair<K, V>(key: K, value: V): [K, V] {
  return [key, value];
}

const pair1 = makePair<string, number>("age", 25);  // ["age", 25]
const pair2 = makePair("name", "Juan");             // Inferido: [string, string]

// Map<K, V> es un ejemplo estándar
const userScores = new Map<string, number>();
userScores.set("Juan", 95);
```

### 📝 Generic Constraints

```typescript
// ❌ T puede ser cualquier cosa, incluso sin .length
function getLength<T>(item: T): number {
  return item.length; // Error: Property 'length' does not exist on type 'T'
}

// ✅ Constraint: T DEBE tener .length
function getLength<T extends { length: number }>(item: T): number {
  return item.length; // OK
}

getLength("hello");     // ✅ string tiene .length
getLength([1, 2, 3]);   // ✅ array tiene .length
getLength(123);         // ❌ Error: number no tiene .length
```

### 📝 Generics en Clases

```typescript
// Clase genérica
class Container<T> {
  private items: T[] = [];
  
  add(item: T): void {
    this.items.push(item);
  }
  
  get(index: number): T {
    return this.items[index];
  }
  
  getAll(): T[] {
    return this.items;
  }
}

// Uso
const numberContainer = new Container<number>();
numberContainer.add(1);
numberContainer.add(2);

const userContainer = new Container<User>();
userContainer.add(user1);
```

### 💻 Generics en el Proyecto

**1. Result Pattern (`lib/server/application/shared/Result.ts`):**
```typescript
export class Result<T> {
  private constructor(
    private readonly _isSuccess: boolean,
    private readonly _value?: T,
    private readonly _error?: string
  ) {}

  static ok<U>(value: U): Result<U> {
    return new Result<U>(true, value);
  }

  static fail<U>(error: string): Result<U> {
    return new Result<U>(false, undefined, error);
  }

  get value(): T {
    if (!this._isSuccess) throw new Error("Cannot get value of failed result");
    return this._value as T;
  }
}

// Uso en Use Cases
async execute(): Promise<Result<CreateMovementResponse>> {
  // T = CreateMovementResponse
  return Result.ok(response);  // Result<CreateMovementResponse>
}
```

**2. React useState Hook:**
```typescript
// useState es genérico: useState<T>(initialValue: T): [T, SetStateAction<T>]
const [movements, setMovements] = useState<Movement[]>([]);
const [user, setUser] = useState<User | null>(null);
const [error, setError] = useState<string | null>(null);
```

**3. API Client:**
```typescript
class ApiClient {
  async get<T>(endpoint: string): Promise<ApiResponse<T>> {
    const response = await fetch(endpoint);
    return response.json() as Promise<ApiResponse<T>>;
  }
  
  async post<TRequest, TResponse>(
    endpoint: string, 
    data: TRequest
  ): Promise<ApiResponse<TResponse>> {
    // ...
  }
}

// Uso
const movements = await client.get<Movement[]>('/api/movements');
const user = await client.post<CreateUserDTO, User>('/api/users', userData);
```

### 🎓 Utility Types (Generics de TypeScript)

TypeScript incluye generics útiles pre-definidos:

```typescript
// Partial<T> - Todas las propiedades opcionales
type PartialUser = Partial<User>;
// { name?: string; email?: string; age?: number }

// Required<T> - Todas las propiedades requeridas
type RequiredUser = Required<User>;

// Pick<T, K> - Solo algunas propiedades
type UserName = Pick<User, 'name' | 'email'>;
// { name: string; email: string }

// Omit<T, K> - Todo excepto algunas propiedades
type UserWithoutEmail = Omit<User, 'email'>;

// Record<K, V> - Objeto con claves K y valores V
type UserScores = Record<string, number>;
// { [key: string]: number }

// ReturnType<T> - Extrae tipo de retorno de una función
type FetchResult = ReturnType<typeof fetch>;
// Promise<Response>

// Parameters<T> - Extrae tipos de parámetros de una función
type FetchParams = Parameters<typeof fetch>;
// [input: RequestInfo, init?: RequestInit]
```

---

## 5. Interfaces vs Types

### 🟢 Explicación Simple

**Analogía:** Ambos son como "plantillas" para describir la forma de un objeto. Es como decir "un carro tiene 4 ruedas, un motor y puertas". `interface` y `type` dicen qué propiedades debe tener un objeto.

**¿Cuál es la diferencia?**
Ambos hacen casi lo mismo, pero `interface` es para objetos y `type` es más flexible (puede ser uniones, primitivos, etc.).

### 🔵 Explicación Técnica

**Interface:**
- Diseñada para definir **contratos de objetos**
- Soporta **declaration merging** (múltiples declaraciones se fusionan)
- Soporta **extends** para herencia
- Mejor rendimiento de compilación para objetos
- Convención: usar para APIs públicas

**Type:**
- **Type alias** - un nombre para cualquier tipo
- Soporta **union types**, **intersection types**, **mapped types**
- Puede representar primitivos, tuplas, funciones
- NO soporta declaration merging
- Más flexible pero menos extensible

### 📝 Interface en Detalle

```typescript
// Declaración básica
interface User {
  id: string;
  name: string;
  email: string;
}

// Propiedades opcionales y readonly
interface User {
  id: string;              // Requerida
  name: string;            // Requerida
  email?: string;          // Opcional
  readonly createdAt: Date; // No se puede modificar después de crear
}

// Extensión (herencia) - una interfaz extiende otra
interface AdminUser extends User {
  permissions: string[];
  role: 'ADMIN';
}

// Extensión múltiple
interface SuperAdmin extends AdminUser, Auditable {
  superPowers: string[];
}

// 🔵 Declaration Merging - TypeScript fusiona interfaces con el mismo nombre
interface User {
  id: string;
  name: string;
}

interface User {
  age?: number;  // Se AÑADE a la interfaz anterior
}

// User ahora tiene: id, name, age

// Esto es útil para extender tipos de librerías externas:
declare module 'express' {
  interface Request {
    user?: User;  // Añadir propiedad custom a Request de Express
  }
}
```

### 📝 Type en Detalle

```typescript
// Type alias para objeto (similar a interface)
type User = {
  id: string;
  name: string;
  email: string;
};

// Intersection (&) - combina tipos
type AdminUser = User & {
  permissions: string[];
};

// Union Types (|) - uno u otro
type Status = 'active' | 'inactive' | 'pending';
type ID = string | number;
type Result = Success | Error;

// Tipos primitivos y tuplas
type StringOrNumber = string | number;
type Coordinate = [number, number];
type Callback = (data: string) => void;

// Mapped Types
type Readonly<T> = {
  readonly [K in keyof T]: T[K];
};

// Conditional Types
type NonNullable<T> = T extends null | undefined ? never : T;

// Template Literal Types
type EventName = `on${Capitalize<string>}`;
// "onClick", "onHover", "onFocus", etc.
```

### 🎯 Interface vs Type - Comparación Directa

| Característica | Interface | Type |
|---------------|-----------|------|
| Objetos | ✅ | ✅ |
| Union types | ❌ | ✅ `string \| number` |
| Intersection | Extiende: `extends A, B` | ✅ `A & B` |
| Primitivos | ❌ | ✅ `type ID = string` |
| Tuplas | ❌ | ✅ `[string, number]` |
| Funciones | ✅ (verboso) | ✅ (conciso) |
| Declaration merging | ✅ | ❌ |
| Extensión de libs | ✅ (mejor) | ❌ |
| Rendimiento compilación | ✅ (mejor) | Similar |

### 💻 Convención del Proyecto

```typescript
// INTERFACES para:
// - Repositorios (contratos)
interface IMovementRepository {
  findAll(): Promise<Movement[]>;
  create(data: CreateMovementData): Promise<Movement>;
}

// - DTOs de API
interface CreateMovementRequest {
  type: 'INCOME' | 'EXPENSE';
  amount: number;
  concept: string;
}

// - Props de React Components
interface MovementFormProps {
  onSubmit: (data: MovementData) => void;
  initialData?: Movement;
}

// TYPES para:
// - Uniones
type MovementType = 'INCOME' | 'EXPENSE';
type Role = 'ADMIN' | 'USER';

// - IDs y primitivos
type UserId = string;
type Amount = number;

// - Tipos derivados
type MovementWithUser = Movement & { user: User };
type PartialMovement = Partial<Movement>;
```

---

## 6. Async/Await y Promises

### 🟢 Explicación Simple

**Analogía:** Imagina que pides comida en un restaurante. No te quedas parado esperando - te sientas y sigues conversando mientras la cocina prepara tu pedido. Cuando está listo, te avisan. `async/await` es esa forma de "esperar sin bloquear".

**¿Qué es `async/await`?**
Es una forma de escribir código que espera por algo (como datos de una API) sin congelar toda la aplicación.

### 🔵 Explicación Técnica

**Promise:** Un objeto que representa un valor que puede estar disponible ahora, en el futuro, o nunca. Tiene 3 estados:
- **Pending**: En progreso
- **Fulfilled**: Completado con éxito (resuelto)
- **Rejected**: Falló (rechazado)

**async/await:** Syntactic sugar sobre Promises. El compilador transforma `async/await` en código basado en Promises.

**Características:**
- `async` marca una función como asíncrona, siempre retorna Promise
- `await` pausa la ejecución hasta que la Promise se resuelve
- `await` solo puede usarse dentro de funciones `async`
- `try/catch` captura errores de Promises rechazadas

### 📝 Evolución del Código Asíncrono

**Era 1: Callbacks (Node.js antiguo)**
```typescript
// ❌ Callback Hell - Pirámide de la muerte
fetchUser(userId, (error, user) => {
  if (error) return handleError(error);
  fetchMovements(user.id, (error, movements) => {
    if (error) return handleError(error);
    calculateBalance(movements, (error, balance) => {
      if (error) return handleError(error);
      updateUI(balance);
    });
  });
});
```

**Era 2: Promises (ES6)**
```typescript
// Mejor: Cadena de .then(), manejo centralizado de errores
fetchUser(userId)
  .then(user => fetchMovements(user.id))
  .then(movements => calculateBalance(movements))
  .then(balance => updateUI(balance))
  .catch(error => handleError(error))
  .finally(() => hideLoading());
```

**Era 3: Async/Await (ES2017)**
```typescript
// ✅ Código que parece síncrono pero es asíncrono
async function loadDashboard(userId: string): Promise<void> {
  try {
    const user = await fetchUser(userId);
    const movements = await fetchMovements(user.id);
    const balance = await calculateBalance(movements);
    updateUI(balance);
  } catch (error) {
    handleError(error);
  } finally {
    hideLoading();
  }
}
```

### 📝 Patrones Comunes

```typescript
// 1. Ejecución Secuencial
async function sequential() {
  const a = await fetchA();  // Espera...
  const b = await fetchB();  // Luego espera...
  const c = await fetchC();  // Luego espera...
  // Tiempo total: A + B + C
}

// 2. Ejecución Paralela (Promise.all)
async function parallel() {
  const [a, b, c] = await Promise.all([
    fetchA(),
    fetchB(),
    fetchC()
  ]);
  // Tiempo total: max(A, B, C)
}

// 3. Ejecución con Timeout
async function withTimeout<T>(promise: Promise<T>, ms: number): Promise<T> {
  const timeout = new Promise<never>((_, reject) =>
    setTimeout(() => reject(new Error('Timeout')), ms)
  );
  return Promise.race([promise, timeout]);
}

// 4. Retry con Backoff
async function fetchWithRetry<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3
): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await delay(Math.pow(2, i) * 1000); // Exponential backoff
    }
  }
  throw new Error('Unreachable');
}
```

### 💻 Ejemplos del Proyecto

```typescript
// hooks/useMovements.ts
export function useMovements() {
  const [movements, setMovements] = useState<Movement[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchMovements = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await movementsService.getAll();
      setMovements(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido');
    } finally {
      setIsLoading(false);
    }
  };

  // ...
}

// Use Case
export class CreateMovementUseCase {
  async execute(input: CreateMovementRequest): Promise<Result<Movement>> {
    try {
      // Validaciones...
      const movement = await this.repository.create(input);
      return Result.ok(movement);
    } catch (error) {
      return Result.fail('Error al crear movimiento');
    }
  }
}

// API Route
export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'GET') {
    const movements = await movementRepository.findAll();
    return res.status(200).json({ data: movements });
  }
  // ...
}
```

### ⚠️ Errores Comunes

```typescript
// ❌ ERROR: Olvidar await
async function bad() {
  const data = fetchData(); // data es Promise, no el valor!
  console.log(data); // Promise { <pending> }
}

// ❌ ERROR: await en loop (secuencial innecesario)
async function slow(ids: string[]) {
  const results = [];
  for (const id of ids) {
    results.push(await fetch(id)); // Una a la vez 🐢
  }
  return results;
}

// ✅ CORRECTO: Promise.all para paralelizar
async function fast(ids: string[]) {
  return Promise.all(ids.map(id => fetch(id))); // Todas a la vez 🚀
}

// ❌ ERROR: No manejar errores
async function risky() {
  const data = await fetchData(); // Si falla, explota
}

// ✅ CORRECTO: Siempre try/catch
async function safe() {
  try {
    const data = await fetchData();
    return data;
  } catch (error) {
    console.error('Error:', error);
    return null;
  }
}
```

---

## 7. Destructuring

### 🟢 Explicación Simple

**Analogía:** Es como abrir una caja de regalo y sacar las cosas individualmente. En lugar de decir "caja.juguete" y "caja.carta", sacas el juguete y la carta directamente y les pones nombre.

**¿Qué es la sintaxis `{ algo }` en funciones?**
**Destructuring** "desempaca" propiedades de objetos o elementos de arrays directamente en variables individuales.

### 🔵 Explicación Técnica

**Destructuring assignment** es una expresión de JavaScript (ES6) que permite extraer datos de arrays u objetos en variables distintas. TypeScript añade type annotations al proceso.

**Tipos de destructuring:**
- **Object destructuring**: Extrae por nombre de propiedad
- **Array destructuring**: Extrae por posición
- **Nested destructuring**: Extracción anidada
- **Rest pattern**: `...rest` captura el resto

### 📝 Object Destructuring

```typescript
const user = {
  name: 'Juan',
  email: 'juan@example.com',
  age: 25,
  address: {
    city: 'Bogotá',
    country: 'Colombia'
  }
};

// ❌ Sin destructuring - Verboso
const name = user.name;
const email = user.email;
const age = user.age;

// ✅ Con destructuring - Conciso
const { name, email, age } = user;

// Con valores por defecto
const { name, role = 'USER' } = user; // role = 'USER' si no existe

// Con renombre (alias)
const { name: userName, email: userEmail } = user;

// Destructuring anidado
const { address: { city, country } } = user;

// Rest pattern - capturar todo lo demás
const { name, ...rest } = user;
// rest = { email: '...', age: 25, address: {...} }
```

### 📝 Array Destructuring

```typescript
const numbers = [1, 2, 3, 4, 5];

// ❌ Sin destructuring
const first = numbers[0];
const second = numbers[1];

// ✅ Con destructuring
const [first, second] = numbers; // first = 1, second = 2

// Saltar elementos
const [first, , third] = numbers; // first = 1, third = 3

// Rest pattern
const [first, second, ...rest] = numbers;
// first = 1, second = 2, rest = [3, 4, 5]

// Swap sin variable temporal
let a = 1, b = 2;
[a, b] = [b, a]; // a = 2, b = 1

// 🔵 React useState retorna un array - por eso usamos destructuring
const [count, setCount] = useState(0);
const [user, setUser] = useState<User | null>(null);
```

### 📝 Destructuring en Parámetros de Función

```typescript
// ❌ Sin destructuring
function greet(user: User): string {
  return `Hola ${user.name}, tu email es ${user.email}`;
}

// ✅ Con destructuring - Más claro qué propiedades usa
function greet({ name, email }: User): string {
  return `Hola ${name}, tu email es ${email}`;
}

// Con valores por defecto en parámetros
function createUser({ 
  name, 
  email, 
  role = 'USER' 
}: CreateUserParams): User {
  return { name, email, role };
}

// React: Destructuring de props
function UserCard({ user, onDelete, isAdmin = false }: UserCardProps) {
  return (
    <div>
      <h1>{user.name}</h1>
      {isAdmin && <button onClick={onDelete}>Delete</button>}
    </div>
  );
}
```

### 💻 Ejemplos del Proyecto

```typescript
// hooks/useMovements.ts - Destructuring de respuesta de API
const { data, error, isLoading } = await movementsService.getAll();

// components - Destructuring de props
function MovementRow({ movement, onEdit, onDelete }: MovementRowProps) {
  const { type, amount, concept, date } = movement;
  // ...
}

// API Response destructuring
const { movements, pagination } = response;

// Context destructuring
const { user, isAuthenticated, logout } = useAuth();
```

---

## 8. Optional Chaining (?.)

### 🟢 Explicación Simple

**Analogía:** Es como preguntar con cuidado. En lugar de decir "dame el teléfono de Juan" (que explota si Juan no existe), dices "¿Juan existe? Si sí, ¿tiene teléfono? Si sí, dámelo".

**¿Qué significa `?.`?**
Accede a propiedades de objetos de forma **segura**. Si algo en el camino es `null` o `undefined`, retorna `undefined` en lugar de lanzar error.

### 🔵 Explicación Técnica

**Optional chaining (`?.`)** es un operador de ES2020 que permite leer propiedades anidadas sin validar explícitamente cada nivel. El operador **short-circuits** (cortocircuita): si encuentra `null` o `undefined`, para inmediatamente y retorna `undefined`.

**Variantes:**
- `obj?.prop` - Acceso a propiedad
- `obj?.[expr]` - Acceso con expresión
- `func?.()` - Llamada a función opcional
- `arr?.[index]` - Acceso a índice de array

### 📝 Ejemplos Detallados

```typescript
const user: User | null = getUser();

// ❌ Sin optional chaining - Puede explotar
const city = user.address.city; 
// TypeError: Cannot read property 'address' of null

// ❌ Validación manual - Verboso
const city = user && user.address && user.address.city;

// ✅ Con optional chaining - Limpio y seguro
const city = user?.address?.city; // undefined si cualquier parte es null/undefined

// Acceso con expresión dinámica
const prop = 'email';
const value = user?.[prop]; // user?.['email']

// Llamada a función opcional
const result = user?.getFullName?.(); // undefined si user o getFullName no existen

// Con arrays
const firstMovement = movements?.[0];
const lastMovement = movements?.[movements.length - 1];
```

### 📝 Combinación con Nullish Coalescing

```typescript
// Obtener valor o usar default
const city = user?.address?.city ?? 'Ciudad desconocida';
const email = user?.email ?? 'sin-email@example.com';
const role = user?.role ?? 'USER';

// En el proyecto
const balance = movements?.reduce((sum, m) => sum + m.amount, 0) ?? 0;
```

### 💻 Ejemplos del Proyecto

```typescript
// Acceso seguro a sesión
const userName = session?.user?.name ?? 'Usuario';
const userRole = session?.user?.role ?? 'USER';

// Acceso seguro a respuestas de API
const movements = response?.data?.movements ?? [];
const totalPages = response?.pagination?.totalPages ?? 1;

// Acceso seguro a elementos del DOM
const inputValue = document.getElementById('search')?.value;
```

---

## 9. Nullish Coalescing (??)

### 🟢 Explicación Simple

**Analogía:** Es como decir "usa esto, pero si no existe, usa esto otro". La diferencia con `||` es que `??` solo considera "no existe" a `null` y `undefined`, no a `0`, `''`, o `false`.

**¿Qué significa `??`?**
Retorna el lado derecho **solo si** el lado izquierdo es `null` o `undefined`. Es más preciso que `||`.

### 🔵 Explicación Técnica

**Nullish coalescing (`??`)** es un operador de ES2020 que retorna el operando derecho cuando el izquierdo es **nullish** (`null` o `undefined`). A diferencia de `||` (OR lógico), `??` no considera valores **falsy** como `0`, `''`, `false`, `NaN`.

**Falsy values:** `false`, `0`, `-0`, `0n`, `''`, `null`, `undefined`, `NaN`
**Nullish values:** Solo `null` y `undefined`

### 📝 Diferencia con || (OR)

```typescript
// 🔴 Problema con || - Trata todos los falsy igual
const port = config.port || 3000;
// Si config.port = 0, usa 3000 (¡incorrecto!)
// Si config.port = null, usa 3000 (correcto)

const name = user.name || 'Anónimo';
// Si user.name = '', usa 'Anónimo' (¿querías esto?)
// Si user.name = null, usa 'Anónimo' (correcto)

const enabled = settings.enabled || true;
// Si settings.enabled = false, usa true (¡incorrecto!)

// ✅ Solución con ?? - Solo null/undefined
const port = config.port ?? 3000;
// Si config.port = 0, usa 0 ✅
// Si config.port = null, usa 3000 ✅

const name = user.name ?? 'Anónimo';
// Si user.name = '', usa '' ✅
// Si user.name = null, usa 'Anónimo' ✅

const enabled = settings.enabled ?? true;
// Si settings.enabled = false, usa false ✅
// Si settings.enabled = undefined, usa true ✅
```

### 📝 Tabla de Comparación

| Valor | `value \|\| 'default'` | `value ?? 'default'` |
|-------|------------------------|----------------------|
| `null` | `'default'` | `'default'` |
| `undefined` | `'default'` | `'default'` |
| `0` | `'default'` 🔴 | `0` ✅ |
| `''` | `'default'` 🔴 | `''` ✅ |
| `false` | `'default'` 🔴 | `false` ✅ |
| `NaN` | `'default'` | `NaN` |
| `'hola'` | `'hola'` | `'hola'` |
| `123` | `123` | `123` |

### 💻 Ejemplos del Proyecto

```typescript
// Paginación con defaults seguros
const page = filters.page ?? 1;      // 0 es válido
const limit = filters.limit ?? 10;   // 0 significaría "sin límite"

// Configuración
const timeout = config.timeout ?? 5000;
const retries = config.retries ?? 3;

// Valores de formulario
const amount = parseFloat(input) ?? 0;

// Estados de React
const count = savedCount ?? 0;  // 0 es un valor válido
const name = savedName ?? '';    // '' es un valor válido
```

### ⚠️ Combinación con Optional Chaining

```typescript
// Patrón común: ?. para acceso seguro, ?? para fallback
const userName = user?.profile?.name ?? 'Usuario Anónimo';
const theme = settings?.appearance?.theme ?? 'light';
const locale = user?.preferences?.language ?? 'es';

// En el proyecto
const balance = account?.balance ?? 0;
const movements = user?.movements ?? [];
```

---

## 10. Export Default vs Named Exports

### 🟢 Explicación Simple

**Analogía:** Imagina un restaurante. "Export default" es el plato del día - solo hay uno y es el principal. "Named exports" son el menú completo - varios platos que eliges por nombre.

**¿Por qué a veces `export default` y a veces `export`?**
- `export default`: Exporta UNA cosa principal del archivo
- `export`: Exporta múltiples cosas con nombre específico

### 🔵 Explicación Técnica

**Default Export (ES6 Modules):**
- Cada módulo puede tener **máximo un** default export
- Se importa **sin llaves**
- Se puede importar con **cualquier nombre**
- Convención: archivos que exportan una sola cosa principal

**Named Exports:**
- Un módulo puede tener **ilimitados** named exports
- Se importan **con llaves**
- Se importan con el **nombre exacto** (o usando `as` para alias)
- Convención: archivos de utilidades, constantes, tipos

### 📝 Default Export en Detalle

```typescript
// Archivo: Button.tsx
function Button(props: ButtonProps) { ... }
export default Button;

// Alternativa: declaración y export juntos
export default function Button(props: ButtonProps) { ... }

// Importar: sin llaves, cualquier nombre
import Button from './Button';
import MiBoton from './Button';    // ✅ Funciona
import LoQueSea from './Button';   // ✅ Funciona (mala práctica)
```

### 📝 Named Exports en Detalle

```typescript
// Archivo: utils.ts
export function formatDate(date: Date): string { ... }
export function formatMoney(amount: number): string { ... }
export const MAX_AMOUNT = 999999999.99;
export type Money = number;
export interface Config { ... }

// Importar: con llaves, nombre exacto
import { formatDate, formatMoney, MAX_AMOUNT } from './utils';

// Con alias
import { formatDate as fd, formatMoney as fm } from './utils';

// Importar todo
import * as utils from './utils';
utils.formatDate(new Date());
utils.formatMoney(1000);
```

### 📝 Combinando Default y Named

```typescript
// Archivo: React.ts (ejemplo conceptual)
export default function React() { ... }  // Default
export function useState() { ... }        // Named
export function useEffect() { ... }       // Named
export type FC = ...                      // Named

// Importar
import React, { useState, useEffect, FC } from 'react';
//     ^default  ^------named------^
```

### 💻 Convenciones del Proyecto

| Tipo de Archivo | Export | Razonamiento |
|-----------------|--------|--------------|
| Componentes React | `export default` | Next.js lo requiere para páginas |
| Páginas Next.js | `export default` | Requerido por Next.js |
| API Routes | `export default` | Requerido por Next.js |
| Hooks | `export function` (named) | Múltiples hooks posibles |
| Services | `export const` (named) | Singleton pattern |
| Utilities | `export function` (named) | Múltiples funciones |
| Types/Interfaces | `export interface` (named) | Múltiples tipos |
| Entidades (Domain) | `export class` (named) | Claridad de importación |
| Value Objects | `export class` (named) | Claridad de importación |

### 💻 Ejemplos del Proyecto

```typescript
// ✅ Página Next.js - REQUIERE default export
// pages/movements.tsx
export default function MovementsPage() {
  return <div>...</div>;
}

// ✅ API Route - REQUIERE default export
// pages/api/movements/index.ts
export default async function handler(req, res) {
  // ...
}

// ✅ Componente - default export (convención)
// components/ui/Button.tsx
export default function Button({ children, onClick }: ButtonProps) {
  return <button onClick={onClick}>{children}</button>;
}

// ✅ Hook - named export (múltiples pueden coexistir)
// hooks/useAuth.ts
export function useAuth() {
  // ...
}

// ✅ Service - named export
// lib/client/services/movements.service.ts
export const movementsService = new MovementsService();

// ✅ Entidad de dominio - named export
// lib/server/domain/entities/Movement.ts
export class Movement {
  // ...
}

// ✅ Value Object - named export
// lib/server/domain/value-objects/Money.ts
export class Money {
  // ...
}
```

---

## 11. Clases en TypeScript

### 🟢 Explicación Simple

**Analogía:** Una clase es como un plano de una casa. El plano describe cómo será la casa (cuartos, puertas, ventanas), pero no es la casa en sí. Cuando construyes la casa siguiendo el plano, eso es una **instancia**.

**¿Qué es una clase?**
Una plantilla para crear objetos con propiedades y métodos predefinidos.

### 🔵 Explicación Técnica

Las **clases** en TypeScript extienden la sintaxis de ES6 con:
- **Type annotations** para propiedades y métodos
- **Modificadores de acceso** (`public`, `private`, `protected`)
- **Modificador `readonly`** para propiedades inmutables
- **Abstract classes** para herencia
- **Property shorthand** en constructores

### 📝 Anatomía de una Clase

```typescript
class User {
  // Propiedades (campos)
  private readonly id: string;
  public name: string;
  protected email: string;
  
  // Propiedad con valor por defecto
  public role: string = 'USER';
  
  // Constructor
  constructor(id: string, name: string, email: string) {
    this.id = id;
    this.name = name;
    this.email = email;
  }
  
  // Método de instancia
  public greet(): string {
    return `Hola, soy ${this.name}`;
  }
  
  // Getter
  get displayName(): string {
    return `${this.name} (${this.role})`;
  }
  
  // Setter
  set displayName(value: string) {
    this.name = value.split(' ')[0];
  }
  
  // Método estático (no necesita instancia)
  static createAnonymous(): User {
    return new User('anon', 'Anónimo', 'anon@example.com');
  }
}

// Uso
const user = new User('1', 'Juan', 'juan@example.com');
user.greet();  // "Hola, soy Juan"
user.displayName;  // "Juan (USER)"

const anon = User.createAnonymous();  // Método estático
```

### 📝 Constructor Shorthand

```typescript
// ❌ Forma larga
class User {
  private readonly id: string;
  public name: string;
  
  constructor(id: string, name: string) {
    this.id = id;
    this.name = name;
  }
}

// ✅ Shorthand - TypeScript crea propiedades automáticamente
class User {
  constructor(
    private readonly id: string,
    public name: string
  ) {}
  // No necesitas asignar this.id = id
}
```

### 💻 Ejemplos del Proyecto

```typescript
// lib/server/domain/entities/Movement.ts
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
    this._type = MovementTypeVO.fromString(typeValue);
    this._amount = Money.create(amountValue);
    this._concept = Concept.create(conceptValue);
  }

  // Factory method
  static create(props: CreateMovementProps): Movement {
    return new Movement(/* ... */);
  }

  // Getters para encapsulamiento
  get amount(): number {
    return this._amount.amount;
  }

  set amount(value: number) {
    this._amount = Money.create(value);
  }
}

// lib/server/domain/value-objects/Money.ts
export class Money {
  private constructor(private readonly _amount: number) {}

  static create(amount: number): Money {
    if (amount < 0) throw new Error('Amount must be positive');
    if (amount > 999999999.99) throw new Error('Amount too large');
    return new Money(amount);
  }

  get amount(): number {
    return this._amount;
  }
}
```

---

## 12. Modificadores de Acceso

### 🟢 Explicación Simple

**Analogía:** Es como los niveles de acceso en un edificio. `public` es como el lobby - todos pueden entrar. `private` es como tu oficina personal - solo tú. `protected` es como el piso de tu departamento - tú y tu familia (subclases).

### 🔵 Explicación Técnica

| Modificador | Clase | Subclase | Exterior |
|-------------|-------|----------|----------|
| `public` | ✅ | ✅ | ✅ |
| `protected` | ✅ | ✅ | ❌ |
| `private` | ✅ | ❌ | ❌ |

### 📝 Ejemplos

```typescript
class BankAccount {
  public accountNumber: string;    // Accesible desde cualquier lugar
  protected balance: number;       // Accesible solo en esta clase y subclases
  private pin: string;             // Solo accesible en esta clase

  constructor(accountNumber: string, initialBalance: number, pin: string) {
    this.accountNumber = accountNumber;
    this.balance = initialBalance;
    this.pin = pin;
  }

  public getBalance(): number {
    return this.balance;
  }

  private validatePin(inputPin: string): boolean {
    return this.pin === inputPin;
  }
}

class SavingsAccount extends BankAccount {
  public addInterest(): void {
    this.balance *= 1.05;  // ✅ protected es accesible
    // this.pin;           // ❌ Error: private no es accesible
  }
}

const account = new BankAccount('123', 1000, '1234');
account.accountNumber;  // ✅ public
account.getBalance();   // ✅ public method
// account.balance;     // ❌ Error: protected
// account.pin;         // ❌ Error: private
```

---

## 13. readonly y const

### 🟢 Explicación Simple

- `const`: La variable no puede reasignarse, pero su contenido puede mutar
- `readonly`: La propiedad de un objeto no puede modificarse después de crearse

### 📝 Diferencias

```typescript
// const - la REFERENCIA no cambia
const user = { name: 'Juan' };
user.name = 'Pedro';  // ✅ Funciona (mutación)
// user = { name: 'Ana' };  // ❌ Error (reasignación)

// readonly - la PROPIEDAD no cambia
class User {
  readonly id: string;
  
  constructor(id: string) {
    this.id = id;  // ✅ Asignación en constructor
  }
  
  changeId() {
    // this.id = 'new';  // ❌ Error
  }
}

// Readonly<T> utility type
const config: Readonly<{ apiUrl: string; timeout: number }> = {
  apiUrl: 'http://api.example.com',
  timeout: 5000
};
// config.timeout = 3000;  // ❌ Error
```

---

## 14. Union Types y Literal Types

### 🟢 Explicación Simple

**Union Type (`|`):** Una variable puede ser de múltiples tipos.
**Literal Type:** El tipo es un valor específico, no solo un tipo general.

### 📝 Ejemplos

```typescript
// Union Type
type ID = string | number;
let userId: ID = '123';  // ✅
userId = 123;            // ✅
// userId = true;        // ❌ Error

// Literal Type
type Status = 'active' | 'inactive' | 'pending';
let state: Status = 'active';    // ✅
// state = 'unknown';            // ❌ Error

// Combinación (Discriminated Union) - muy usado
type Result = 
  | { success: true; data: User }
  | { success: false; error: string };

function handleResult(result: Result) {
  if (result.success) {
    console.log(result.data);   // TypeScript sabe que data existe
  } else {
    console.log(result.error);  // TypeScript sabe que error existe
  }
}
```

### 💻 En el Proyecto

```typescript
// lib/server/domain/value-objects/MovementType.ts
type MovementType = 'INCOME' | 'EXPENSE';

// lib/server/domain/value-objects/Role.ts
type Role = 'ADMIN' | 'USER';

// Result pattern (discriminated union)
type Result<T> = 
  | { isSuccess: true; value: T }
  | { isSuccess: false; error: string };
```

---

## 15. Type Guards

### 🟢 Explicación Simple

**Type Guard:** Una forma de decirle a TypeScript "en este punto del código, sé que el tipo es X".

### 📝 Ejemplos

```typescript
// typeof guard
function process(value: string | number) {
  if (typeof value === 'string') {
    return value.toUpperCase();  // TypeScript sabe que es string
  }
  return value.toFixed(2);       // TypeScript sabe que es number
}

// instanceof guard
function handleError(error: Error | string) {
  if (error instanceof Error) {
    return error.message;
  }
  return error;
}

// in guard
interface Dog { bark(): void }
interface Cat { meow(): void }

function speak(animal: Dog | Cat) {
  if ('bark' in animal) {
    animal.bark();  // TypeScript sabe que es Dog
  } else {
    animal.meow();  // TypeScript sabe que es Cat
  }
}

// Custom type guard
function isUser(obj: unknown): obj is User {
  return obj !== null 
    && typeof obj === 'object' 
    && 'email' in obj;
}

function process(data: unknown) {
  if (isUser(data)) {
    console.log(data.email);  // TypeScript sabe que es User
  }
}
```

---

## 🎓 Resumen Rápido

| Concepto | Qué Hace | Ejemplo |
|----------|----------|---------|
| `index.ts` | Barrel export - simplifica imports | `import { A, B } from '@/lib'` |
| `@/` | Path alias - evita `../../../` | `import { X } from '@/hooks'` |
| `: Type` | Type annotation - tipado | `const x: string = 'hi'` |
| `<T>` | Generics - tipos reutilizables | `Result<Movement>` |
| `interface` | Define forma de objeto | `interface User { }` |
| `type` | Define tipos (más flexible) | `type ID = string \| number` |
| `async/await` | Código asíncrono legible | `const x = await fetch()` |
| `{ a, b }` | Destructuring | `const { name } = user` |
| `?.` | Optional chaining | `user?.address?.city` |
| `??` | Nullish coalescing | `value ?? 'default'` |
| `export default` | Export único por archivo | Componentes, páginas |
| `export` | Named exports múltiples | Hooks, utils, services |
| `class` | Plantilla para objetos | Entidades, Value Objects |
| `private/protected` | Modificadores de acceso | Encapsulamiento |
| `readonly` | Propiedad inmutable | IDs, timestamps |
| `string \| number` | Union type | Variables múltiples tipos |
| `'a' \| 'b'` | Literal type | Valores restringidos |

---

## 📚 Continúa Leyendo

➡️ **Siguiente documento**: [07 - Next.js Explicado](./07-NEXTJS-EXPLICADO.md)

---

**Última actualización:** Febrero 2026
