# 1️⃣1️⃣ Complejidades y Desafíos

## 🎯 Introducción

Este documento identifica las **partes más complejas** del sistema y cómo abordarlas. Útil para entender dónde prestar más atención durante mantenimiento o extensión.

---

## 🔴 Top 5 Complejidades del Sistema

### 1. Mapeo entre Capas (★★★★★)

**¿Qué es?** Transformar datos entre representaciones de diferentes capas.

**Flujo completo:**
```
PostgreSQL (Prisma)
    ↓ mapeo
Domain Entity (Movement)
    ↓ mapeo
DTO (Application)
    ↓ serialización
JSON (API Response)
```

**Código real:**
```typescript
// 1. Prisma (Infrastructure) → Domain Entity
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
  
  // Mapeo con validación
  return Movement.create({
    id: prismaMovement.id,
    type: prismaMovement.type as MovementType,
    amount: Number(prismaMovement.amount),  // Decimal → number
    concept: prismaMovement.concept,
    date: prismaMovement.date,
    userId: prismaMovement.userId,
    createdAt: prismaMovement.createdAt,
    updatedAt: prismaMovement.updatedAt,
  });
}

// 2. Domain Entity → DTO (en Use Case)
const response: CreateMovementResponse = {
  id: movement.id,
  type: movement.type,
  amount: movement.amount,
  concept: movement.concept,
  date: movement.date,
  userId: movement.userId,
  createdAt: movement.createdAt,
  updatedAt: movement.updatedAt,
};
```

**¿Por qué es complejo?**
- Muchas transformaciones manuales
- Conversión de tipos (Decimal → number, Date → ISO string)
- Mantener sincronizados diferentes modelos
- Fácil olvidar campos

**Estrategias de mitigación:**

#### 1. Mapper Classes
```typescript
class MovementMapper {
  static toDomain(prisma: PrismaMovement): Movement {
    return Movement.create({
      id: prisma.id,
      type: prisma.type as MovementType,
      amount: Number(prisma.amount),
      concept: prisma.concept,
      date: prisma.date,
      userId: prisma.userId,
      createdAt: prisma.createdAt,
      updatedAt: prisma.updatedAt,
    });
  }
  
  static toDTO(domain: Movement): MovementResponseDTO {
    return {
      id: domain.id,
      type: domain.type,
      amount: domain.amount,
      concept: domain.concept,
      date: domain.date,
      userId: domain.userId,
      createdAt: domain.createdAt,
      updatedAt: domain.updatedAt,
    };
  }
}
```

#### 2. Tests de Mapeo
```typescript
describe('MovementMapper', () => {
  it('should map from Prisma to Domain correctly', () => {
    const prismaMovement = createMockPrismaMovement();
    const domainMovement = MovementMapper.toDomain(prismaMovement);
    
    expect(domainMovement.id).toBe(prismaMovement.id);
    expect(domainMovement.amount).toBe(Number(prismaMovement.amount));
  });
});
```

---

### 2. Gestión de Estado de Autenticación (★★★★☆)

**¿Qué es?** Mantener sincronizado el estado de usuario entre cliente y servidor.

**Complejidad:**
- OAuth flow (GitHub)
- Email verification
- Session management
- Refresh tokens
- SSR con Next.js (sincronizar server y client)

**Flujo completo:**
```
1. Usuario hace clic en "Login with GitHub"
2. Redirect a GitHub OAuth
3. GitHub callback con code
4. Exchange code por token
5. Crear sesión en DB
6. Crear cookie httpOnly
7. Redirect a app
8. Fetch user data
9. Actualizar Context
10. Renderizar UI autenticada
```

**Código:**
```typescript
// hooks/useAuth.ts
export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchUser() {
      try {
        const session = await authClient.getSession();
        setUser(session?.user || null);
      } catch (error) {
        console.error('Error fetching user:', error);
        setUser(null);
      } finally {
        setLoading(false);
      }
    }
    
    fetchUser();
  }, []);

  const signIn = async () => {
    await authClient.signIn.social({
      provider: 'github',
      callbackURL: '/dashboard',
    });
  };

  const signOut = async () => {
    await authClient.signOut();
    setUser(null);
  };

  return {
    user,
    loading,
    isAuthenticated: !!user,
    isAdmin: user?.role === 'ADMIN',
    signIn,
    signOut,
  };
}
```

**Problemas comunes:**
- Race conditions (múltiples requests simultáneos)
- Estado desincronizado (server dice autenticado, client dice no)
- Manejo de errores (token expirado, network failure)
- SSR: session en servidor vs cliente

**Mitigaciones:**

#### 1. Context Provider Robusto
```typescript
export function AuthProvider({ children }: { children: ReactNode }) {
  const auth = useAuth();

  // Manejar errores de autenticación globalmente
  useEffect(() => {
    function handleAuthError(event: CustomEvent) {
      if (event.detail.status === 401) {
        auth.signOut();
      }
    }
    
    window.addEventListener('auth-error', handleAuthError as any);
    return () => window.removeEventListener('auth-error', handleAuthError as any);
  }, [auth]);

  return <AuthContext.Provider value={auth}>{children}</AuthContext.Provider>;
}
```

#### 2. Interceptor para Errores de Auth
```typescript
// lib/client/api/client.ts
async get<T>(endpoint: string): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      credentials: 'include',
    });
    
    if (response.status === 401) {
      // Emitir evento de error de auth
      window.dispatchEvent(new CustomEvent('auth-error', { 
        detail: { status: 401 } 
      }));
      throw new Error('Unauthorized');
    }
    
    return response.json();
  } catch (error) {
    throw error;
  }
}
```

---

### 3. Validación Distribuida (★★★★☆)

**¿Qué es?** Validaciones en múltiples capas pueden crear inconsistencias.

**Problema:**
```
API Layer: ¿Valido aquí?
    ↓
Use Case: ¿O aquí?
    ↓
Domain: ¿O aquí?
```

**Ejemplo real:**

```typescript
// 🤔 ¿Dónde valido que el monto sea positivo?

// Opción 1: API Layer
if (amount <= 0) {
  return res.status(400).json({ error: 'Amount must be positive' });
}

// Opción 2: Use Case
if (input.amount <= 0) {
  return Result.fail('Amount must be positive');
}

// Opción 3: Domain (Value Object)
class Money {
  static create(amount: number): Money {
    if (amount <= 0) throw new Error('Amount must be positive');
    return new Money(amount);
  }
}
```

**Solución: Regla de Validación**

| Tipo de Validación | Capa | Ejemplo |
|-------------------|------|---------|
| **Formato** | API / DTO | ¿Es un número? ¿Es una fecha válida? |
| **Negocio** | Use Case | ¿El usuario tiene permisos? ¿La operación es válida? |
| **Invariantes de Dominio** | Value Object | ¿El monto es >= 0? ¿El email es válido? |

**Implementación correcta:**
```typescript
// 1. API Layer: Validación de FORMATO
if (typeof amount !== 'number') {
  return res.status(400).json({ error: 'Amount must be a number' });
}

// 2. Use Case: Validación de NEGOCIO
if (req.user.role !== 'ADMIN') {
  return Result.fail('Only admins can create movements');
}

// 3. Domain: Validación de INVARIANTES
class Money {
  static create(amount: number): Money {
    if (amount < 0) throw new Error('Amount cannot be negative');
    if (amount > 999999999.99) throw new Error('Amount too large');
    return new Money(amount);
  }
}
```

---

### 4. Testing E2E con Autenticación (★★★★☆)

**¿Qué es?** Testear flujos completos requiere usuario autenticado.

**Problema:**
```typescript
// ❌ No puedo simplemente hacer:
test('should create movement', async () => {
  const response = await fetch('/api/movements', {
    method: 'POST',
    body: JSON.stringify({ ... }),
  });
  // Falla: 401 Unauthorized
});
```

**Solución 1: Helper de Autenticación**
```typescript
// __tests__/helpers/auth.ts
export async function createAuthenticatedUser(role: Role = 'ADMIN'): Promise<{
  user: User;
  session: string;
}> {
  // 1. Crear usuario en DB
  const user = await prisma.user.create({
    data: {
      name: 'Test User',
      email: `test-${Date.now()}@example.com`,
      role,
      emailVerified: true,
    },
  });
  
  // 2. Crear sesión
  const session = await prisma.session.create({
    data: {
      userId: user.id,
      token: generateToken(),
      expiresAt: new Date(Date.now() + 86400000), // 24h
    },
  });
  
  return { user, session: session.token };
}

// Uso en tests
test('should create movement as admin', async () => {
  const { session } = await createAuthenticatedUser('ADMIN');
  
  const response = await fetch('/api/movements', {
    method: 'POST',
    headers: {
      'Cookie': `session=${session}`,
    },
    body: JSON.stringify({
      type: 'INCOME',
      amount: 100,
      concept: 'Test',
      date: new Date().toISOString(),
    }),
  });
  
  expect(response.status).toBe(201);
});
```

**Solución 2: Mock de Middleware**
```typescript
// Para tests unitarios de API routes
jest.mock('@/lib/server/presentation/middlewares/withAuth', () => ({
  withAuth: (handler: any) => handler, // No-op
}));

// Luego en el test
test('should handle request', async () => {
  const req = {
    method: 'POST',
    body: { ... },
    user: { id: 'user-1', role: 'ADMIN' }, // Usuario mockeado
  };
  
  await handler(req, res);
});
```

---

### 5. Sincronización Frontend-Backend (★★★☆☆)

**¿Qué es?** Mantener el estado del frontend sincronizado con el backend.

**Problemas comunes:**

#### Problema 1: Estado Optimista
```typescript
// Usuario crea movimiento
const createMovement = async (data: CreateMovementDTO) => {
  // 1. Actualizar UI inmediatamente (optimistic)
  setMovements(prev => [{ ...data, id: 'temp' }, ...prev]);
  
  try {
    // 2. Enviar al servidor
    const created = await movementsService.createMovement(data);
    
    // 3. Reemplazar temp con real
    setMovements(prev => 
      prev.map(m => m.id === 'temp' ? created : m)
    );
  } catch (error) {
    // 4. Rollback si falla
    setMovements(prev => prev.filter(m => m.id !== 'temp'));
    showError(error.message);
  }
};
```

#### Problema 2: Invalidación de Cache
```typescript
// Usuario edita movimiento en otra pestaña → ¿cómo sincronizar?

// Solución: Polling
useEffect(() => {
  const interval = setInterval(() => {
    fetchMovements();
  }, 30000); // Cada 30 segundos
  
  return () => clearInterval(interval);
}, []);

// Solución mejor: WebSockets (futuro)
useEffect(() => {
  const socket = io();
  
  socket.on('movement:created', (movement) => {
    setMovements(prev => [movement, ...prev]);
  });
  
  socket.on('movement:deleted', (id) => {
    setMovements(prev => prev.filter(m => m.id !== id));
  });
  
  return () => socket.disconnect();
}, []);
```

#### Problema 3: Errores de Network
```typescript
function useMovements() {
  const [error, setError] = useState<string | null>(null);
  const [retrying, setRetrying] = useState(false);

  const fetchMovements = async (attempt = 1) => {
    try {
      const data = await movementsService.getMovements();
      setMovements(data);
      setError(null);
    } catch (err) {
      if (attempt < 3) {
        setRetrying(true);
        await delay(1000 * attempt); // Exponential backoff
        return fetchMovements(attempt + 1);
      }
      setError('Error de red. Por favor, intenta de nuevo.');
      setRetrying(false);
    }
  };

  return { movements, error, retrying, fetchMovements };
}
```

---

## 🟡 Complejidades Medias

### 6. Manejo de Fechas (★★★☆☆)

**Problemas:**
- Timezone del cliente vs servidor
- Formato ISO vs locale
- Date en JS vs Prisma DateTime

**Soluciones:**
```typescript
// Siempre almacenar en UTC
const movement = await prisma.movement.create({
  data: {
    date: new Date(input.date), // Convertir a UTC
  },
});

// Formatear en frontend según locale
const formatted = new Intl.DateTimeFormat('es-ES', {
  year: 'numeric',
  month: 'long',
  day: 'numeric',
}).format(movement.date);
```

---

### 7. Números Decimales (★★★☆☆)

**Problemas:**
- Precisión de punto flotante en JavaScript
- Prisma Decimal vs JS number
- Formateo de moneda

**Soluciones:**
```typescript
// En DB: Decimal(12, 2)
model Movement {
  amount Decimal @db.Decimal(12, 2)
}

// En código: Redondear a 2 decimales
class Money {
  static create(amount: number): Money {
    const rounded = Math.round(amount * 100) / 100;
    return new Money(rounded);
  }
}

// En frontend: Formatear
const formatted = new Intl.NumberFormat('es-ES', {
  style: 'currency',
  currency: 'USD',
}).format(movement.amount);
// "$1,234.56"
```

---

## 🎯 Estrategias Generales para Manejar Complejidad

### 1. Documentación
- ✅ Este documento
- ✅ Comentarios JSDoc en funciones críticas
- ✅ README en cada módulo complejo

### 2. Tests
- ✅ Tests unitarios para lógica compleja
- ✅ Tests de integración para flujos E2E
- ✅ Tests específicos para casos edge

### 3. Helpers y Utilities
- ✅ Mappers para transformaciones
- ✅ Formatters para presentación
- ✅ Validators centralizados

### 4. Error Handling Robusto
```typescript
try {
  // Operación compleja
} catch (error) {
  logger.error('Error en operación X', {
    error: error.message,
    stack: error.stack,
    context: { ... },
  });
  
  // Fallback o retry
}
```

### 5. Logging Estructurado
```typescript
logger.info('Movement created', {
  movementId: movement.id,
  userId: user.id,
  amount: movement.amount,
  timestamp: new Date(),
});
```

---

## 📊 Matriz de Complejidad

| Aspecto | Complejidad | Mitigación | Prioridad |
|---------|-------------|------------|-----------|
| Mapeo entre capas | 🔴 Alta | Mappers, tests | 🔴 Alta |
| Autenticación | 🔴 Alta | Better Auth, Context | 🔴 Alta |
| Validación distribuida | 🟡 Media | Reglas claras por capa | 🟡 Media |
| Testing E2E | 🟡 Media | Helpers de auth | 🟡 Media |
| Sincronización FE-BE | 🟡 Media | Estado optimista, polling | 🟢 Baja |
| Fechas | 🟡 Media | UTC siempre | 🟢 Baja |
| Decimales | 🟡 Media | Money VO, Decimal en DB | 🟢 Baja |

---

## 🚀 Cuando Necesitas Trabajar en Código Complejo

### Checklist:
1. ✅ Lee la documentación relevante
2. ✅ Revisa tests existentes
3. ✅ Escribe tests antes de modificar
4. ✅ Haz cambios pequeños e incrementales
5. ✅ Verifica que tests pasen
6. ✅ Actualiza documentación si es necesario
7. ✅ Code review con otro desarrollador

---

## 📚 Continúa Leyendo

➡️ **Documento más importante**: [13 - FAQ Revisión Técnica](./13-FAQ-REVISION-TECNICA.md)

---

**Última actualización:** Febrero 2026
