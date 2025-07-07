# API de Versículos Bíblicos

Una API REST para consultar versículos bíblicos con caché local y estadísticas de uso.

## Características

- Consulta versículos bíblicos por referencia
- Caché local en PostgreSQL
- Estadísticas de versículos más consultados
- Desplegado con Docker

## Instalación Rápida

1. **Clona el repositorio**
```bash
git clone https://github.com/valentindc/bibleapi_req
cd bible-verse-api
```

2. **Inicia los servicios**
```bash
docker-compose up --build
```

3. **¡Listo!** La API está disponible en `http://localhost:8000`

## Endpoints

### Obtener versículo
```http
GET /verse/{referencia}
```
Ejemplo: `GET /verse/Juan%203:16`

### Top 3 versículos más consultados
```http
GET /top3
```

### Estado de la API
```http
GET /health
```

## Ejemplos de Uso

```bash
# Consultar un versículo
curl http://localhost:8000/verse/Juan%203:16

# Ver estadísticas
curl http://localhost:8000/top3
```

## Configuración

Crea un archivo `.env` para personalizar la configuración:

```env
DATABASE_URL=postgresql://postgres:tu_password@localhost:5432/bible_verses
POSTGRES_PASSWORD=tu_password
```

## Gestión de Datos

Los datos se guardan automáticamente en un volumen de Docker. Para limpiar la base de datos:

```bash
docker-compose down -v
docker-compose up --build
```

## Tecnologías

- **FastAPI** - Framework web
- **PostgreSQL** - Base de datos
- **SQLAlchemy** - ORM
- **Docker** - Contenedores
