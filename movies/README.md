## Endpoints

### 1. Obtener Películas al Azar

**Ruta:** `GET /movies/random`  
**Descripción:** Retorna una lista de películas aleatorias, según el límite especificado.  
**Parámetros de Consulta (Query Params):**
- `limit`: Número de películas a retornar. Debe ser un número entero positivo.

**Ejemplo de Solicitud:**
```bash
GET /movies/random?limit=5
```

**Respuestas:**
- `200 OK`: Retorna un arreglo de películas aleatorias.
- `400 Bad Request`: Si `limit` no es un número válido o es menor o igual a cero.
- `500 Internal Server Error`: Si ocurre un error en el servidor.

---

### 2. Obtener Película por ID

**Ruta:** `GET /movies`  
**Descripción:** Retorna los detalles de una película específica según su ID.  
**Parámetros de Consulta (Query Params):**
- `id` (requerido): ID de la película a buscar.

**Ejemplo de Solicitud:**
```bash
GET /movies?id=12345
```

**Respuestas:**
- `200 OK`: Retorna la película correspondiente al ID proporcionado.
- `400 Bad Request`: Si el parámetro `id` no se proporciona.
- `500 Internal Server Error`: Si ocurre un error en el servidor.

---

### 3. Buscar Películas por Título

**Ruta:** `POST /movies/title`  
**Descripción:** Busca películas cuyo título coincide con el texto proporcionado.  
**Cuerpo de la Solicitud (Request Body):**
- `title` (requerido): Título o parte del título de la película.

**Ejemplo de Solicitud:**
```bash
POST /movies/title
Content-Type: application/json

{
  "title": "Inception"
}
```

**Respuestas:**
- `200 OK`: Retorna un arreglo de películas que coinciden con el título proporcionado.
- `400 Bad Request`: Si el parámetro `title` no se proporciona en el cuerpo de la solicitud.
- `500 Internal Server Error`: Si ocurre un error en el servidor.

---

### 4. Buscar Películas por Director

**Ruta:** `POST /movies/director`  
**Descripción:** Busca películas cuyo director coincide con el nombre proporcionado.  
**Cuerpo de la Solicitud (Request Body):**
- `director` (requerido): Nombre del director o parte del nombre.

**Ejemplo de Solicitud:**
```bash
POST /movies/director
Content-Type: application/json

{
  "director": "Christopher Nolan"
}
```

**Respuestas:**
- `200 OK`: Retorna un arreglo de películas dirigidas por el director especificado.
- `400 Bad Request`: Si el parámetro `director` no se proporciona en el cuerpo de la solicitud.
- `500 Internal Server Error`: Si ocurre un error en el servidor.

## Instalación individual

1. Clona este repositorio.
2. Instala las dependencias necesarias ejecutando:
   ```bash
   npm install
   ```
3. Inicia el servidor:
   ```bash
   npm start
   ```

### Requisitos para su ejecución
1. Node.js
2. npm
3. redis