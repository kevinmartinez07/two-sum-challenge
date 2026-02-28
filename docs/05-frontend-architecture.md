# Frontend Architecture - Arquitectura del Cliente

## 📍 Ubicación
- `pages/` - Páginas y rutas (Next.js Pages Router)
- `components/` - Componentes React reutilizables
- `hooks/` - Custom hooks
- `lib/client/` - Lógica del cliente (API, servicios, tipos)
- `contexts/` - React Context para estado global
- `styles/` - Estilos globales

## 🎯 Propósito
**Interfaz de usuario** que consume la API backend sin conocer la implementación interna del servidor.

---

## 🧱 Estructura

```
Frontend (Nunca importa de lib/server/)
├── pages/                    ← Rutas y páginas
│   ├── index.tsx            ← Dashboard (/)
│   ├── login.tsx            ← Login (/login)
│   ├── movements.tsx        ← Gestión de movimientos
│   ├── reports.tsx          ← Reportes y gráficos
│   └── users.tsx            ← Administración de usuarios
├── components/              ← UI components
│   ├── Layout.tsx
│   ├── movements/
│   │   ├── MovementForm.tsx
│   │   ├── MovementTable.tsx
│   │   └── MovementStats.tsx
│   ├── reports/
│   │   ├── MonthlyChart.tsx
│   │   └── DistributionChart.tsx
│   └── ui/                  ← Componentes base (shadcn/ui)
│       ├── Button.tsx
│       ├── Card.tsx
│       └── Modal.tsx
├── hooks/                   ← Custom hooks
│   ├── useAuth.ts
│   ├── useMovements.ts
│   ├── useUsers.ts
│   └── useReports.ts
├── lib/client/              ← Lógica del cliente
│   ├── api/
│   │   └── client.ts       ← HTTP client (fetch wrapper)
│   ├── services/           ← Servicios por dominio
│   │   ├── movements.service.ts
│   │   ├── users.service.ts
│   │   └── reports.service.ts
│   ├── types/              ← Tipos del frontend
│   │   ├── movement.types.ts
│   │   ├── user.types.ts
│   │   └── report.types.ts
│   └── utils/
│       └── errors.ts       ← Manejo de errores
├── contexts/
│   └── AuthContext.tsx     ← Estado global de autenticación
└── styles/
    └── globals.css
```

---

## 1. API Client (HTTP Wrapper)

### lib/client/api/client.ts

```typescript
export interface ApiResponseFormat<T> {
  success: boolean;
  data?: T;
  error?: string;
  errors?: string[];
}

export class ApiError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public response?: unknown
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

class ApiClient {
  private baseUrl: string = '/api';

  private async request<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<ApiResponseFormat<T>> {
    const url = `${this.baseUrl}${endpoint}`;

    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new ApiError(
          data.error || 'An error occurred',
          response.status,
          data
        );
      }

      return data;
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }
      throw new ApiError(
        error instanceof Error ? error.message : 'Network error',
        0
      );
    }
  }

  async get<T>(endpoint: string): Promise<ApiResponseFormat<T>> {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  async post<T>(
    endpoint: string,
    body?: unknown
  ): Promise<ApiResponseFormat<T>> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(body),
    });
  }

  async put<T>(
    endpoint: string,
    body?: unknown
  ): Promise<ApiResponseFormat<T>> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(body),
    });
  }

  async delete<T>(endpoint: string): Promise<ApiResponseFormat<T>> {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }
}

export const apiClient = new ApiClient();
```

**Características:**
1. ✅ Centraliza configuración (base URL, headers)
2. ✅ Maneja errores HTTP consistentemente
3. ✅ Lanza `ApiError` con status code
4. ✅ Tipado genérico con TypeScript

---

## 2. Services (Capa de Servicios)

### lib/client/services/movements.service.ts

```typescript
import { apiClient } from '../api/client';
import { MovementResponseDTO } from '../types/movement.types';

export interface CreateMovementDTO {
  type: 'INCOME' | 'EXPENSE';
  amount: number;
  concept: string;
  date: Date;
}

export interface MovementFilters {
  type?: 'INCOME' | 'EXPENSE';
  startDate?: Date;
  endDate?: Date;
}

class MovementsService {
  /**
   * GET /api/movements
   */
  async getMovements(
    filters?: MovementFilters
  ): Promise<MovementResponseDTO[]> {
    const params = new URLSearchParams();
    
    if (filters?.type) params.append('type', filters.type);
    if (filters?.startDate) 
      params.append('startDate', filters.startDate.toISOString());
    if (filters?.endDate) 
      params.append('endDate', filters.endDate.toISOString());

    const query = params.toString() ? `?${params.toString()}` : '';
    const response = await apiClient.get<{ movements: MovementResponseDTO[] }>(
      `/movements${query}`
    );

    return response.data?.movements || [];
  }

  /**
   * POST /api/movements
   */
  async createMovement(data: CreateMovementDTO): Promise<MovementResponseDTO> {
    const response = await apiClient.post<MovementResponseDTO>('/movements', {
      ...data,
      date: data.date.toISOString(),
    });

    if (!response.data) {
      throw new Error('No data returned from server');
    }

    return response.data;
  }

  /**
   * DELETE /api/movements/:id
   */
  async deleteMovement(id: string): Promise<void> {
    await apiClient.delete(`/movements/${id}`);
  }
}

export const movementsService = new MovementsService();
```

**Patrón Service Layer:**
- Encapsula las llamadas HTTP
- Transforma datos (Date → ISO string)
- Maneja query params
- Retorna tipos específicos
- Oculta detalles de la API al resto del frontend

---

## 3. Custom Hooks (Estado y Lógica)

### hooks/useMovements.ts

```typescript
import { movementsService, CreateMovementDTO, MovementFilters } from '@/lib/client/services/movements.service';
import { MovementResponseDTO } from '@/lib/client/types/movement.types';
import { useCallback, useEffect, useState } from 'react';

interface UseMovementsOptions {
  autoFetch?: boolean;
  filters?: MovementFilters;
}

export function useMovements(options: UseMovementsOptions = {}) {
  const { autoFetch = true, filters } = options;

  const [movements, setMovements] = useState<MovementResponseDTO[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Fetch movements from server
   */
  const fetchMovements = useCallback(
    async (customFilters?: MovementFilters) => {
      setLoading(true);
      setError(null);

      try {
        const data = await movementsService.getMovements(
          customFilters || filters
        );
        setMovements(data);
      } catch (err) {
        const message =
          err instanceof Error ? err.message : 'Error al cargar movimientos';
        setError(message);
      } finally {
        setLoading(false);
      }
    },
    [filters]
  );

  /**
   * Create new movement
   */
  const createMovement = useCallback(async (data: CreateMovementDTO) => {
    setLoading(true);
    setError(null);

    try {
      const newMovement = await movementsService.createMovement(data);
      
      // Optimistic update: agregar al estado local
      setMovements((prev) => [newMovement, ...prev]);
      
      return { success: true, data: newMovement };
    } catch (err) {
      const message =
        err instanceof Error ? err.message : 'Error al crear movimiento';
      setError(message);
      return { success: false, error: message };
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Delete movement
   */
  const deleteMovement = useCallback(async (id: string) => {
    setLoading(true);
    setError(null);

    try {
      await movementsService.deleteMovement(id);
      
      // Optimistic update: remover del estado local
      setMovements((prev) => prev.filter((m) => m.id !== id));
      
      return { success: true };
    } catch (err) {
      const message =
        err instanceof Error ? err.message : 'Error al eliminar movimiento';
      setError(message);
      return { success: false, error: message };
    } finally {
      setLoading(false);
    }
  }, []);

  // Auto-fetch on mount
  useEffect(() => {
    if (autoFetch) {
      fetchMovements();
    }
  }, [autoFetch, fetchMovements]);

  return {
    movements,
    loading,
    error,
    fetchMovements,
    createMovement,
    deleteMovement,
  };
}
```

**Hook Pattern Ventajas:**
1. ✅ Encapsula estado y lógica
2. ✅ Reutilizable en múltiples componentes
3. ✅ Manejo de loading/error consistente
4. ✅ Optimistic updates (UI actualiza antes de confirmar servidor)
5. ✅ Auto-fetch opcional

**Uso en componente:**
```typescript
function MovementsPage() {
  const { movements, loading, createMovement, deleteMovement } = useMovements();

  const handleCreate = async (data) => {
    const result = await createMovement(data);
    if (result.success) {
      toast.success('Movimiento creado');
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div>
      <MovementForm onSubmit={handleCreate} />
      <MovementTable data={movements} onDelete={deleteMovement} />
    </div>
  );
}
```

---

## 4. Components (UI)

### Jerarquía de Componentes

```
components/
├── ui/                      ← Componentes base (shadcn/ui)
│   ├── Button.tsx          ← <Button variant="primary" />
│   ├── Card.tsx            ← <Card><CardHeader /><CardContent /></Card>
│   ├── Modal.tsx           ← <Modal open={true} onClose={...} />
│   └── Table.tsx           ← Tabla genérica
├── movements/              ← Dominio: Movimientos
│   ├── MovementForm.tsx   ← Formulario crear/editar
│   ├── MovementTable.tsx  ← Tabla de movimientos
│   ├── MovementRow.tsx    ← Fila individual
│   └── MovementStats.tsx  ← Estadísticas resumidas
├── users/
│   ├── UserTable.tsx
│   └── UserEditForm.tsx
└── Layout.tsx              ← Layout general con nav
```

### Ejemplo: MovementForm.tsx

```typescript
interface MovementFormProps {
  onSubmit: (data: CreateMovementDTO) => Promise<void>;
  onCancel?: () => void;
}

export function MovementForm({ onSubmit, onCancel }: MovementFormProps) {
  const [formData, setFormData] = useState<CreateMovementDTO>({
    type: 'INCOME',
    amount: 0,
    concept: '',
    date: new Date(),
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await onSubmit(formData);
      // Reset form
      setFormData({ type: 'INCOME', amount: 0, concept: '', date: new Date() });
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <select
        value={formData.type}
        onChange={(e) => setFormData({ ...formData, type: e.target.value })}
      >
        <option value="INCOME">Ingreso</option>
        <option value="EXPENSE">Egreso</option>
      </select>

      <input
        type="number"
        step="0.01"
        min="0.01"
        value={formData.amount}
        onChange={(e) =>
          setFormData({ ...formData, amount: Number(e.target.value) })
        }
      />

      <input
        type="text"
        value={formData.concept}
        onChange={(e) => setFormData({ ...formData, concept: e.target.value })}
        minLength={3}
        maxLength={200}
      />

      <input
        type="date"
        value={formData.date.toISOString().split('T')[0]}
        onChange={(e) =>
          setFormData({ ...formData, date: new Date(e.target.value) })
        }
      />

      <Button type="submit" disabled={loading}>
        {loading ? 'Creando...' : 'Crear Movimiento'}
      </Button>
      {onCancel && (
        <Button type="button" variant="secondary" onClick={onCancel}>
          Cancelar
        </Button>
      )}
    </form>
  );
}
```

---

## 5. Pages (Rutas)

### pages/movements.tsx

```typescript
import { Layout } from '@/components/Layout';
import { MovementForm } from '@/components/movements/MovementForm';
import { MovementTable } from '@/components/movements/MovementTable';
import { MovementStats } from '@/components/movements/MovementStats';
import { useMovements } from '@/hooks/useMovements';
import { useAuth } from '@/hooks/useAuth';
import { useState } from 'react';

export default function MovementsPage() {
  const { user } = useAuth();
  const [filters, setFilters] = useState<MovementFilters>({});
  
  const {
    movements,
    loading,
    error,
    createMovement,
    deleteMovement,
    fetchMovements,
  } = useMovements({ filters });

  if (!user) {
    return <div>Cargando...</div>;
  }

  return (
    <Layout>
      <div className="container mx-auto p-4">
        <h1 className="text-3xl font-bold mb-6">Movimientos</h1>

        {/* Estadísticas */}
        <MovementStats movements={movements} />

        {/* Formulario */}
        <MovementForm
          onSubmit={async (data) => {
            const result = await createMovement(data);
            if (result.success) {
              toast.success('Movimiento creado exitosamente');
            } else {
              toast.error(result.error);
            }
          }}
        />

        {/* Filtros */}
        <MovementFilters
          filters={filters}
          onFiltersChange={(newFilters) => {
            setFilters(newFilters);
            fetchMovements(newFilters);
          }}
        />

        {/* Tabla */}
        {error && <div className="text-red-500">{error}</div>}
        {loading ? (
          <LoadingSpinner />
        ) : (
          <MovementTable
            movements={movements}
            onDelete={async (id) => {
              if (confirm('¿Eliminar movimiento?')) {
                const result = await deleteMovement(id);
                if (result.success) {
                  toast.success('Movimiento eliminado');
                }
              }
            }}
          />
        )}
      </div>
    </Layout>
  );
}
```

---

## 6. Error Handling

### lib/utils/errors.ts

```typescript
import { ApiError } from '../client/api/client';

export function parseHttpError(error: unknown): string {
  if (error instanceof ApiError) {
    // Errores de la API
    return error.message;
  }

  if (error instanceof Error) {
    // Errores JavaScript genéricos
    return error.message;
  }

  // Fallback
  return 'Ha ocurrido un error inesperado';
}
```

**Uso:**
```typescript
try {
  await movementsService.createMovement(data);
} catch (error) {
  const message = parseHttpError(error);
  toast.error(message);
}
```

---

## 7. Context API (Estado Global)

### contexts/AuthContext.tsx

```typescript
import { createContext, useContext, useEffect, useState } from 'react';
import { useSession } from '@/lib/auth/client';

interface User {
  id: string;
  email: string;
  name: string;
  role: 'ADMIN' | 'USER';
}

interface AuthContextValue {
  user: User | null;
  loading: boolean;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const { data: session, isPending } = useSession();
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    if (session?.user) {
      setUser({
        id: session.user.id,
        email: session.user.email,
        name: session.user.name,
        role: session.user.role || 'USER',
      });
    } else {
      setUser(null);
    }
  }, [session]);

  const signOut = async () => {
    await authClient.signOut({ fetchOptions: { onSuccess: () => setUser(null) } });
  };

  return (
    <AuthContext.Provider value={{ user, loading: isPending, signOut }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
```

**Uso:**
```typescript
function Header() {
  const { user, signOut } = useAuth();

  return (
    <header>
      <span>Bienvenido, {user?.name}</span>
      <button onClick={signOut}>Cerrar sesión</button>
    </header>
  );
}
```

---

## 8. Separación Frontend/Backend

### ❌ NUNCA hacer esto

```typescript
// ❌ Importar desde lib/server en el frontend
import { CreateMovementUseCase } from '@/lib/server/application/use-cases';
import { prisma } from '@/lib/server/infrastructure/prisma/client';
```

**Problema**: El frontend no debe conocer la implementación del servidor.

### ✅ Siempre hacer esto

```typescript
// ✅ Usar servicios que llaman a la API
import { movementsService } from '@/lib/client/services/movements.service';

const movements = await movementsService.getMovements();
```

**Contrato**: HTTP/JSON solamente.

---

## 9. Data Flow (Flujo de Datos)

```
Component (UI)
    ↓
Custom Hook (useMovements)
    ↓
Service (movementsService)
    ↓
API Client (apiClient.post)
    ↓
HTTP Request → /api/movements
    ↓
Backend (pages/api/movements/index.ts)
    ↓
Use Case → Repository → Prisma
    ↓
HTTP Response ← { success: true, data: {...} }
    ↓
Service ← Recibe data
    ↓
Hook ← Actualiza estado
    ↓
Component ← Re-renderiza
```

---

## 10. Performance Optimizations

### Memoization

```typescript
const expensiveCalculation = useMemo(() => {
  return movements.reduce((sum, m) => sum + m.amount, 0);
}, [movements]);
```

### Callback Memoization

```typescript
const handleDelete = useCallback(
  (id: string) => {
    deleteMovement(id);
  },
  [deleteMovement]
);
```

### Lazy Loading

```typescript
import dynamic from 'next/dynamic';

const Chart = dynamic(() => import('@/components/reports/MonthlyChart'), {
  loading: () => <LoadingSpinner />,
  ssr: false, // Solo cliente
});
```

---

## ✅ Best Practices

1. **Separación de responsabilidades**:
   - Componentes: Solo UI
   - Hooks: Estado y lógica
   - Services: Llamadas HTTP
   - Types: Tipado TypeScript

2. **Error handling consistente**:
   - Try/catch en hooks
   - `parseHttpError()` para mensajes
   - Toast notifications para feedback

3. **Loading states**:
   - Siempre mostrar spinners
   - Deshabilitar botones durante requests

4. **Optimistic updates**:
   - Actualizar UI antes de confirmar servidor
   - Rollback si falla

5. **TypeScript en todo**:
   - DTOs tipados
   - Interfaces para props
   - Genéricos en servicios

---

## 🔗 Comunicación Frontend ↔ Backend

```
Frontend                    Backend
--------                    -------
Component
   ↓
Hook (useMovements)
   ↓
Service (movementsService)
   ↓
API Client
   ↓
fetch('/api/movements')   → API Route (pages/api/movements)
                            ↓
                          Use Case
                            ↓
                          Repository
                            ↓
                          Prisma → PostgreSQL
                            ↓
                          Result<Movement>
                            ↓
{ success, data } ←        ApiResponse.success()
   ↑
Service recibe
   ↑
Hook actualiza estado
   ↑
Component re-renderiza
```

**Contrato**: Solo JSON sobre HTTP. Sin compartir código TypeScript.

**Fin de la documentación arquitectónica. Ahora tienes una visión completa del sistema.**
