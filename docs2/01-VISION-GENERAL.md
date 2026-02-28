# 1️⃣ Visión General del Proyecto

## 🎯 ¿Qué es este Sistema?

**Sistema de Gestión de Ingresos y Egresos** es una aplicación web fullstack empresarial diseñada para gestionar movimientos financieros (ingresos y gastos) con un enfoque en escalabilidad, mantenibilidad y calidad de código.

---

## 🚀 Propósito del Sistema

### Problema que Resuelve
Las empresas y usuarios necesitan:
- **Registrar** todos sus movimientos financieros de forma estructurada
- **Filtrar y analizar** sus ingresos y egresos
- **Controlar el acceso** mediante roles y permisos
- **Generar reportes** para toma de decisiones
- **Auditar** quién creó cada movimiento

### Solución Propuesta
Un sistema robusto con:
- ✅ Arquitectura escalable (Clean Architecture + DDD)
- ✅ Validaciones de dominio rigurosas
- ✅ Sistema de autenticación OAuth + credentials
- ✅ Control de acceso basado en roles (RBAC)
- ✅ API REST documentada (OpenAPI/Swagger)
- ✅ Testing automatizado (198 tests)
- ✅ CI/CD con GitHub Actions
- ✅ Despliegue en Vercel

---

## 🛠️ Stack Tecnológico

### Frontend
| Tecnología | Versión | Propósito |
|-----------|---------|-----------|
| **Next.js** | 15.1.3 | Framework React con SSR/SSG |
| **React** | 18.3.1 | Librería de UI |
| **TypeScript** | 5.7.2 | Tipado estático |
| **Tailwind CSS** | 3.4.17 | Estilos utilitarios |
| **Recharts** | 3.7.0 | Gráficas y visualizaciones |
| **Lucide React** | - | Iconos |

### Backend
| Tecnología | Versión | Propósito |
|-----------|---------|-----------|
| **Next.js API Routes** | 15.1.3 | Backend serverless |
| **Prisma ORM** | 6.15.0 | ORM para PostgreSQL |
| **PostgreSQL** | - | Base de datos relacional |
| **Better Auth** | 1.1.1 | Autenticación OAuth + Credentials |
| **Nodemailer** | 7.0.13 | Envío de emails |
| **Mailtrap** | 4.4.0 | Testing de emails |

### Testing y Calidad
| Tecnología | Versión | Propósito |
|-----------|---------|-----------|
| **Jest** | 30.2.0 | Framework de testing |
| **Testing Library** | 16.3.2 | Testing de componentes React |
| **ESLint** | 9.17.0 | Linting de código |
| **Prettier** | 3.6.2 | Formateo de código |

### DevOps
- **GitHub Actions**: CI/CD automatizado
- **Vercel**: Despliegue en producción
- **TypeScript**: Compilación y type-checking

---

## 🎨 Funcionalidades Principales

### 1. Gestión de Movimientos 💰
- **Crear movimientos** (ingresos/egresos) con validación de dominio
- **Listar movimientos** con filtros avanzados (tipo, fecha, usuario)
- **Eliminar movimientos** con control de permisos
- **Trazabilidad completa**: cada movimiento registra quién lo creó
- **Validación monetaria**: montos entre $0.01 y $999,999,999.99

### 2. Sistema de Autenticación 🔐
- **OAuth GitHub**: Inicio de sesión con GitHub
- **Credentials**: Registro tradicional con email/contraseña
- **Verificación de email**: Confirmación por correo electrónico
- **Sesiones persistentes**: Almacenadas en base de datos
- **Control de acceso basado en roles** (RBAC):
  - `ADMIN`: Puede crear, editar y eliminar movimientos y usuarios
  - `USER`: Solo puede ver movimientos (funcionalidad futura)

### 3. Administración de Usuarios 👥
- **Listar usuarios** con búsqueda por nombre/email
- **Editar usuarios**: nombre, rol, teléfono
- **Eliminar usuarios** con validación de permisos
- **Estadísticas por usuario**: cantidad de movimientos creados
- **Validación de datos**: email RFC 5322, teléfono internacional

### 4. Reportes y Analítica 📊
- **Balance general**: ingresos, egresos, balance neto
- **Distribución por tipo**: % de ingresos vs egresos
- **Tendencia mensual**: gráfica de ingresos y egresos por mes
- **Movimientos recientes**: últimos 5 movimientos
- **Filtros por rango de fechas**

---

## 🏛️ Arquitectura de Alto Nivel

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │  Pages   │  │Components│  │  Hooks   │             │
│  └──────────┘  └──────────┘  └──────────┘             │
│         │              │              │                 │
│         └──────────────┴──────────────┘                 │
│                        │                                 │
│                 ┌──────▼──────┐                         │
│                 │   Services  │                         │
│                 └──────┬──────┘                         │
└─────────────────────────┼─────────────────────────────┘
                          │ HTTP/JSON
┌─────────────────────────▼─────────────────────────────┐
│              API LAYER (Next.js API Routes)            │
│  ┌──────────────┐  ┌──────────────┐                   │
│  │ Middlewares  │  │  API Routes  │                   │
│  └──────────────┘  └──────────────┘                   │
│         │                   │                           │
│         └───────────────────┘                           │
│                     │                                   │
│           ┌─────────▼──────────┐                       │
│           │ Application Service│                       │
│           └─────────┬──────────┘                       │
└──────────────────────┼──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│              CLEAN ARCHITECTURE LAYERS                   │
│                                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │  DOMAIN (Entities, ValueObjects, Events)        │   │
│  │  - Movement, User                               │   │
│  │  - Money, Email, Phone, Concept                 │   │
│  └─────────────────────────────────────────────────┘   │
│                       ▲                                  │
│  ┌────────────────────┴────────────────────────────┐   │
│  │  APPLICATION (Use Cases, DTOs)                  │   │
│  │  - CreateMovementUseCase                        │   │
│  │  - GetMovementsUseCase                          │   │
│  │  - UpdateUserUseCase                            │   │
│  └────────────────────┬────────────────────────────┘   │
│                       ▼                                  │
│  ┌─────────────────────────────────────────────────┐   │
│  │  INFRASTRUCTURE (Repositories, Prisma)          │   │
│  │  - PrismaMovementRepository                     │   │
│  │  - PrismaUserRepository                         │   │
│  └────────────────────┬────────────────────────────┘   │
│                       ▼                                  │
│  ┌─────────────────────────────────────────────────┐   │
│  │  DATABASE (PostgreSQL)                          │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Modelo de Datos Simplificado

```
┌──────────────────┐          ┌──────────────────┐
│      User        │          │    Movement      │
├──────────────────┤          ├──────────────────┤
│ id: string (PK)  │◄────────┤ userId (FK)      │
│ name: string     │ 1     N │ id: string (PK)  │
│ email: string    │          │ type: enum       │
│ role: enum       │          │ amount: decimal  │
│ phone: string?   │          │ concept: string  │
│ emailVerified    │          │ date: datetime   │
│ createdAt        │          │ createdAt        │
│ updatedAt        │          │ updatedAt        │
└──────────────────┘          └──────────────────┘
        │                             
        │ 1:N                         
        ▼                             
┌──────────────────┐          
│    Session       │          
├──────────────────┤          
│ id: string (PK)  │          
│ userId: string   │          
│ token: string    │          
│ expiresAt        │          
└──────────────────┘          
```

### Enums
- **Role**: `ADMIN`, `USER`
- **MovementType**: `INCOME`, `EXPENSE`

---

## 🎯 Casos de Uso Principales

### Para Administradores (ADMIN)
1. ✅ Iniciar sesión (GitHub OAuth o Email/Password)
2. ✅ Ver dashboard con reportes
3. ✅ Crear movimientos (ingresos/egresos)
4. ✅ Filtrar movimientos por tipo y fecha
5. ✅ Eliminar movimientos
6. ✅ Ver lista de usuarios
7. ✅ Editar información de usuarios
8. ✅ Eliminar usuarios
9. ✅ Ver reportes gráficos
10. ✅ Cerrar sesión

### Para Usuarios Normales (USER)
1. ✅ Iniciar sesión
2. ✅ Ver movimientos (sin poder crear/eliminar)
3. ✅ Ver reportes
4. ✅ Cerrar sesión

---

## 📈 Métricas del Proyecto

| Métrica | Valor |
|---------|-------|
| **Tests Automatizados** | 198 passing |
| **Cobertura de Código** | ~85% (lib/server) |
| **Líneas de Código** | ~5,000+ |
| **Componentes React** | 25+ |
| **API Endpoints** | 8 |
| **Entidades de Dominio** | 2 (User, Movement) |
| **Value Objects** | 6 (Money, Email, Phone, Concept, MovementType, Role) |
| **Use Cases** | 7 |
| **Repositorios** | 2 |

---

## 🌐 URLs y Recursos

- **Aplicación en Producción**: https://sistema-gestion-ingresos.vercel.app/
- **Documentación API**: https://sistema-gestion-ingresos.vercel.app/api-docs
- **Repositorio GitHub**: (tu repositorio)

---

## 🎓 Nivel de Complejidad

| Aspecto | Nivel | Justificación |
|---------|-------|---------------|
| **Arquitectura** | 🔴 Alta | Clean Architecture + DDD requiere disciplina |
| **Frontend** | 🟡 Media | React con hooks y state management |
| **Backend** | 🔴 Alta | Múltiples capas, abstracciones, patrones |
| **Testing** | 🟡 Media | Tests unitarios completos |
| **DevOps** | 🟢 Baja | CI/CD automatizado con GitHub Actions |
| **Base de Datos** | 🟢 Baja | PostgreSQL con Prisma (abstracción simple) |

---

## 🎯 ¿Por Qué Este Proyecto es Especial?

### 1. **Arquitectura Empresarial**
No es un CRUD simple. Es una aplicación con arquitectura de nivel empresarial:
- Separación clara de responsabilidades
- Independencia de frameworks
- Fácil de testear y mantener

### 2. **Domain-Driven Design**
El dominio está modelado con:
- Entidades ricas con comportamiento
- Value Objects para validación
- Domain Events para comunicación

### 3. **Escalabilidad**
Preparado para crecer:
- Agregar nuevos casos de uso es simple
- Cambiar la base de datos es factible
- Migrar a microservicios es posible

### 4. **Calidad de Código**
- TypeScript en todo el stack
- 198 tests automatizados
- Linting y formateo automático
- CI/CD con GitHub Actions

---

## 🚀 Próximos Pasos (Roadmap)

### Funcionalidades Futuras
- [ ] Categorías personalizadas para movimientos
- [ ] Metas de ahorro
- [ ] Notificaciones push
- [ ] Exportar reportes a PDF/Excel
- [ ] Multi-tenancy (múltiples organizaciones)
- [ ] API GraphQL
- [ ] Aplicación móvil (React Native)

### Mejoras Técnicas
- [ ] Event Sourcing
- [ ] CQRS completo con bases separadas
- [ ] Microservicios
- [ ] Cache con Redis
- [ ] Búsqueda con Elasticsearch
- [ ] Mensajería con RabbitMQ

---

## 📚 Continúa Leyendo

➡️ **Siguiente documento**: [02 - Arquitectura del Sistema](./02-ARQUITECTURA.md)

---

**Última actualización:** Febrero 2026
