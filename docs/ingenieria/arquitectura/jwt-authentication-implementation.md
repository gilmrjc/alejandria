---
id: ARC-022
type: Implementation Specification
rating: 9
rating-phase: document-editing
related:
  - target: ARC-005
    relationship_type: implements
    reason: Implementa la autenticación JWT definida en la especificación de API REST (básico para MVP, completo con refresh tokens post-MVP)
  - target: TRD-021
    relationship_type: references
    reason: Referencia el TRD de Hito 2 para requisitos de autenticación de API
  - target: EPC-002
    relationship_type: implements
    reason: EPC-002 implementa T-020 (Users y Auth) con JWT básico para MVP según este documento
  - target: ARC-008
    relationship_type: references
    reason: Define la estrategia de storage usando localStorage (línea 392) para el token JWT
---

# JWT Authentication Implementation (MVP) — Alejandria

Este documento define la implementación de autenticación JWT básica para MVP Bootstrapped.

## Índice

1. [Visión General](#1-visión-general)
2. [Implementación de Access Tokens](#2-implementación-de-access-tokens)
3. [Manejo de Expiración](#3-manejo-de-expiración)
4. [Token Storage](#4-token-storage)
5. [Security Best Practices](#5-security-best-practices)

---

## 1. Visión General

### Propósito

Especificar la implementación de autenticación JWT básica para MVP Bootstrapped, incluyendo access tokens, manejo de expiración y storage en cliente.

### Referencia

Para la especificación de API REST, ver [api-specification.md](api-specification.md).

---

## 2. Implementación de Access Tokens

### Configuración

- Algoritmo: HS256
- Expiración: 8 horas (configurable)
- Claims estándar: iss, sub, exp, iat, jti

### Claims Personalizados

```python
{
    "user_id": "uuid",
    "email": "user@example.com",
    "organization_id": "uuid"
}
```

**NOTA**: El claim `role` no se incluye en MVP. El sistema de roles (RBAC) no se implementará en MVP. Referencia: api-specification.md (línea 299).

### Implementación

```python
def create_access_token(user_id, email, organization_id):
    payload = {
        "user_id": str(user_id),
        "email": email,
        "organization_id": str(organization_id),
        "exp": datetime.utcnow() + timedelta(hours=8),
        "iat": datetime.utcnow(),
        "jti": str(uuid.uuid4())  # JWT ID para revocación
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
```

---

## 3. Manejo de Expiración

### Expiración de Access Token

- Tokens tienen expiración de 8 horas
- Cuando un token expira, el usuario debe volver a autenticarse
- Cliente detecta expiración (401 Unauthorized)
- Usuario redirigido a login
- Nuevos tokens emitidos tras autenticación exitosa

---

## 4. Token Storage

### Estrategia Seleccionada

La estrategia seleccionada es **localStorage**.

**Referencia**: frontend-specification.md (línea 392) muestra `const token = localStorage.getItem('access_token')`. El interceptor de axios usa localStorage para almacenar y recuperar el token de autenticación.

#### Justificación de la Estrategia

Se seleccionó localStorage sobre httpOnly cookies y sessionStorage por las siguientes razones:

- **Simplicidad de implementación**: localStorage es más simple de implementar que httpOnly cookies (no requiere configuración de cookies en servidor)
- **Compatibilidad con arquitectura existente**: El frontend-specification.md ya usa localStorage en el interceptor de axios (línea 392)
- **Adecuado para MVP**: Para MVP bootstrapped, localStorage es suficiente. httpOnly cookies ofrecen mejor seguridad (protección contra XSS) pero requieren más configuración
- **Trade-offs evaluados**:
  - **localStorage**: Vulnerable a XSS pero simple de implementar
  - **httpOnly cookies**: Protección contra XSS pero requiere configuración de CORS y cookies en servidor
  - **sessionStorage**: Similar a localStorage pero se limpia al cerrar el navegador (no adecuado para persistencia de sesión)

### Implementación en Frontend

```javascript
// Almacenar token
localStorage.setItem('access_token', token);

// Recuperar token
const token = localStorage.getItem('access_token');

// Eliminar token (logout)
localStorage.removeItem('access_token');
```

---

## 5. Security Best Practices

### Secret Management

- SECRET_KEY almacenado en variables de entorno
- Rotación periódica de SECRET_KEY
- Different SECRET_KEY para desarrollo vs producción

### Algorithm Selection

- HS256 tanto para desarrollo como para producción
- No se usan key pairs (simplifica implementación)

**Justificación**: Usar HS256 con SECRET_KEY tanto para desarrollo como para producción simplifica la implementación y reduce la complejidad operacional, siendo adecuado para MVP bootstrapped. No se usan key pairs (RS256) porque:

- **Simplicidad operacional**: No requiere gestión de key pairs públicas/privadas
- **Menor complejidad de implementación**: Un solo SECRET_KEY para firma y verificación
- **Adecuado para MVP**: MVP bootstrapped no requiere la seguridad adicional de key pairs asimétricas
- **Trade-off aceptable**: Si bien RS256 ofrece mejor seguridad (key pública no expone clave privada), el overhead operacional no se justifica en MVP

**Referencia**: Gap "Algorithm selection para producción" (línea 209-216)

### Token Validation

- Validar firma en cada request
- Validar expiración (exp claim)
- Validar not before (nbf claim si aplica)
- Validar issuer (iss claim si aplica)

### Implementación de Validación

```python
def validate_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError()
    except jwt.InvalidTokenError:
        raise InvalidTokenError()
```

### Revocación de Tokens (Post-MVP)

#### NO APLICA para MVP Bootstrapped

En MVP bootstrapped no se implementa mecanismo de revocación de tokens en el servidor. La estrategia de revocación es:

- **Logout en cliente**: Al hacer logout, el cliente elimina el token de localStorage
- **Expiración natural**: Los tokens expiran después de 8 horas
- **Sin tokens de larga duración**: No hay refresh tokens que requieran invalidación

**Justificación**: Sin refresh tokens, no hay necesidad de invalidar tokens de larga duración. Logout en cliente es suficiente para MVP. Revocación solo sería necesaria si se implementan refresh tokens o tokens de larga duración en fases post-MVP.

**Referencia**: api-specification.md (líneas 294-299) especifica autenticación JWT básica para MVP sin refresh tokens.

---
