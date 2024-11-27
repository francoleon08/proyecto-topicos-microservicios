FROM python:3.9-slim

WORKDIR /usr/src/app/

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "src.main:app"]