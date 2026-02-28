# 📗 Next.js Explicado

## 🎯 Introducción

Este documento explica todos los conceptos de **Next.js** usados en el proyecto. Next.js es un framework sobre React que agrega SSR, routing, API routes, y más.

---

## 📋 Índice

1. [¿Qué es Next.js?](#1-qué-es-nextjs)
2. [Pages Router vs App Router](#2-pages-router-vs-app-router)
3. [Estructura de Carpetas](#3-estructura-de-carpetas)
4. [Archivos Especiales](#4-archivos-especiales)
5. [Sistema de Routing](#5-sistema-de-routing)
6. [API Routes](#6-api-routes)
7. [Rendering (SSR, SSG, CSR)](#7-rendering-ssr-ssg-csr)
8. [Fetching de Datos](#8-fetching-de-datos)
9. [Middlewares](#9-middlewares)
10. [Variables de Entorno](#10-variables-de-entorno)
11. [Configuración](#11-configuración)

---

## 1. ¿Qué es Next.js?

### Framework React con Baterías Incluidas

| React Solo | Next.js |
|------------|---------|
| Solo UI components | Framework completo |
| Sin routing | Routing automático |
| Sin backend | API Routes integradas |
| Client-side rendering | SSR, SSG, ISR |
| Configuras todo | Pre-configurado |

### Por Qué Usamos Next.js

```
✅ Routing automático basado en archivos
✅ API Routes para backend (sin Express/Nest)
✅ TypeScript nativo
✅ Optimización automática (imágenes, fonts)
✅ Deployment simple (Vercel)
✅ Hot Reload rápido
```

---

## 2. Pages Router vs App Router

### Next.js tiene 2 sistemas de routing

| Pages Router | App Router |
|--------------|------------|
| Carpeta `pages/` | Carpeta `app/` |
| Más antiguo (estable) | Más nuevo (Next.js 13+) |
| File-based routing | Server Components |
| `getServerSideProps` | `fetch()` con cache |
| Más documentación | Más features |

### 🎯 Este Proyecto Usa: Pages Router

```
pages/
├── _app.tsx          # Wrapper global
├── _document.tsx     # HTML structure
├── index.tsx         # Página: /
├── login.tsx         # Página: /login
├── movements.tsx     # Página: /movements
├── users.tsx         # Página: /users
├── reports.tsx       # Página: /reports
└── api/              # Backend routes
    ├── auth/
    ├── movements/
    ├── users/
    └── reports/
```

---

## 3. Estructura de Carpetas

### Carpetas con Significado Especial

```
proyecto/
├── pages/           # 👈 OBLIGATORIA: Define rutas
│   ├── api/         # 👈 ESPECIAL: Backend endpoints
│   ├── _app.tsx     # 👈 ESPECIAL: Wrapper
│   └── _document.tsx# 👈 ESPECIAL: HTML
├── public/          # 👈 ESPECIAL: Archivos estáticos
├── styles/          # CSS (convención)
├── components/      # React components (convención)
├── hooks/           # Custom hooks (convención)
├── lib/             # Código compartido (convención)
└── ...
```

### 📁 `pages/` - Obligatoria

**Cada archivo = Una ruta automática**

```
pages/index.tsx      →  /
pages/login.tsx      →  /login
pages/users.tsx      →  /users
pages/about.tsx      →  /about
pages/blog/post.tsx  →  /blog/post
```

### 📁 `public/` - Especial

Archivos accesibles directamente:

```
public/logo.png      →  https://site.com/logo.png
public/favicon.ico   →  https://site.com/favicon.ico
public/images/bg.jpg →  https://site.com/images/bg.jpg
```

### 📁 Otras Carpetas - Convenciones

```
components/  # UI Components (no es especial para Next.js)
hooks/       # Custom hooks
lib/         # Lógica compartida
styles/      # CSS files
contexts/    # React contexts
```

---

## 4. Archivos Especiales

### 📄 `_app.tsx` - Application Wrapper

**¿Qué es?** El componente que envuelve TODAS las páginas. Se ejecuta en cada navegación.

**¿Para qué?**
- Providers globales (Auth, Theme)
- Layout global
- Estado global
- CSS global

**En este proyecto:**
```tsx
// pages/_app.tsx
import type { AppProps } from 'next/app';
import '@/styles/globals.css';

const App = ({ Component, pageProps }: AppProps) => {
  return <Component {...pageProps} />;
};

export default App;
```

**Con providers (típico):**
```tsx
const App = ({ Component, pageProps }: AppProps) => {
  return (
    <AuthProvider>        {/* Contexto de autenticación */}
      <ThemeProvider>      {/* Contexto de tema */}
        <Layout>           {/* Layout común */}
          <Component {...pageProps} />
        </Layout>
      </ThemeProvider>
    </AuthProvider>
  );
};
```

### 📄 `_document.tsx` - HTML Document

**¿Qué es?** Customiza el HTML que envuelve la app. Solo se ejecuta en el servidor.

**¿Para qué?**
- Modificar `<html>` y `<body>`
- Agregar fonts
- Agregar scripts externos
- Meta tags globales

**En este proyecto:**
```tsx
// pages/_document.tsx
import { Html, Head, Main, NextScript } from 'next/document';

export default function Document() {
  return (
    <Html lang="es">
      <Head />
      <body>
        <Main />        {/* Aquí se renderiza la app */}
        <NextScript />  {/* Scripts de Next.js */}
      </body>
    </Html>
  );
}
```

### ⚠️ Diferencia _app vs _document

| `_app.tsx` | `_document.tsx` |
|------------|-----------------|
| Ejecuta en cliente Y servidor | Solo servidor |
| Se ejecuta en cada navegación | Solo una vez (inicial) |
| Para lógica React (hooks, state) | Para HTML puro |
| Puede usar hooks | NO puede usar hooks |
| Providers, layouts | html, head, scripts |

### 📄 `index.tsx` - Homepage

```
pages/index.tsx  →  https://tuapp.com/
```

Siempre que una carpeta tiene `index.tsx`, responde a la ruta de esa carpeta.

```
pages/index.tsx           →  /
pages/users/index.tsx     →  /users
pages/api/users/index.ts  →  /api/users
```

---

## 5. Sistema de Routing

### Routing Basado en Archivos

**Tu estructura de archivos ES tu routing:**

```
pages/
├── index.tsx           →  /
├── login.tsx           →  /login
├── register.tsx        →  /register
├── movements.tsx       →  /movements
├── users.tsx           →  /users
├── reports.tsx         →  /reports
├── verify-email.tsx    →  /verify-email
├── api-docs.tsx        →  /api-docs
└── api/
    ├── openapi.ts      →  /api/openapi
    ├── auth/
    │   └── [...all].ts →  /api/auth/*
    ├── movements/
    │   ├── index.ts    →  /api/movements
    │   └── [id].ts     →  /api/movements/:id
    └── users/
        ├── index.ts    →  /api/users
        └── [id].ts     →  /api/users/:id
```

### Rutas Dinámicas

**Archivos con `[param]` son dinámicos:**

```typescript
// pages/api/movements/[id].ts
// Responde a: /api/movements/123, /api/movements/abc, etc.

export default async function handler(req, res) {
  const { id } = req.query; // "123", "abc", etc.
  // ...
}
```

### Catch-All Routes

**Archivos con `[...param]` capturan todo:**

```typescript
// pages/api/auth/[...all].ts
// Responde a:
//   /api/auth/login
//   /api/auth/register
//   /api/auth/callback/github
//   /api/auth/cualquier/cosa

export default async function handler(req, res) {
  const { all } = req.query; 
  // ["login"], ["callback", "github"], etc.
}
```

### Navegación

**Con Link (preferido):**
```tsx
import Link from 'next/link';

<Link href="/movements">Ir a Movimientos</Link>
<Link href={`/users/${userId}`}>Ver Usuario</Link>
```

**Con useRouter (programática):**
```tsx
import { useRouter } from 'next/router';

const router = useRouter();

// Navegar
router.push('/movements');
router.push(`/users/${userId}`);

// Con query params
router.push({
  pathname: '/search',
  query: { keyword: 'test' }
});

// Reemplazar (sin agregar al historial)
router.replace('/login');

// Volver atrás
router.back();

// Leer parámetros actuales
const { id } = router.query;
const currentPath = router.pathname;
```

---

## 6. API Routes

### Backend Integrado

Los archivos en `pages/api/` son endpoints **del servidor**, no páginas React.

```
pages/api/
├── openapi.ts                  # GET /api/openapi
├── auth/
│   └── [...all].ts             # ALL /api/auth/*
├── movements/
│   ├── index.ts                # GET/POST /api/movements
│   └── [id].ts                 # GET/PUT/DELETE /api/movements/:id
├── users/
│   ├── index.ts                # GET/POST /api/users
│   └── [id].ts                 # GET/PUT/DELETE /api/users/:id
└── reports/
    ├── index.ts                # GET /api/reports
    ├── balance.ts              # GET /api/reports/balance
    ├── movements-count.ts      # GET /api/reports/movements-count
    ├── monthly.ts              # GET /api/reports/monthly
    └── distribution.ts         # GET /api/reports/distribution
```

### Estructura de un API Route

```typescript
// pages/api/movements/index.ts
import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  // req.method: GET, POST, PUT, DELETE
  // req.body: Body del request (POST/PUT)
  // req.query: Query parameters
  // req.cookies: Cookies
  // req.headers: Headers

  if (req.method === 'GET') {
    const movements = await getMovements();
    return res.status(200).json({ data: movements });
  }

  if (req.method === 'POST') {
    const movement = await createMovement(req.body);
    return res.status(201).json({ data: movement });
  }

  return res.status(405).json({ error: 'Method not allowed' });
}
```

### ⚡ API Routes en Este Proyecto

Usamos el patrón de **middlewares encadenados**:

```typescript
// pages/api/movements/index.ts
export default withErrorHandling(
  withAuth(
    async (req, res) => {
      // Ya pasó autenticación y error handling
      const service = new ApplicationService();
      
      if (req.method === 'GET') {
        const result = await service.getMovements(req.query);
        return res.json(result);
      }
      // ...
    }
  )
);
```

---

## 7. Rendering (SSR, SSG, CSR)

### 3 Formas de Renderizar

```
┌─────────────────────────────────────────────────────────────────┐
│                       RENDERING METHODS                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  CSR (Client-Side)      SSR (Server-Side)     SSG (Static)     │
│  ┌─────────────────┐    ┌─────────────────┐  ┌──────────────┐  │
│  │ JS → Browser    │    │ Server → HTML   │  │ Build → HTML │  │
│  │ renders page    │    │ on each request │  │ cached       │  │
│  └─────────────────┘    └─────────────────┘  └──────────────┘  │
│                                                                 │
│  Cuándo: Real-time     Cuándo: Auth pages  Cuándo: Blog,       │
│          dashboards              Dynamic            Landing     │
│          User data               User-specific      Docs        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### CSR - Client-Side Rendering

**El navegador descarga JS y renderiza la página.**

```tsx
// pages/movements.tsx
function MovementsPage() {
  const [movements, setMovements] = useState([]);
  
  useEffect(() => {
    // Fetch después de que carga la página
    fetch('/api/movements')
      .then(res => res.json())
      .then(data => setMovements(data));
  }, []);
  
  return <div>{/* render movements */}</div>;
}
```

**✅ Usado en este proyecto para:**
- Dashboard
- Movimientos
- Usuarios
- Reportes

### SSR - Server-Side Rendering

**El servidor genera HTML en cada request.**

```tsx
// pages/users/[id].tsx
export async function getServerSideProps(context) {
  const { id } = context.params;
  const user = await fetchUser(id);
  
  return {
    props: { user } // Se pasa al componente
  };
}

function UserPage({ user }) {
  return <div>{user.name}</div>;
}
```

### SSG - Static Site Generation

**HTML generado en build time.**

```tsx
// pages/about.tsx
export async function getStaticProps() {
  const content = await fetchCMSContent();
  
  return {
    props: { content },
    revalidate: 3600 // Regenerar cada hora (ISR)
  };
}

function AboutPage({ content }) {
  return <div>{content}</div>;
}
```

---

## 8. Fetching de Datos

### En Este Proyecto: Hooks + Services

```tsx
// pages/movements.tsx
import { useMovements } from '@/hooks/useMovements';

function MovementsPage() {
  const { 
    movements, 
    isLoading, 
    error,
    createMovement,
    updateMovement,
    deleteMovement 
  } = useMovements();

  if (isLoading) return <Loading />;
  if (error) return <Error message={error} />;

  return <MovementTable movements={movements} />;
}
```

**Hook internamente usa Service:**
```typescript
// hooks/useMovements.ts
export function useMovements() {
  const [movements, setMovements] = useState([]);
  
  useEffect(() => {
    movementsService.getAll()
      .then(setMovements);
  }, []);
  
  // ...
}
```

**Service llama a API:**
```typescript
// lib/client/services/movements.service.ts
class MovementsService {
  async getAll() {
    return apiClient.get('/api/movements');
  }
}
```

---

## 9. Middlewares

### Middlewares de API Routes

**En este proyecto, seguimos el patrón de HOF (Higher-Order Functions):**

```typescript
// lib/server/presentation/middlewares/withAuth.ts
export function withAuth(handler: NextApiHandler): NextApiHandler {
  return async (req, res) => {
    const session = await getSession(req);
    
    if (!session) {
      return res.status(401).json({ error: 'No autorizado' });
    }
    
    // Adjuntar usuario al request
    (req as any).user = session.user;
    
    // Continuar al handler original
    return handler(req, res);
  };
}
```

**Uso encadenado:**
```typescript
// pages/api/movements/index.ts
export default withErrorHandling(  // 3. Manejo de errores
  withAuth(                         // 2. Autenticación
    withRole(['ADMIN', 'USER'])(    // 1. Autorización
      async (req, res) => {
        // Handler protegido
      }
    )
  )
);
```

### Orden de Ejecución

```
Request llega a /api/movements
        ↓
withErrorHandling (try-catch global)
        ↓
withAuth (verifica sesión)
        ↓
withRole (verifica permisos)
        ↓
Handler (lógica de negocio)
        ↓
Response se envía
```

---

## 10. Variables de Entorno

### Archivos de Entorno

```
.env                # Base (git ignored)
.env.local          # Local overrides (git ignored)
.env.development    # Solo en desarrollo
.env.production     # Solo en producción
.env.example        # Template (commiteado)
```

### Variables Públicas vs Privadas

```bash
# ❌ PRIVADA - Solo en servidor
DATABASE_URL="postgresql://..."
BETTER_AUTH_SECRET="secret"
GITHUB_CLIENT_SECRET="secret"

# ✅ PÚBLICA - Disponible en cliente (prefijo NEXT_PUBLIC_)
NEXT_PUBLIC_API_URL="https://api.example.com"
NEXT_PUBLIC_APP_NAME="Mi App"
```

### Uso

```typescript
// ✅ En servidor (API routes, getServerSideProps)
const dbUrl = process.env.DATABASE_URL;

// ✅ En cliente (componentes)
const apiUrl = process.env.NEXT_PUBLIC_API_URL;

// ❌ En cliente - NO funciona (undefined)
const secret = process.env.BETTER_AUTH_SECRET;
```

---

## 11. Configuración

### 📄 `next.config.mjs`

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Modo estricto de React (detecta problemas)
  reactStrictMode: true,
  
  // Dominios permitidos para imágenes externas
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'avatars.githubusercontent.com'
      }
    ]
  },
  
  // Otras opciones comunes:
  // output: 'standalone',  // Para Docker
  // basePath: '/app',      // Sub-path deployment
  // i18n: { locales: [...] } // Internacionalización
};

export default nextConfig;
```

### 📄 `vercel.json`

```json
{
  "git": {
    "deploymentEnabled": {
      "main": true,
      "preview": false
    }
  }
}
```

---

## 🗺️ Flujo Completo de una Request

### Request a Página (ej: /movements)

```
1. Usuario visita /movements
         ↓
2. Next.js encuentra pages/movements.tsx
         ↓
3. _document.tsx genera HTML base
         ↓
4. _app.tsx envuelve con providers
         ↓
5. movements.tsx renderiza
         ↓
6. useMovements() hook se ejecuta
         ↓
7. Fetch a /api/movements
         ↓
8. Datos llegan, componente re-renderiza
```

### Request a API (ej: POST /api/movements)

```
1. Frontend llama: POST /api/movements
         ↓
2. Next.js encuentra pages/api/movements/index.ts
         ↓
3. withErrorHandling ejecuta
         ↓
4. withAuth verifica sesión
         ↓
5. withRole verifica permisos
         ↓
6. Handler procesa request
         ↓
7. ApplicationService ejecuta Use Case
         ↓
8. Repository guarda en DB
         ↓
9. Response { data: movement }
```

---

## 📝 Resumen de Archivos de Next.js

| Archivo | Propósito |
|---------|-----------|
| `pages/*.tsx` | Páginas/rutas |
| `pages/api/*.ts` | Backend endpoints |
| `pages/_app.tsx` | Wrapper global |
| `pages/_document.tsx` | HTML structure |
| `pages/[param].tsx` | Ruta dinámica |
| `pages/[...all].tsx` | Catch-all route |
| `public/*` | Archivos estáticos |
| `next.config.mjs` | Configuración |
| `.env*` | Variables de entorno |

---

## 🎓 Preguntas Frecuentes

### ¿Por qué `pages/` y no `src/pages/`?
Next.js busca `pages/` en la raíz O en `src/`. Elegimos raíz para mantener estructura más plana.

### ¿Por qué API Routes y no Express/Nest?
Simplicidad. Para este proyecto, API Routes son suficientes y evitan mantener 2 proyectos.

### ¿Por qué no App Router?
Pages Router es más estable, tiene más documentación, y el equipo lo conoce mejor.

### ¿Cómo escalo si necesito más backend?
Extraer la lógica de `lib/server/` a un microservicio separado es fácil porque ya está desacoplada.

---

## 📚 Continúa Leyendo

⬅️ **Anterior**: [06 - Conceptos TypeScript](./06-CONCEPTOS-TYPESCRIPT.md)
➡️ **Siguiente**: [11 - Complejidades](./11-COMPLEJIDADES.md)

---

**Última actualización:** Febrero 2026
