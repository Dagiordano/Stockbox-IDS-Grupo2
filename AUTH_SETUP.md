# Instrucciones de configuración del sistema de autenticación

## Sistema de Autenticación Implementado

Se ha implementado un sistema completo de autenticación con django-allauth que incluye:
- Login manual con email y contraseña
- Login con Google OAuth
- Registro de nuevas cuentas
- Gestión de perfil y contraseña
- Menú de usuario con dropdown en todas las páginas

## Pasos para completar la configuración:

### 1. Instalar dependencias
```bash
pip install django-allauth
```

### 2. Aplicar migraciones
```bash
python manage.py migrate
```

### 3. Crear superusuario (opcional)
```bash
python manage.py createsuperuser
```

### 4. Configurar Google OAuth (Opcional pero recomendado)

#### 4.1. Crear proyecto en Google Cloud Console
1. Ve a https://console.cloud.google.com/
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la API de Google+ (Google+ API)

#### 4.2. Crear credenciales OAuth 2.0
1. Ve a "APIs & Services" > "Credentials"
2. Clic en "Create Credentials" > "OAuth client ID"
3. Tipo de aplicación: "Web application"
4. Nombre: "StockBox"
5. URIs de redireccionamiento autorizados:
   - http://127.0.0.1:8000/accounts/google/login/callback/
   - http://localhost:8000/accounts/google/login/callback/

#### 4.3. Configurar en Django Admin
1. Inicia el servidor: `python manage.py runserver`
2. Ve a http://127.0.0.1:8000/admin/
3. Ve a "Sites" y asegúrate de que existe un site con:
   - Domain name: 127.0.0.1:8000
   - Display name: StockBox
4. Ve a "Social applications" y crea uno nuevo:
   - Provider: Google
   - Name: Google OAuth
   - Client id: [Tu Client ID de Google]
   - Secret key: [Tu Client Secret de Google]
   - Sites: Selecciona el site que creaste

### 5. Actualizar settings.py con tus credenciales
En `stockbox/settings.py`, actualiza:
```python
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': 'TU_CLIENT_ID_AQUI',
            'secret': 'TU_CLIENT_SECRET_AQUI',
            'key': ''
        }
    }
}
```

## Características implementadas:

### Templates creados:
- ✅ `/inventario/templates/account/login.html` - Página de inicio de sesión
- ✅ `/inventario/templates/account/signup.html` - Página de registro
- ✅ `/inventario/templates/account/logout.html` - Confirmación de cierre de sesión

### Protección de vistas:
- ✅ Todas las vistas están protegidas con `@login_required`
- ✅ La página home redirige automáticamente al login si no está autenticado

### Navegación:
- ✅ Menú de usuario en el navbar con dropdown
- ✅ Avatar circular con inicial del email
- ✅ Opciones: Dashboard, Configuración, Cambiar Contraseña, Cerrar Sesión
- ✅ Responsive (en móviles solo muestra el avatar)

### URLs disponibles:
- `/accounts/login/` - Iniciar sesión
- `/accounts/signup/` - Crear cuenta
- `/accounts/logout/` - Cerrar sesión
- `/accounts/password/change/` - Cambiar contraseña
- `/accounts/password/reset/` - Recuperar contraseña
- `/accounts/email/` - Gestionar emails
- `/accounts/google/login/` - Login con Google

## Uso del sistema:

### Primera vez:
1. Ejecuta: `python manage.py runserver`
2. Ve a: http://127.0.0.1:8000/
3. Serás redirigido automáticamente al login
4. Crea una cuenta o inicia sesión

### Login con Google (después de configurar OAuth):
1. Haz clic en "Continuar con Google"
2. Autoriza la aplicación
3. Serás redirigido al dashboard automáticamente

## Notas importantes:
- El email backend está configurado para consola (desarrollo)
- En producción, configura un email backend real
- La verificación de email está en modo 'optional'
- Cambia `ACCOUNT_EMAIL_VERIFICATION = 'mandatory'` en producción
