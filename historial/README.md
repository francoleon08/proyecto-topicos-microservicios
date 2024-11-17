# History Movies Service

Este servicio proporciona una API REST para la gestion de un historial de películas.
Esta construido con Spring Boot 3 y RabbitMQ.

## Endpoints

### 1. Agregar Película al Historial

**Ruta:** `POST /history`  
**Descripción:** Agrega una película al historial.  
**Cuerpo de la Solicitud (Request Body):** Debe ser un JSON válido que represente una película. Se considera una película válida si tiene los siguientes campos:
- `title`: Título de la película.
- `imdb`: dato que indetifica unívocamente a la película en la base de datos.

**Ejemplo de Solicitud:**
```bash
POST /history
Content-Type: application/json

{
    "title": "Inception",
    "year": 2010,
    "genre": "Sci-Fi"
    ...
}
```
Observación: El JSON puede contener cualquier cantidad de campos, pero debe tener al menos los campos `title` e `imdb`.


**Respuestas:**
- `200 OK`: Si la película se agregó correctamente al historial.
- `400 Bad Request`: Si el JSON proporcionado no es válido.
- `500 Internal Server Error`: Si ocurre un error en el servidor.

### 2. Obtener Última Película Guardada

**Ruta:** `GET /history/lastSaved`  
**Descripción:** Retorna la última película guardada en el historial.

**Ejemplo de Solicitud:**
```bash
GET /history/lastSaved
```

**Respuestas:**
- `200 OK`: Retorna la última película guardada.
- `400 Bad Request`: Si el historial está vacío.
- `500 Internal Server Error`: Si ocurre un error en el servidor.

### 3. Obtener Todo el Historial

**Ruta:** `GET /history/allHistory`  
**Descripción:** Retorna todas las películas en el historial.

**Ejemplo de Solicitud:**
```bash
GET /history/allHistory
```

**Respuestas:**
- `200 OK`: Retorna un arreglo con todas las películas en el historial.
- `400 Bad Request`: Si el historial está vacío.
- `500 Internal Server Error`: Si ocurre un error en el servidor.

## Especificaciones Técnicas

### Tecnologías Utilizadas
- Java 21
- Spring Boot 3.x
- Maven 3.8.x o superior
- RabbitMQ
- Docker (opcional, para contenedores)

### Variables de Entorno
- SPRING_RABBITMQ_HOST
- SPRING_RABBITMQ_PORT
- SPRING_RABBITMQ_USERNAME
- SPRING_RABBITMQ_PASSWORD

### RabbitMQ
La cola de mensajes se llama `movies`. Almacenará las películas que se agreguen al historial.
