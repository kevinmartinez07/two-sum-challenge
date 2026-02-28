# 5️⃣ Arquitectura del Frontend

## 🎯 Introducción

El frontend está construido con **Next.js 15**, **React 18** y **TypeScript**, siguiendo principios de separación de responsabilidades y componentes reutilizables.

---

## 📁 Estructura de Carpetas

```
├── pages/                 # 🟦 Rutas y páginas de Next.js
│   ├── _app.tsx          # Layout global, providers
│   ├── _document.tsx     # HTML base
│   ├── index.tsx         # Dashboard principal
│   ├── login.tsx         # Página de login
│   ├── register.tsx      # Página de registro
│   ├── movements.tsx     # Gestión de movimientos
│   ├── users.tsx         # Administración de usuarios
│   ├── reports.tsx       # Reportes y analítica
│   └── api/              # API Routes (backend)
│
├── components/           # 🟨 Componentes React
│   ├── auth/            # Componentes de autenticación
│   │   ├── RegisterForm.tsx
│   │   └── RegistrationSuccess.tsx
│   ├── layout/          # Layout y navegación
│   │   ├── Sidebar.tsx
│   │   └── UserProfile.tsx
│   ├── movements/       # Gestión de movimientos
│   │   ├── MovementForm.tsx
│   │   ├── MovementTable.tsx
│   │   ├── MovementRow.tsx
│   │   ├── MovementFilters.tsx
│   │   └── MovementStats.tsx
│   ├── reports/         # Reportes y gráficas
│   │   ├── MonthlyChart.tsx
│   │   ├── DistributionChart.tsx
│   │   ├── ReportStats.tsx
│   │   └── RecentMovementsTable.tsx
│   ├── users/           # Administración usuarios
│   │   ├── UserTable.tsx
│   │   ├── UserRow.tsx
│   │   ├── UserEditForm.tsx
│   │   └── UserSearch.tsx
│   └── ui/              # Componentes UI genéricos
│       ├── Button.tsx
│       ├── Card.tsx
│       ├── Modal.tsx
│       ├── EmptyState.tsx
│       └── Input.tsx
│
├── hooks/                # 🟧 Custom Hooks
│   ├── useAuth.ts       # Hook de autenticación
│   ├── useMovements.ts  # Hook de movimientos
│   ├── useUsers.ts      # Hook de usuarios
│   └── useReports.ts    # Hook de reportes
│
├── contexts/             # 🟥 React Context
│   └── AuthContext.tsx  # Context de autenticación
│
├── lib/                  # 🟪 Librerías y utilidades
│   ├── client/          # Cliente HTTP
│   │   ├── api/
│   │   │   └── client.ts      # Cliente API centralizado
│   │   ├── services/          # Services por dominio
│   │   │   ├── movements.service.ts
│   │   │   ├── users.service.ts
│   │   │   └── reports.service.ts
│   │   └── types/             # Tipos TypeScript
│   │       ├── movement.types.ts
│   │       ├── user.types.ts
│   │       └── report.types.ts
│   ├── utils/           # Utilidades
│   │   ├── formatters.ts    # Formateo de datos
│   │   └── errors.ts        # Manejo de errores
│   └── constants.ts     # Constantes globales
│
└── styles/               # 🎨 Estilos
    └── globals.css      # Estilos globales con Tailwind
```

---

## 🏗️ Arquitectura en Capas (Frontend)

### Diagrama de Flujo

```
┌───────────────────────────────────────────────────────┐
│              PAGES (Rutas / Next.js)                  │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐               │
│  │ index   │  │movement │  │ users   │               │
│  └────┬────┘  └────┬────┘  └────┬────┘               │
└───────┼────────────┼────────────┼─────────────────────┘
        │            │            │
        └────────────┴────────────┘
                     │
        ┌────────────▼──────────────┐
        │  COMPONENTS (UI Lógica)   │
        │  ┌──────────────────────┐ │
        │  │ MovementTable        │ │
        │  │ UserForm             │ │
        │  │ ReportChart          │ │
        │  └──────────────────────┘ │
        └────────────┬──────────────┘
                     │
        ┌────────────▼──────────────┐
        │  HOOKS (Estado + Lógica)  │
        │  ┌──────────────────────┐ │
        │  │ useMovements         │ │
        │  │ useUsers             │ │
        │  │ useAuth              │ │
        │  └──────────────────────┘ │
        └────────────┬──────────────┘
                     │
        ┌────────────▼──────────────┐
        │  SERVICES (API Client)    │
        │  ┌──────────────────────┐ │
        │  │ movementsService     │ │
        │  │ usersService         │ │
        │  └──────────────────────┘ │
        └────────────┬──────────────┘
                     │ HTTP
        ┌────────────▼──────────────┐
        │  API ROUTES (Backend)     │
        │  /api/movements           │
        │  /api/users               │
        └───────────────────────────┘
```

---

## 🔷 CAPA 1: Pages (Rutas)

### Responsabilidades
- Define rutas de la aplicación
- Renderiza layout principal
- Orquesta componentes grandes
- Maneja parámetros de URL

### Ejemplo: movements.tsx
```typescript
import { useMovements } from '@/hooks/useMovements';
import { MovementTable } from '@/components/movements/MovementTable';
import { MovementFilters } from '@/components/movements/MovementFilters';
import { MovementStats } from '@/components/movements/MovementStats';
import { MovementForm } from '@/components/movements/MovementForm';

export default function MovementsPage() {
  const [filters, setFilters] = useState<MovementFilters>({});
  const { movements, loading, createMovement, deleteMovement, stats } = useMovements({ filters });

  return (
    <Layout>
      <Head>
        <title>Movimientos - Sistema de Gestión</title>
      </Head>
      
      <div className="container">
        <h1>Gestión de Movimientos</h1>
        
        <MovementStats stats={stats} />
        
        <MovementFilters 
          filters={filters} 
          onChange={setFilters} 
        />
        
        <MovementForm 
          onSubmit={createMovement} 
        />
        
        <MovementTable 
          movements={movements}
          loading={loading}
          onDelete={deleteMovement}
        />
      </div>
    </Layout>
  );
}
```

### Características
- ✅ Minimalismo: solo orquestación
- ✅ Delegación: lógica en hooks y components
- ✅ SEO: uso de `<Head>` para metadata

---

## 🔶 CAPA 2: Components (Componentes UI)

### Responsabilidades
- Renderizado de UI
- Manejo de eventos del usuario
- Validación visual
- Estilos con Tailwind CSS

### Organización por Dominio

#### ¿Por qué separados por carpetas (auth, movements, users, reports)?

**Razones:**

1. **Cohesión Alta**: Componentes relacionados están juntos
2. **Navegación Fácil**: Encuentra componentes por feature
3. **Escalabilidad**: Agregar features no afecta otras carpetas
4. **Ownership Claro**: Cada equipo puede trabajar en su carpeta
5. **Reusabilidad**: Componentes UI genéricos en `ui/`

### Ejemplo: MovementTable.tsx
```typescript
interface MovementTableProps {
  movements: MovementResponseDTO[];
  loading: boolean;
  onDelete: (id: string) => Promise<void>;
}

export function MovementTable({ movements, loading, onDelete }: MovementTableProps) {
  if (loading) return <LoadingSpinner />;
  
  if (movements.length === 0) {
    return <EmptyState message="No hay movimientos registrados" />;
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead>
          <tr>
            <th>Tipo</th>
            <th>Monto</th>
            <th>Concepto</th>
            <th>Fecha</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {movements.map(movement => (
            <MovementRow 
              key={movement.id}
              movement={movement}
              onDelete={onDelete}
            />
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

### Principios de Componentes

#### 1. **Single Responsibility**
```typescript
// ❌ MAL: Componente que hace demasiado
function MovementPage() {
  // Fetch data
  // Render table
  // Render form
  // Handle filters
  // Handle stats
}

// ✅ BIEN: Componentes específicos
<MovementStats stats={stats} />
<MovementFilters onChange={setFilters} />
<MovementForm onSubmit={handleSubmit} />
<MovementTable movements={movements} />
```

#### 2. **Props Explícitas**
```typescript
// ❌ MAL: Props ambiguas
interface Props {
  data: any;
  onClick: Function;
}

// ✅ BIEN: Props tipadas y descriptivas
interface MovementRowProps {
  movement: MovementResponseDTO;
  onDelete: (id: string) => Promise<void>;
  onEdit?: (movement: MovementResponseDTO) => void;
}
```

#### 3. **Composición sobre Herencia**
```typescript
// ✅ BIEN: Composición
function Card({ children, title }: CardProps) {
  return (
    <div className="card">
      <h3>{title}</h3>
      {children}
    </div>
  );
}

// Uso
<Card title="Estadísticas">
  <MovementStats stats={stats} />
</Card>
```

---

## 🔷 CAPA 3: Hooks (Lógica de Estado)

### Responsabilidades
- Gestión de estado local
- Llamadas a services
- Lógica de negocio del cliente
- Side effects (useEffect)

### Ejemplo: useMovements.ts
```typescript
export function useMovements(options: UseMovementsOptions = {}) {
  const { autoFetch = true, filters } = options;

  const [movements, setMovements] = useState<MovementResponseDTO[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch movements
  const fetchMovements = useCallback(async (customFilters?: MovementFilters) => {
    setLoading(true);
    setError(null);

    try {
      const data = await movementsService.getMovements(customFilters || filters);
      setMovements(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido');
    } finally {
      setLoading(false);
    }
  }, [filters]);

  // Create movement
  const createMovement = useCallback(async (data: CreateMovementDTO) => {
    setLoading(true);
    try {
      const newMovement = await movementsService.createMovement(data);
      setMovements(prev => [newMovement, ...prev]);
      return { success: true, data: newMovement };
    } catch (err) {
      return { success: false, error: err.message };
    } finally {
      setLoading(false);
    }
  }, []);

  // Delete movement
  const deleteMovement = useCallback(async (id: string) => {
    setLoading(true);
    try {
      await movementsService.deleteMovement(id);
      setMovements(prev => prev.filter(m => m.id !== id));
      return { success: true };
    } catch (err) {
      return { success: false, error: err.message };
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

  // Computed stats
  const stats: MovementStats = useMemo(() => {
    return movementsService.calculateStats(movements);
  }, [movements]);

  return {
    movements,
    loading,
    error,
    stats,
    fetchMovements,
    createMovement,
    deleteMovement,
  };
}
```

### Ventajas de Custom Hooks

1. **Reusabilidad**: Un hook puede usarse en múltiples componentes
2. **Testabilidad**: Se pueden testear independientemente
3. **Separación de Responsabilidades**: Componentes solo renderizan, hooks manejan lógica
4. **Composición**: Hooks pueden usar otros hooks

### Hooks en el Proyecto

| Hook | Propósito |
|------|-----------|
| `useAuth` | Autenticación, usuario actual, login/logout |
| `useMovements` | CRUD de movimientos, filtros, estadísticas |
| `useUsers` | CRUD de usuarios, búsqueda |
| `useReports` | Reportes, balance, gráficas |

---

## 🔶 CAPA 4: Services (Cliente API)

### Responsabilidades
- Comunicación HTTP con backend
- Serialización/deserialización de datos
- Manejo de errores HTTP
- Transformación de datos

### Ejemplo: movements.service.ts
```typescript
class MovementsService {
  async getMovements(filters?: MovementFilters): Promise<MovementResponseDTO[]> {
    const queryParams = new URLSearchParams();
    if (filters?.type) queryParams.append('type', filters.type);
    if (filters?.startDate) queryParams.append('startDate', filters.startDate);
    if (filters?.endDate) queryParams.append('endDate', filters.endDate);

    const query = queryParams.toString();
    const endpoint = `/movements${query ? `?${query}` : ''}`;

    const response = await apiClient.get<MovementResponseDTO[]>(endpoint);
    return response.data || [];
  }

  async createMovement(data: CreateMovementDTO): Promise<MovementResponseDTO> {
    const response = await apiClient.post<MovementResponseDTO>('/movements', data);
    if (!response.data) {
      throw new Error('No data returned from server');
    }
    return response.data;
  }

  async deleteMovement(id: string): Promise<void> {
    await apiClient.delete<void>(`/movements/${id}`);
  }

  calculateStats(movements: MovementResponseDTO[]): MovementStats {
    const stats = movements.reduce(
      (acc, movement) => {
        acc.count++;
        if (movement.type === 'INCOME') {
          acc.totalIncome += Number(movement.amount);
        } else {
          acc.totalExpense += Number(movement.amount);
        }
        return acc;
      },
      { count: 0, totalIncome: 0, totalExpense: 0, balance: 0 }
    );

    stats.balance = stats.totalIncome - stats.totalExpense;
    return stats;
  }
}

export const movementsService = new MovementsService();
```

### API Client Centralizado

```typescript
// lib/client/api/client.ts
class ApiClient {
  private baseURL = '/api';

  async get<T>(endpoint: string): Promise<ApiResponse<T>> {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
    });

    if (!response.ok) {
      throw await this.handleError(response);
    }

    return response.json();
  }

  async post<T>(endpoint: string, data: unknown): Promise<ApiResponse<T>> {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw await this.handleError(response);
    }

    return response.json();
  }

  async delete<T>(endpoint: string): Promise<ApiResponse<T>> {
    // Similar implementation
  }

  private async handleError(response: Response): Promise<Error> {
    const errorData = await response.json().catch(() => ({}));
    return new Error(errorData.error || `HTTP ${response.status}`);
  }
}

export const apiClient = new ApiClient();
```

### Ventajas del Service Layer

1. ✅ **Centralización**: Un solo lugar para lógica de API
2. ✅ **Reutilización**: Services pueden usarse en múltiples hooks
3. ✅ **Testing**: Fácil de mockear
4. ✅ **Cambio de Backend**: Cambiar solo services, no hooks/components

---

## 🔷 CAPA 5: Context (Estado Global)

### Responsabilidades
- Estado compartido entre múltiples componentes
- Evitar prop drilling

### Ejemplo: AuthContext.tsx
```typescript
interface AuthContextValue {
  user: User | null;
  loading: boolean;
  error: string | null;
  isAdmin: boolean;
  isAuthenticated: boolean;
  signIn: () => Promise<void>;
  signOut: () => Promise<void>;
  refetch: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const auth = useAuth(); // Hook que maneja lógica

  return <AuthContext.Provider value={auth}>{children}</AuthContext.Provider>;
}

export function useAuthContext() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuthContext must be used within an AuthProvider');
  }
  return context;
}
```

### Uso
```typescript
// _app.tsx
function MyApp({ Component, pageProps }: AppProps) {
  return (
    <AuthProvider>
      <Component {...pageProps} />
    </AuthProvider>
  );
}

// En cualquier componente
function UserProfile() {
  const { user, isAdmin, signOut } = useAuthContext();
  
  return (
    <div>
      <p>{user?.name}</p>
      {isAdmin && <AdminBadge />}
      <button onClick={signOut}>Cerrar sesión</button>
    </div>
  );
}
```

---

## 🎨 Patrones Frontend Utilizados

### 1. Container/Presentational Pattern
```typescript
// Container (lógica)
function MovementsContainer() {
  const { movements, loading, deleteMovement } = useMovements();
  
  return (
    <MovementsTable 
      movements={movements}
      loading={loading}
      onDelete={deleteMovement}
    />
  );
}

// Presentational (UI pura)
function MovementsTable({ movements, loading, onDelete }: Props) {
  return <table>...</table>;
}
```

### 2. Render Props
```typescript
<DataFetcher
  url="/api/movements"
  render={(data, loading) => (
    loading ? <Spinner /> : <MovementList movements={data} />
  )}
/>
```

### 3. Compound Components
```typescript
<Card>
  <Card.Header>
    <Card.Title>Movimientos</Card.Title>
  </Card.Header>
  <Card.Body>
    <MovementTable />
  </Card.Body>
</Card>
```

---

## 🎯 Preguntas y Respuestas

### ¿Por qué separar components por carpetas (auth, movements, users)?

**Respuesta:**
- **Escalabilidad**: Cada feature es independiente
- **Organización**: Fácil encontrar componentes relacionados
- **Ownership**: Equipos pueden trabajar en paralelo
- **Cohesión**: Componentes relacionados juntos

### ¿Por qué usar Services en lugar de llamar fetch directamente?

**Respuesta:**
- **Reutilización**: Lógica de API en un solo lugar
- **Testabilidad**: Fácil mockear services
- **Mantenibilidad**: Cambios en API afectan solo services
- **Type Safety**: DTOs tipados

### ¿Por qué Custom Hooks?

**Respuesta:**
- **Separación de Responsabilidades**: Componentes solo renderizan
- **Reusabilidad**: Hooks usables en múltiples componentes
- **Testabilidad**: Hooks testeables independientemente
- **Composición**: Hooks pueden usar otros hooks

---

## 📚 Continúa Leyendo

➡️ **Siguiente documento**: [13 - FAQ Revisión Técnica](./13-FAQ-REVISION-TECNICA.md) (más importante para el martes)

---

**Última actualización:** Febrero 2026
