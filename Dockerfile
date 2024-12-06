FROM python:3.12.4

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./config /code/config

COPY ./static /code/static

COPY ./static/templates /code/static/templates

COPY ./static/uploads /code/static/uploads

COPY ./src /code/src


CMD ["fastapi", "run", "src/app.py"]