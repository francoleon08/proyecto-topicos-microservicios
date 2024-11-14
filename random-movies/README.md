# Random Movies Service

Este servicio proporciona un endpoint para obtener películas aleatorias desde otro servicio de películas.

## Endpoints

### GET /randommovies

Obtiene una lista de películas aleatorias.

#### Parámetros de consulta

- `limit`: El número de películas a obtener.

#### Ejemplo de solicitud

```sh
curl "http://localhost:3000/randommovies?limit=5"
```