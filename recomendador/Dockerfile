FROM python:3.9-slim

WORKDIR /usr/src/app/recomendador

COPY . .

RUN pip install virtualenv

RUN virtualenv venv

RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

COPY .env .env

EXPOSE 5000

ENV NAME .env

CMD ["venv/bin/gunicorn", "-b", "0.0.0.0:5000", "src.main:app", "--reload"]