# 1️⃣2️⃣ Guía de Desarrollo

## 🎯 Para Desarrolladores Nuevos en el Proyecto

Esta guía te ayudará a empezar a trabajar en el proyecto rápidamente.

---

## 🚀 Configuración del Entorno

### Requisitos Previos

```bash
Node.js: >= 18.0.0
npm: >= 9.0.0
PostgreSQL: >= 14.0
Git: >= 2.30
```

### Paso 1: Clonar el Repositorio

```bash
git clone <repo-url>
cd sistema-gestion-ingresos
```

### Paso 2: Instalar Dependencias

```bash
npm install
```

### Paso 3: Configurar Variables de Entorno

```bash
cp .env.example .env
```

Edita `.env` con tus valores:

```env
# Database
DATABASE_URL="postgresql://user:password@localhost:5432/dbname"

# Auth
BETTER_AUTH_SECRET="tu-secret-aqui"
BETTER_AUTH_URL="http://localhost:3000"

# GitHub OAuth (opcional para desarrollo)
GITHUB_CLIENT_ID="tu-client-id"
GITHUB_CLIENT_SECRET="tu-client-secret"

# Email (opcional)
MAILTRAP_TOKEN="tu-token"
```

### Paso 4: Configurar Base de Datos

```bash
# Crear base de datos y ejecutar migraciones
npx prisma migrate dev

# Generar cliente de Prisma
npx prisma generate

# Seed (opcional, para datos de prueba)
npx prisma db seed
```

### Paso 5: Ejecutar en Desarrollo

```bash
npm run dev
```

Abre http://localhost:3000

---

## 🛠️ Comandos Útiles

### Desarrollo

```bash
# Iniciar servidor de desarrollo
npm run dev

# Type checking (sin compilar)
npm run typecheck

# Linting
npm run lint

# Formatear código
npm run format
```

### Testing

```bash
# Ejecutar todos los tests
npm test

# Tests en modo watch
npm run test:watch

# Tests con cobertura
npm run test:coverage
```

### Base de Datos

```bash
# Ver datos en GUI
npx prisma studio

# Crear nueva migración
npx prisma migrate dev --name nombre_migracion

# Aplicar migraciones en producción
npx prisma migrate deploy

# Reset de base de datos (⚠️ DESTRUCTIVO)
npx prisma migrate reset
```

### Build y Producción

```bash
# Build para producción
npm run build

# Iniciar en producción
npm start
```

---

## 📁 Estructura del Código

### Backend (lib/server/)

```
lib/server/
├── domain/              # ← Empezar aquí para entender el negocio
│   ├── entities/
│   ├── value-objects/
│   └── events/
│
├── application/         # ← Casos de uso
│   ├── use-cases/
│   ├── repositories/
│   └── shared/
│
├── infrastructure/      # ← Implementaciones técnicas
│   └── repositories/
│
└── presentation/        # ← API HTTP
    └── middlewares/
```

### Frontend

```
├── pages/              # ← Rutas de Next.js
├── components/         # ← Componentes por feature
├── hooks/              # ← Lógica reutilizable
├── contexts/           # ← Estado global
└── lib/client/         # ← Services y API client
```

---

## 🎓 Flujo de Trabajo Recomendado

### Para Agregar una Nueva Feature

#### Ejemplo: Agregar "Categorías"

**1. Domain Layer** (si aplica)
```typescript
// lib/server/domain/entities/Category.ts
export class Category {
  constructor(
    public readonly id: string,
    public name: string,
    public color: string,
    public readonly createdAt: Date
  ) {}
  
  static create(props: CategoryProps): Category {
    // Validaciones y lógica de negocio
    return new Category(props.id, props.name, props.color, new Date());
  }
}
```

**2. Application Layer** (repositorio y use cases)
```typescript
// lib/server/application/repositories/ICategoryRepository.ts
export interface ICategoryRepository {
  create(data: CreateCategoryData): Promise<Category>;
  findAll(): Promise<Category[]>;
  delete(id: string): Promise<void>;
}

// lib/server/application/use-cases/categories/commands/CreateCategoryUseCase.ts
export class CreateCategoryUseCase {
  constructor(private repository: ICategoryRepository) {}
  
  async execute(input: CreateCategoryRequest): Promise<Result<CategoryResponse>> {
    try {
      const category = await this.repository.create(input);
      return Result.ok(this.toResponse(category));
    } catch (error) {
      return Result.fail((error as Error).message);
    }
  }
}
```

**3. Infrastructure Layer** (repositorio concreto)
```typescript
// lib/server/infrastructure/repositories/PrismaCategoryRepository.ts
export class PrismaCategoryRepository implements ICategoryRepository {
  async create(data: CreateCategoryData): Promise<Category> {
    const prismaCategory = await prisma.category.create({ data });
    return this.toDomain(prismaCategory);
  }
  
  private toDomain(prisma: PrismaCategory): Category {
    return Category.create({
      id: prisma.id,
      name: prisma.name,
      color: prisma.color,
      createdAt: prisma.createdAt,
    });
  }
}
```

**4. Presentation Layer** (API route)
```typescript
// pages/api/categories/index.ts
import { appService } from '@/lib/server/application/ApplicationService';

const handler = async (req: NextApiRequest, res: NextApiResponse) => {
  if (req.method === 'POST') {
    const result = await appService.createCategory.execute(req.body);
    
    if (result.isFailure) {
      return res.status(400).json({ error: result.error });
    }
    
    return res.status(201).json({ success: true, data: result.value });
  }
};

export default withAuth(withErrorHandling(handler));
```

**5. Frontend** (service, hook, componente)
```typescript
// lib/client/services/categories.service.ts
class CategoriesService {
  async createCategory(data: CreateCategoryDTO): Promise<CategoryDTO> {
    const response = await apiClient.post<CategoryDTO>('/categories', data);
    return response.data!;
  }
}

// hooks/useCategories.ts
export function useCategories() {
  const [categories, setCategories] = useState<CategoryDTO[]>([]);
  
  const createCategory = async (data: CreateCategoryDTO) => {
    const created = await categoriesService.createCategory(data);
    setCategories(prev => [...prev, created]);
  };
  
  return { categories, createCategory };
}

// components/categories/CategoryForm.tsx
export function CategoryForm() {
  const { createCategory } = useCategories();
  
  const handleSubmit = async (data: CreateCategoryDTO) => {
    await createCategory(data);
  };
  
  return <form onSubmit={handleSubmit}>...</form>;
}
```

**6. Tests**
```typescript
// __tests__/domain/entities/Category.test.ts
describe('Category', () => {
  it('should create category', () => {
    const category = Category.create({
      id: '1',
      name: 'Test',
      color: '#FF0000',
      createdAt: new Date(),
    });
    expect(category.name).toBe('Test');
  });
});

// __tests__/application/use-cases/CreateCategoryUseCase.test.ts
describe('CreateCategoryUseCase', () => {
  it('should create category successfully', async () => {
    const mockRepo = { create: jest.fn().mockResolvedValue(mockCategory) };
    const useCase = new CreateCategoryUseCase(mockRepo as any);
    
    const result = await useCase.execute(input);
    
    expect(result.isSuccess).toBe(true);
  });
});
```

---

## 🧪 Testing

### Ejecutar Tests Específicos

```bash
# Tests de un archivo específico
npm test -- Movement.test.ts

# Tests con patrón
npm test -- --testPathPattern=domain

# Tests con watch mode
npm test -- --watch
```

### Escribir Tests

#### Tests Unitarios (Domain)
```typescript
// No necesitas mocks
describe('Money', () => {
  it('should validate amount', () => {
    expect(() => Money.create(-10)).toThrow();
    expect(() => Money.create(100)).not.toThrow();
  });
});
```

#### Tests con Mocks (Application)
```typescript
describe('CreateMovementUseCase', () => {
  it('should create movement', async () => {
    const mockRepo: IMovementRepository = {
      create: jest.fn().mockResolvedValue(mockMovement),
      // ... otros métodos
    };
    
    const useCase = new CreateMovementUseCase(mockRepo);
    const result = await useCase.execute(input);
    
    expect(result.isSuccess).toBe(true);
    expect(mockRepo.create).toHaveBeenCalledWith(input);
  });
});
```

---

## 🔧 Debugging

### VS Code Launch Config

Crea `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Next.js: debug server-side",
      "type": "node",
      "request": "launch",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "port": 9229,
      "console": "integratedTerminal"
    },
    {
      "name": "Jest: debug current file",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/node_modules/.bin/jest",
      "args": ["${file}", "--runInBand"],
      "console": "integratedTerminal"
    }
  ]
}
```

### Logs

```typescript
// En desarrollo
console.log('Debug:', someVariable);

// En producción (mejor usar logger estructurado)
logger.info('User created', {
  userId: user.id,
  email: user.email,
  timestamp: new Date(),
});
```

---

## 🎯 Convenciones de Código

### Nombres

```typescript
// Clases: PascalCase
class CreateMovementUseCase { }
class PrismaMovementRepository { }

// Interfaces: I + PascalCase
interface IMovementRepository { }

// Funciones: camelCase
function createMovement() { }

// Constantes: UPPER_SNAKE_CASE
const MAX_AMOUNT = 999999999.99;

// Archivos: kebab-case o PascalCase según tipo
Movement.ts          // Entidad
movement.types.ts    // Tipos
CreateMovementUseCase.ts  // Use case
```

### Imports

```typescript
// 1. Librerías externas
import { NextApiRequest, NextApiResponse } from 'next';
import { PrismaClient } from '@prisma/client';

// 2. Alias internos
import { Movement } from '@/lib/server/domain/entities/Movement';
import { IMovementRepository } from '@/lib/server/application/repositories/IMovementRepository';

// 3. Relativos (solo si muy cercanos)
import { Money } from './Money';
```

### Comentarios

```typescript
/**
 * Crea un nuevo movimiento validando todas las reglas de negocio
 * @param data - Datos del movimiento a crear
 * @returns Result con el movimiento creado o error
 */
async execute(data: CreateMovementRequest): Promise<Result<MovementResponse>> {
  // Validación de permisos
  if (!this.canCreate(data.userId)) {
    return Result.fail('No autorizado');
  }
  
  // Crear movimiento
  const movement = await this.repository.create(data);
  return Result.ok(movement);
}
```

---

## 🐛 Problemas Comunes

### Error: "Prisma Client not generated"

**Solución:**
```bash
npx prisma generate
```

### Error: "Database connection failed"

**Solución:**
1. Verifica que PostgreSQL esté corriendo
2. Verifica DATABASE_URL en .env
3. Prueba conexión con:
```bash
npx prisma db pull
```

### Error: "Module not found"

**Solución:**
```bash
# Limpiar node_modules y reinstalar
rm -rf node_modules
npm install

# Limpiar cache de Next.js
rm -rf .next
npm run dev
```

### Tests fallan por timeout

**Solución:**
```typescript
// Aumentar timeout en test específico
it('should create movement', async () => {
  // ...
}, 10000); // 10 segundos
```

---

## 📚 Recursos Útiles

### Documentación del Proyecto
- [00-INDICE.md](./00-INDICE.md) - Navegación completa
- [02-ARQUITECTURA.md](./02-ARQUITECTURA.md) - Entender la arquitectura
- [13-FAQ-REVISION-TECNICA.md](./13-FAQ-REVISION-TECNICA.md) - Preguntas frecuentes

### Documentación Externa
- [Next.js Docs](https://nextjs.org/docs)
- [Prisma Docs](https://www.prisma.io/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [Jest Docs](https://jestjs.io/docs/getting-started)

---

## 🤝 Contribución

### Flujo de Git

```bash
# 1. Crear rama desde main
git checkout main
git pull origin main
git checkout -b feature/nombre-feature

# 2. Hacer cambios y commits
git add .
git commit -m "feat: add category feature"

# 3. Push
git push origin feature/nombre-feature

# 4. Crear Pull Request en GitHub
```

### Commits Convencionales

```bash
feat: nueva funcionalidad
fix: corrección de bug
docs: cambios en documentación
style: formateo, punto y coma, etc.
refactor: refactorización de código
test: agregar o modificar tests
chore: tareas de mantenimiento
```

---

## 📞 Ayuda

Si tienes problemas:

1. ✅ Lee la documentación relevante en `docs/`
2. ✅ Busca en issues de GitHub
3. ✅ Revisa los tests para ver ejemplos de uso
4. ✅ Pregunta al equipo

---

**Última actualización:** Febrero 2026
