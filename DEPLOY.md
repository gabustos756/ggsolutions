# Guía de Despliegue en VPS Producción — GG Solutions (`ggsolutions.com.ar`)

Esta guía detalla los pasos exactos para desplegar la aplicación **GG Solutions** en tu servidor VPS Linux (Ubuntu / Debian), configurando **Gunicorn**, **Systemd**, **Nginx** como Proxy Inverso y **Certbot** para certificado SSL gratuito HTTPS.

---

## 1. Requisitos Previos en el VPS

- Servidor VPS con Ubuntu 20.04 / 22.04 LTS o Debian.
- Acceso SSH con permisos de root o sudo.
- Dominio `ggsolutions.com.ar` y `www.ggsolutions.com.ar` apuntando la **IP A-Record** hacia la IP pública del VPS.

---

## 2. Instalación de Paquetes en el VPS

Conéctate por SSH e instala Python 3, venv, Nginx y Git:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip nginx git certbot python3-certbot-nginx
```

---

## 3. Clonado del Repositorio y Entorno Virtual

1. Clona el proyecto en `/var/www/ggsolutions`:

```bash
sudo mkdir -p /var/www/ggsolutions
sudo chown -R $USER:$USER /var/www/ggsolutions
cd /var/www/ggsolutions
git clone <URL_DE_TU_REPOSITY_GIT> .
```

2. Crea y activa el entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 4. Configuración de Variables de Entorno

Crea el archivo `.env` de producción en `/var/www/ggsolutions/.env`:

```bash
cat << 'EOF' > /var/www/ggsolutions/.env
SECRET_KEY=cambiar_por_clave_super_segura_aleatoria_2026
ADMIN_EMAIL=contacto@ggsolutions.com.ar
ADMIN_PASSWORD=TuPasswordSuperSeguro2026
PORT=5050
EOF
```

---

## 5. Configuración del Servicio Systemd (`ggsolutions.service`)

Crea la unidad de servicio para que Gunicorn corra de forma persistente y se reinicie automáticamente si falla o se reinicia el servidor:

```bash
sudo nano /etc/systemd/system/ggsolutions.service
```

Pega el siguiente contenido:

```ini
[Unit]
Description=Gunicorn instance for GG Solutions Landing & Admin
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/ggsolutions
EnvironmentFile=/var/www/ggsolutions/.env
ExecStart=/var/www/ggsolutions/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5050 app:app

[Install]
WantedBy=multi-user.target
```

Asigna permisos correctos e inicia el servicio:

```bash
sudo chown -R www-data:www-data /var/www/ggsolutions
sudo systemctl daemon-reload
sudo systemctl start ggsolutions
sudo systemctl enable ggsolutions
sudo systemctl status ggsolutions
```

---

## 6. Configuración de Nginx Proxy Inverso

Crea el archivo de configuración para Nginx:

```bash
sudo nano /etc/nginx/sites-available/ggsolutions
```

Pega el siguiente bloque:

```nginx
server {
    server_name ggsolutions.com.ar www.ggsolutions.com.ar;

    client_max_body_size 20M;

    location / {
        proxy_pass http://127.0.0.1:5050;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/ggsolutions/static/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }
}
```

Habilita el sitio y reinicia Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/ggsolutions /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 7. Instalación del Certificado SSL HTTPS Gratis (Certbot)

Ejecuta Certbot para obtener e instalar automáticamente el certificado SSL en Nginx:

```bash
sudo certbot --nginx -d ggsolutions.com.ar -d www.ggsolutions.com.ar
```

Responde las preguntas interactivas y selecciona **Redirigir todo el tráfico a HTTPS**.

---

## 8. Verificación Final

1. Visita en tu navegador: `https://ggsolutions.com.ar`
2. Prueba el formulario de contacto enviando un mensaje con teléfono y característica.
3. Ingresa al panel de administración en: `https://ggsolutions.com.ar/admin`
4. Inicia sesión con `ADMIN_EMAIL` y `ADMIN_PASSWORD` configurados en tu `.env`.

¡Tu plataforma estará 100% en producción con seguridad de nivel empresarial!
