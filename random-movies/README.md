# Random Movies Service

Este servicio proporciona un endpoint para obtener películas aleatorias desde otro servicio de películas.

## Endpoints

### 1. Obtener Películas al Azar

**Ruta:** `GET /randommovies`  
**Descripción:** Retorna una lista de películas aleatorias, según el límite especificado.  
**Parámetros de Consulta (Query Params):**
- `limit`: Número de películas a retornar. Debe ser un número entero positivo.

**Ejemplo de Solicitud:**
```bash
GET randommovies?limit=5
```

**Respuestas:**
- `200 OK`: Retorna un arreglo de películas aleatorias.
- `400 Bad Request`: Si `limit` no es un número válido o es menor o igual a cero.
- `500 Internal Server Error`: Si ocurre un error en el servidor.

---