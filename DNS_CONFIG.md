# 📋 Guía de Configuración DNS

Esta guía te ayudará a configurar los DNS para que tu dominio apunte correctamente a tu servidor VPS.

## 🌐 Información del Servidor

- **IP del Servidor (IPv4)**: `72.60.51.74`
- **IP del Servidor (IPv6)**: `2a02:4780:66:d8a6::1`
- **Dominio configurado**: `pablogaray.com` y `www.pablogaray.com`

## ⚙️ Configuración de DNS

### Paso 1: Accede al Panel de DNS de tu Registrador de Dominio

Necesitas acceder al panel de control de donde compraste tu dominio (p. ej., Hostinger, Namecheap, GoDaddy, etc.).

### Paso 2: Configura los Registros DNS

Debes crear o modificar los siguientes registros DNS en tu panel:

#### Opción A: Usando IPv4 (Recomendado - más compatible)

| Tipo | Nombre/Host | Valor/Contenido | TTL |
|------|-------------|-----------------|-----|
| **A** | `@` o vacío | `72.60.51.74` | 3600 (o Auto) |
| **A** | `www` | `72.60.51.74` | 3600 (o Auto) |

#### Opción B: Usando IPv6 (Opcional, para soporte dual-stack)

Si tu proveedor de DNS soporta IPv6, puedes agregar también:

| Tipo | Nombre/Host | Valor/Contenido | TTL |
|------|-------------|-----------------|-----|
| **AAAA** | `@` o vacío | `2a02:4780:66:d8a6::1` | 3600 (o Auto) |
| **AAAA** | `www` | `2a02:4780:66:d8a6::1` | 3600 (o Auto) |

### Paso 3: Explicación de los Registros

- **Registro A (@ o vacío)**: Este es el registro para el dominio raíz (`pablogaray.com`)
  - El símbolo `@` o dejarlo vacío significa "el dominio raíz"
  - Apunta a la IP `72.60.51.74`

- **Registro A (www)**: Este es el registro para el subdominio `www` (`www.pablogaray.com`)
  - Apunta a la misma IP `72.60.51.74`

### Paso 4: TTL (Time To Live)

- **3600 segundos** (1 hora): Recomendado para cambios iniciales (se propagan más rápido)
- **Auto o por defecto**: Una vez configurado y funcionando, puedes dejarlo en el valor por defecto de tu proveedor

## 🔍 Verificación de la Configuración

Después de configurar los DNS, espera entre **15 minutos y 48 horas** para que los cambios se propaguen (generalmente toma 1-2 horas).

### Verificar desde la Terminal

```bash
# Verificar el registro A del dominio principal
dig pablogaray.com A +short

# Verificar el registro A de www
dig www.pablogaray.com A +short

# Verificar ambos desde tu navegador
# Abre: http://pablogaray.com y http://www.pablogaray.com
```

### Verificar en Línea

Puedes usar estas herramientas online:
- https://dnschecker.org/
- https://www.whatsmydns.net/
- https://mxtoolbox.com/

## ⚠️ Problemas Comunes

### 1. "El sitio no carga después de configurar DNS"

**Solución**:
- Verifica que los contenedores Docker estén corriendo:
  ```bash
  docker-compose ps
  ```
- Verifica que nginx esté escuchando en el puerto 80:
  ```bash
  sudo netstat -tlnp | grep :80
  # O
  sudo ss -tlnp | grep :80
  ```
- Asegúrate de que el firewall permita tráfico en los puertos 80 y 443:
  ```bash
  sudo ufw allow 80/tcp
  sudo ufw allow 443/tcp
  ```

### 2. "Solo funciona www o solo funciona el dominio sin www"

**Solución**:
- Verifica que ambos registros A estén configurados
- Revisa el archivo `nginx.conf` - ambos dominios deben estar en `server_name`

### 3. "Los DNS no se han propagado aún"

**Solución**:
- Espera más tiempo (puede tardar hasta 48 horas, pero generalmente es 1-2 horas)
- Limpia la caché DNS de tu navegador
- En Windows: `ipconfig /flushdns`
- En Linux/Mac: `sudo systemd-resolve --flush-caches` o `sudo dscacheutil -flushcache`

### 4. "El sitio carga pero sin SSL (HTTPS)"

**Solución**:
- Necesitas configurar certificados SSL. Revisa el README.md, sección "SSL Certificate Setup"
- Una vez configurados los DNS, puedes obtener certificados con Let's Encrypt:
  ```bash
  sudo certbot certonly --standalone -d pablogaray.com -d www.pablogaray.com
  ```

## 🔐 Configuración SSL (Opcional pero Recomendado)

Una vez que los DNS estén configurados y funcionando:

1. **Instala Certbot**:
   ```bash
   sudo apt-get update
   sudo apt-get install certbot python3-certbot-nginx
   ```

2. **Detén temporalmente nginx**:
   ```bash
   docker-compose stop nginx
   ```

3. **Obtén el certificado**:
   ```bash
   sudo certbot certonly --standalone -d pablogaray.com -d www.pablogaray.com
   ```

4. **Copia los certificados al directorio ssl/**:
   ```bash
   mkdir -p ssl
   sudo cp /etc/letsencrypt/live/pablogaray.com/fullchain.pem ssl/
   sudo cp /etc/letsencrypt/live/pablogaray.com/privkey.pem ssl/
   sudo chown -R $USER:$USER ssl/
   ```

5. **Actualiza nginx.conf** para incluir configuración SSL (ver README.md)

6. **Reinicia los contenedores**:
   ```bash
   docker-compose up -d
   ```

## 📝 Notas Importantes

- ⏰ **Propagación DNS**: Los cambios pueden tardar hasta 48 horas, pero generalmente es 1-2 horas
- 🔒 **Puerto 80**: Debe estar abierto en el firewall para que HTTP funcione
- 🔒 **Puerto 443**: Debe estar abierto en el firewall para que HTTPS funcione
- ✅ **Verificación**: Usa las herramientas online mencionadas para verificar que los DNS se han propagado globalmente

## 🆘 ¿Necesitas Ayuda?

Si después de seguir estos pasos aún tienes problemas:

1. Verifica los logs de nginx: `docker-compose logs nginx`
2. Verifica los logs del backend: `docker-compose logs backend`
3. Verifica el estado de los contenedores: `docker-compose ps`
4. Verifica que los puertos estén abiertos: `sudo ufw status`

---

**Última actualización**: Después de corregir los puertos en docker-compose.yml