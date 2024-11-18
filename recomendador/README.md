## Requisitos

- Python 3.x
- pip
- virtualenv

## Instalación

1. Crea un entorno virtual (opcional):
    ```bash
    virtualenv venv
    source venv/bin/activate
    ```

2. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Ejecución

Para ejecutar la aplicación:

```bash
gunicorn -b 127.0.0.1:5000 src.main:app --reload
```

La API se ejecuta en **localhost**, puerto **5000**.