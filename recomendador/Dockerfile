FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

COPY src /app/src

CMD ["gunicorn", "-b", "0.0.0.0:5000", "src.main:app", "--timeout", "0"]
