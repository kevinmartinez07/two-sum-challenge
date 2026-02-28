# 📖 Glosario Técnico Completo

## 🎯 Propósito

Este glosario define **todos los términos técnicos** usados en el proyecto. Cada concepto tiene:
- 🟢 **Definición simple** - Una oración fácil de entender
- 🔵 **Definición técnica** - La explicación formal correcta
- 💻 **Ejemplo del proyecto** - Dónde se usa en este código

---

## 📋 Índice Alfabético

[A](#a) | [B](#b) | [C](#c) | [D](#d) | [E](#e) | [F](#f) | [G](#g) | [H](#h) | [I](#i) | [J](#j) | [K](#k) | [L](#l) | [M](#m) | [N](#n) | [O](#o) | [P](#p) | [Q](#q) | [R](#r) | [S](#s) | [T](#t) | [U](#u) | [V](#v) | [W](#w) | [X](#x) | [Y](#y) | [Z](#z)

---

## A

### Abstracción
- 🟢 Ocultar los detalles complicados y mostrar solo lo necesario
- 🔵 Principio de diseño que separa la interfaz (qué hace) de la implementación (cómo lo hace)
- 💻 `IMovementRepository` es una abstracción de la persistencia de datos

### API (Application Programming Interface)
- 🟢 Un contrato que define cómo dos programas se comunican
- 🔵 Conjunto de protocolos y herramientas que permiten la comunicación entre componentes de software
- 💻 `/api/movements` es una API REST que expone operaciones CRUD

### API Route
- 🟢 Un archivo en Next.js que actúa como endpoint de backend
- 🔵 Función serverless en Next.js ubicada en `pages/api/` que maneja requests HTTP
- 💻 `pages/api/movements/index.ts` maneja GET/POST de movimientos

### Async/Await
- 🟢 Forma de escribir código que espera por algo sin congelar la aplicación
- 🔵 Sintaxis de ES2017 que simplifica el manejo de Promises usando `async` functions y `await` expressions
- 💻 `const movements = await repository.findAll();`

### Agregado (Aggregate)
- 🟢 Un grupo de objetos que se tratan como una unidad
- 🔵 En DDD, cluster de entidades y value objects con una raíz que garantiza consistencia
- 💻 `Movement` es un agregado con `Money`, `Concept` como value objects internos

---

## B

### Barrel Export
- 🟢 Un archivo `index.ts` que re-exporta otros archivos para simplificar imports
- 🔵 Patrón de organización de módulos donde un archivo central exporta la API pública del módulo
- 💻 `components/ui/index.ts` exporta Button, Card, Modal, etc.

### Better Auth
- 🟢 Librería de autenticación que usamos para login
- 🔵 Framework de autenticación para Next.js que soporta múltiples proveedores (OAuth, credentials)
- 💻 Configurado en `lib/auth/` para login con GitHub y email/password

---

## C

### Capa (Layer)
- 🟢 Un nivel de organización del código con una responsabilidad específica
- 🔵 División lógica del sistema donde cada nivel tiene una función definida y reglas de comunicación
- 💻 Domain, Application, Infrastructure, Presentation son las 4 capas

### Clean Architecture
- 🟢 Una forma de organizar el código donde lo importante (negocio) no depende de lo técnico (BD, framework)
- 🔵 Arquitectura de software de Robert C. Martin donde las dependencias apuntan hacia el dominio central
- 💻 `lib/server/domain/` no importa nada de `lib/server/infrastructure/`

### CLI (Command Line Interface)
- 🟢 Programa que se usa escribiendo comandos en la terminal
- 🔵 Interfaz de usuario basada en texto para interactuar con software
- 💻 `npm run dev`, `npx prisma migrate dev`

### Command (CQRS)
- 🟢 Una operación que modifica datos (crear, actualizar, eliminar)
- 🔵 En CQRS, operación de escritura que cambia el estado del sistema
- 💻 `CreateMovementUseCase`, `DeleteMovementUseCase`

### Componente (React)
- 🟢 Un pedazo reutilizable de interfaz de usuario
- 🔵 Función o clase en React que retorna JSX y encapsula UI + lógica
- 💻 `Button`, `Card`, `MovementForm`, `UserTable`

### Constructor
- 🟢 Función especial que se ejecuta al crear un objeto
- 🔵 Método especial de una clase invocado con `new` para inicializar instancias
- 💻 `new Movement(id, type, amount, ...)` llama al constructor de Movement

### Context (React)
- 🟢 Una forma de compartir datos entre componentes sin pasarlos uno por uno
- 🔵 API de React para pasar datos a través del árbol de componentes sin prop drilling
- 💻 `AuthContext` comparte el estado de autenticación globalmente

### CQRS (Command Query Responsibility Segregation)
- 🟢 Separar las operaciones de lectura de las de escritura
- 🔵 Patrón arquitectónico que separa modelos de lectura (Query) y escritura (Command)
- 💻 `GetMovementsUseCase` (Query) vs `CreateMovementUseCase` (Command)

### CRUD
- 🟢 Las 4 operaciones básicas: Crear, Leer, Actualizar, Eliminar
- 🔵 Acrónimo de Create, Read, Update, Delete - operaciones fundamentales de datos
- 💻 API de movimientos tiene POST (Create), GET (Read), PUT (Update), DELETE (Delete)

---

## D

### DDD (Domain-Driven Design)
- 🟢 Diseñar el software basándose en cómo funciona el negocio
- 🔵 Enfoque de desarrollo que centra el diseño en el dominio del negocio y su lógica
- 💻 Entidades, Value Objects, Domain Events implementan DDD

### Decorator Pattern
- 🟢 Añadir funcionalidad a algo sin modificar su código original
- 🔵 Patrón estructural que envuelve objetos para añadir comportamiento dinámicamente
- 💻 `withAuth(withRole(handler))` - cada función añade funcionalidad

### Dependency Injection (DI)
- 🟢 Pasar las dependencias desde afuera en lugar de crearlas adentro
- 🔵 Técnica donde las dependencias de un componente se proveen externamente
- 💻 `new CreateMovementUseCase(repository)` - el repositorio se inyecta

### Destructuring
- 🟢 Extraer partes de un objeto/array en variables separadas
- 🔵 Sintaxis de ES6 para extraer propiedades de objetos o elementos de arrays
- 💻 `const { name, email } = user;`

### DIP (Dependency Inversion Principle)
- 🟢 Depender de abstracciones, no de implementaciones concretas
- 🔵 Principio SOLID: módulos de alto nivel no deben depender de módulos de bajo nivel
- 💻 Use Cases dependen de `IMovementRepository`, no de `PrismaMovementRepository`

### Domain Event
- 🟢 Un registro de "algo pasó" en el sistema
- 🔵 Objeto que representa un hecho ocurrido en el dominio, usado para comunicación entre agregados
- 💻 `MovementCreatedEvent`, `UserUpdatedEvent`

### Domain Layer
- 🟢 La capa que contiene las reglas del negocio
- 🔵 Capa central en Clean Architecture que contiene entidades, value objects y lógica de negocio
- 💻 `lib/server/domain/entities/`, `lib/server/domain/value-objects/`

### DTO (Data Transfer Object)
- 🟢 Objeto simple para mover datos entre capas
- 🔵 Objeto que transporta datos entre procesos, sin lógica de negocio
- 💻 `CreateMovementRequest`, `CreateMovementResponse`

---

## E

### Encapsulamiento
- 🟢 Ocultar los detalles internos de un objeto
- 🔵 Principio OOP de ocultar estado interno y exponer solo interfaz pública
- 💻 `private _amount` con getter `get amount()` en la clase Money

### Endpoint
- 🟢 Una URL específica de una API
- 🔵 URI que acepta requests HTTP y retorna respuestas
- 💻 `POST /api/movements` es un endpoint para crear movimientos

### Entity (Entidad)
- 🟢 Un objeto con identidad única que persiste en el tiempo
- 🔵 En DDD, objeto definido por su identidad continua, no por sus atributos
- 💻 `Movement` y `User` son entidades (tienen `id` único)

### Environment Variables
- 🟢 Configuraciones guardadas fuera del código
- 🔵 Variables del sistema operativo usadas para configuración de aplicaciones
- 💻 `DATABASE_URL`, `BETTER_AUTH_SECRET` en `.env`

### ESLint
- 🟢 Herramienta que detecta errores y malas prácticas en tu código
- 🔵 Linter de JavaScript/TypeScript que analiza código estáticamente
- 💻 Configurado para detectar errores de estilo y mejores prácticas

---

## F

### Factory Method
- 🟢 Un método especial que crea objetos (en lugar de usar `new`)
- 🔵 Patrón de creación que encapsula la lógica de instanciación de objetos
- 💻 `Money.create(100)` en lugar de `new Money(100)`

### Facade Pattern
- 🟢 Una interfaz simple que esconde complejidad detrás
- 🔵 Patrón estructural que proporciona interfaz unificada a un conjunto de interfaces
- 💻 `ApplicationService` es el facade que unifica todos los use cases

### Falsy/Truthy
- 🟢 Valores que se evalúan como false o true en condiciones
- 🔵 En JavaScript, valores que coercionan a false (`0`, `''`, `null`, `undefined`, `false`) o true (resto)
- 💻 `if (user)` evalúa falsy si user es null/undefined

### Fetch API
- 🟢 Forma moderna de hacer requests HTTP en JavaScript
- 🔵 API nativa del navegador para realizar requests HTTP basados en Promises
- 💻 `const response = await fetch('/api/movements');`

---

## G

### Generic (Genérico)
- 🟢 Un tipo que funciona con cualquier otro tipo
- 🔵 En TypeScript, parámetros de tipo que permiten crear componentes reutilizables
- 💻 `Result<T>`, `Promise<Movement[]>`, `useState<User>`

### Getter
- 🟢 Un método que devuelve el valor de una propiedad
- 🔵 Accessor que permite acceso controlado a propiedades de una clase
- 💻 `get amount(): number { return this._amount.amount; }`

---

## H

### HOC (Higher-Order Component)
- 🟢 Una función que toma un componente y retorna un componente mejorado
- 🔵 Patrón en React para reutilizar lógica de componentes
- 💻 No usado directamente, preferimos hooks

### HOF (Higher-Order Function)
- 🟢 Una función que recibe o retorna otras funciones
- 🔵 Función de primera clase que opera sobre funciones
- 💻 `withAuth(handler)` es un HOF que retorna una función

### Hook (React)
- 🟢 Funciones especiales de React que añaden capacidades a componentes
- 🔵 API de React (16.8+) que permite usar estado y otras características sin clases
- 💻 `useAuth()`, `useMovements()`, `useState()`, `useEffect()`

### HTTP Methods
- 🟢 Tipos de acciones que puedes hacer con una URL (GET, POST, PUT, DELETE)
- 🔵 Verbos del protocolo HTTP que indican la acción deseada
- 💻 GET = leer, POST = crear, PUT = actualizar, DELETE = eliminar

---

## I

### Inmutabilidad
- 🟢 Algo que NO puede cambiar después de crearse
- 🔵 Principio donde los objetos no modifican su estado interno después de la construcción
- 💻 Value Objects son inmutables: `Money.create()` retorna nueva instancia

### Interface (Interfaz)
- 🟢 Un contrato que dice qué métodos debe tener una clase
- 🔵 En TypeScript, declaración de estructura que otros tipos deben implementar
- 💻 `interface IMovementRepository { findAll(): Promise<Movement[]>; }`

### ISR (Incremental Static Regeneration)
- 🟢 Regenerar páginas estáticas sin rebuild completo
- 🔵 Característica de Next.js que permite actualizar páginas estáticas incrementalmente
- 💻 No usado actualmente en el proyecto

---

## J

### Jest
- 🟢 Herramienta para escribir y ejecutar tests
- 🔵 Framework de testing de JavaScript mantenido por Meta
- 💻 198 tests escritos con Jest en `__tests__/`

### JSX
- 🟢 HTML dentro de JavaScript
- 🔵 Extensión de sintaxis de JavaScript que permite escribir markup similar a HTML
- 💻 `return <Button onClick={handleClick}>Click</Button>;`

### JSON (JavaScript Object Notation)
- 🟢 Formato de texto para intercambiar datos
- 🔵 Formato ligero de intercambio de datos basado en objetos JavaScript
- 💻 API responses: `{ "data": [...], "success": true }`

---

## K

### Key (React)
- 🟢 Identificador único para elementos en listas
- 🔵 Prop especial que ayuda a React a identificar elementos que cambiaron
- 💻 `movements.map(m => <MovementRow key={m.id} ... />)`

---

## L

### Layer (Capa)
- Ver [Capa](#capa-layer)

### Lazy Loading
- 🟢 Cargar algo solo cuando se necesita
- 🔵 Técnica de optimización que difiere la carga de recursos hasta que son necesarios
- 💻 Next.js hace lazy loading de páginas automáticamente

### Literal Type
- 🟢 Un tipo que solo acepta un valor específico
- 🔵 En TypeScript, tipo que representa un valor exacto, no solo una categoría
- 💻 `type MovementType = 'INCOME' | 'EXPENSE';`

---

## M

### Middleware
- 🟢 Código que se ejecuta antes/después de una operación
- 🔵 Función que intercepta el flujo de request/response para procesar datos
- 💻 `withAuth`, `withRole`, `withErrorHandling`

### Migration (Prisma)
- 🟢 Cambio en la estructura de la base de datos
- 🔵 Archivo que describe cambios en el schema de la BD, versionado
- 💻 `npx prisma migrate dev` crea y aplica migraciones

### Module
- 🟢 Un archivo de código reutilizable
- 🔵 En ES6, archivo con su propio scope que puede exportar/importar código
- 💻 Cada archivo `.ts`/`.tsx` es un módulo

---

## N

### Next.js
- 🟢 Framework de React para crear aplicaciones web completas
- 🔵 Framework React que añade SSR, routing, API routes, y optimizaciones
- 💻 Versión 15.1.3 usada en el proyecto

### Nullish
- 🟢 Solo `null` y `undefined` (no incluye `0`, `''`, `false`)
- 🔵 En JavaScript/TypeScript, valores nullish son estrictamente `null` o `undefined`
- 💻 `value ?? 'default'` usa default solo si value es nullish

---

## O

### ORM (Object-Relational Mapping)
- 🟢 Herramienta que traduce entre objetos de código y tablas de BD
- 🔵 Técnica que convierte datos entre sistemas de tipos incompatibles (OOP ↔ SQL)
- 💻 Prisma es el ORM que usamos

### Optional Chaining
- 🟢 Acceder a propiedades de forma segura (retorna undefined si no existe)
- 🔵 Operador `?.` de ES2020 que cortocircuita si encuentra null/undefined
- 💻 `user?.address?.city` retorna undefined si user o address no existen

---

## P

### Pages Router
- 🟢 Sistema de routing de Next.js basado en la carpeta `pages/`
- 🔵 Arquitectura de Next.js donde archivos en `pages/` definen rutas automáticamente
- 💻 `pages/movements.tsx` → `/movements`

### Path Alias
- 🟢 Atajo para imports (ej: `@/` en lugar de `../../../`)
- 🔵 Configuración de TypeScript que mapea rutas virtuales a reales
- 💻 `import { Button } from '@/components/ui';`

### Pattern
- 🟢 Una solución reutilizable a un problema común
- 🔵 Descripción de una solución general a un problema recurrente en diseño de software
- 💻 Repository Pattern, Factory Pattern, CQRS Pattern

### Prisma
- 🟢 Herramienta para trabajar con bases de datos fácilmente
- 🔵 ORM de siguiente generación para Node.js y TypeScript con type-safety
- 💻 Versión 6.15.0, schema en `prisma/schema.prisma`

### Promise
- 🟢 Un objeto que representa algo que terminará en el futuro
- 🔵 Objeto que representa la eventual completitud (o falla) de una operación asíncrona
- 💻 `repository.findAll()` retorna `Promise<Movement[]>`

### Props
- 🟢 Datos que pasas a un componente de React
- 🔵 Propiedades de solo lectura pasadas de componentes padres a hijos
- 💻 `<Button onClick={handleClick} variant="primary">Text</Button>`

---

## Q

### Query (CQRS)
- 🟢 Una operación que solo lee datos (no los modifica)
- 🔵 En CQRS, operación de lectura que no cambia el estado del sistema
- 💻 `GetMovementsUseCase`, `GetBalanceUseCase`

---

## R

### React
- 🟢 Librería para construir interfaces de usuario
- 🔵 Biblioteca de JavaScript para construir UIs basadas en componentes
- 💻 Versión 18.3.1 usada en el proyecto

### Readonly
- 🟢 Algo que solo se puede leer, no modificar
- 🔵 Modificador de TypeScript que impide reasignación después de inicialización
- 💻 `readonly id: string` - el id no puede cambiar

### Repository Pattern
- 🟢 Un intermediario entre el dominio y la fuente de datos
- 🔵 Patrón que abstrae la capa de persistencia, proporcionando interfaz tipo colección
- 💻 `IMovementRepository` (interfaz) implementada por `PrismaMovementRepository`

### REST (Representational State Transfer)
- 🟢 Estilo de diseño de APIs basado en recursos y verbos HTTP
- 🔵 Estilo arquitectónico que define restricciones para crear servicios web escalables
- 💻 API usa REST: `GET /api/movements`, `POST /api/movements`

### Result Pattern
- 🟢 Retornar éxito o error explícitamente en lugar de lanzar excepciones
- 🔵 Patrón donde las funciones retornan un objeto que encapsula éxito/fallo
- 💻 `Result.ok(value)` o `Result.fail("error")`

---

## S

### Schema (Prisma)
- 🟢 La definición de las tablas de la base de datos
- 🔵 Archivo que define modelos de datos, relaciones y configuración de Prisma
- 💻 `prisma/schema.prisma`

### Setter
- 🟢 Un método para cambiar el valor de una propiedad de forma controlada
- 🔵 Accessor que permite modificación controlada de propiedades
- 💻 `set amount(value) { this._amount = Money.create(value); }`

### SRP (Single Responsibility Principle)
- 🟢 Cada clase/función debe hacer solo una cosa
- 🔵 Principio SOLID: una clase debe tener una única razón para cambiar
- 💻 `CreateMovementUseCase` solo crea movimientos, nada más

### SSG (Static Site Generation)
- 🟢 Generar HTML en tiempo de build (no en cada visita)
- 🔵 Técnica de pre-renderizado donde el HTML se genera en build time
- 💻 No usado actualmente (usamos CSR para páginas dinámicas)

### SSR (Server-Side Rendering)
- 🟢 Generar HTML en el servidor en cada request
- 🔵 Técnica de renderizado donde el servidor genera HTML para cada request
- 💻 No usado actualmente (usamos CSR)

### State
- 🟢 Datos que pueden cambiar y afectan la UI
- 🔵 En React, datos internos del componente que cuando cambian, causa re-render
- 💻 `const [movements, setMovements] = useState([]);`

---

## T

### Tailwind CSS
- 🟢 Framework de CSS con clases utilitarias
- 🔵 Framework de CSS utility-first para diseño rápido
- 💻 Versión 3.4.17, clases como `bg-blue-500 px-4 py-2`

### Transaction
- 🟢 Grupo de operaciones que deben completarse todas o ninguna
- 🔵 Secuencia de operaciones tratadas como unidad atómica (ACID)
- 💻 `prisma.$transaction()` para operaciones atómicas

### Type Annotation
- 🟢 Indicar qué tipo de dato espera una variable
- 🔵 Sintaxis de TypeScript para especificar tipos estáticamente
- 💻 `const name: string = "Juan";`

### Type Guard
- 🟢 Verificación que le dice a TypeScript qué tipo es algo
- 🔵 Expresión que realiza runtime check para refinar tipos
- 💻 `if (typeof value === 'string')` o `if (error instanceof Error)`

### TypeScript
- 🟢 JavaScript con tipos
- 🔵 Superset de JavaScript que añade tipado estático opcional
- 💻 Versión 5.7.2 con strict mode habilitado

---

## U

### Union Type
- 🟢 Un tipo que puede ser de varios tipos
- 🔵 En TypeScript, tipo que representa uno de varios tipos posibles
- 💻 `type ID = string | number;`

### Use Case
- 🟢 Una acción específica que el usuario puede realizar
- 🔵 En Clean Architecture, componente que orquesta la lógica para un caso de uso específico
- 💻 `CreateMovementUseCase`, `GetUsersUseCase`

### UUID
- 🟢 Identificador único universal
- 🔵 Estándar de identificadores de 128 bits, único globalmente
- 💻 Prisma genera UUIDs con `@default(uuid())`

---

## V

### Validación
- 🟢 Verificar que los datos sean correctos
- 🔵 Proceso de verificar que datos cumplan reglas de negocio/formato
- 💻 Value Objects validan en creación: `Money.create()` rechaza negativos

### Value Object
- 🟢 Objeto definido por su valor, no por una identidad
- 🔵 En DDD, objeto inmutable sin identidad, comparado por sus atributos
- 💻 `Money`, `Email`, `Phone`, `Concept`, `Role`

### Vercel
- 🟢 Plataforma donde está desplegado el proyecto
- 🔵 Plataforma de deployment para frontend y serverless functions
- 💻 Deployment automático desde GitHub

### void
- 🟢 Indica que una función no retorna nada
- 🔵 Tipo de TypeScript que representa ausencia de valor de retorno
- 💻 `function logMessage(msg: string): void { console.log(msg); }`

---

## W

### Wrapper
- 🟢 Un componente que envuelve a otros
- 🔵 Componente o función que encapsula otro para añadir contexto/funcionalidad
- 💻 `_app.tsx` es el wrapper global de todas las páginas

---

## X

### XSS (Cross-Site Scripting)
- 🟢 Ataque donde alguien inyecta código malicioso en tu página
- 🔵 Vulnerabilidad de seguridad que permite inyección de scripts en aplicaciones web
- 💻 React previene XSS escapando contenido automáticamente

---

## Y

### Yarn/npm/pnpm
- 🟢 Herramientas para instalar paquetes de JavaScript
- 🔵 Gestores de paquetes para el ecosistema Node.js
- 💻 Usamos npm (`npm install`, `npm run dev`)

---

## Z

### Zod
- 🟢 Librería para validar datos en TypeScript
- 🔵 Librería de declaración y validación de schemas con inferencia de tipos
- 💻 No usado actualmente, pero podría añadirse para validación de DTOs

---

## 📝 Acrónimos Frecuentes

| Acrónimo | Significado | Traducción |
|----------|-------------|------------|
| API | Application Programming Interface | Interfaz de Programación de Aplicaciones |
| CQRS | Command Query Responsibility Segregation | Segregación de Responsabilidad de Comando y Consulta |
| CRUD | Create, Read, Update, Delete | Crear, Leer, Actualizar, Eliminar |
| DDD | Domain-Driven Design | Diseño Dirigido por el Dominio |
| DI | Dependency Injection | Inyección de Dependencias |
| DIP | Dependency Inversion Principle | Principio de Inversión de Dependencias |
| DTO | Data Transfer Object | Objeto de Transferencia de Datos |
| HOC | Higher-Order Component | Componente de Orden Superior |
| HOF | Higher-Order Function | Función de Orden Superior |
| OCP | Open/Closed Principle | Principio Abierto/Cerrado |
| ORM | Object-Relational Mapping | Mapeo Objeto-Relacional |
| REST | Representational State Transfer | Transferencia de Estado Representacional |
| SOLID | SRP, OCP, LSP, ISP, DIP | Los 5 principios de diseño OOP |
| SRP | Single Responsibility Principle | Principio de Responsabilidad Única |
| SSG | Static Site Generation | Generación de Sitio Estático |
| SSR | Server-Side Rendering | Renderizado del Lado del Servidor |
| UUID | Universally Unique Identifier | Identificador Único Universal |

---

## 📚 Recursos Adicionales

- **Clean Architecture**: "Clean Architecture" de Robert C. Martin
- **DDD**: "Domain-Driven Design" de Eric Evans
- **TypeScript**: [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/)
- **Next.js**: [Next.js Documentation](https://nextjs.org/docs)
- **React**: [React Documentation](https://react.dev)
- **Prisma**: [Prisma Documentation](https://www.prisma.io/docs)

---

**Última actualización:** Febrero 2026
