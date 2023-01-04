FROM python:3.8.10

WORKDIR /app

COPY ./app /app
COPY ./requirements /app

RUN pip install --no-cache-dir -r /app/requirements

ENV TZ="Asia/Taipei"

CMD ["python", "server.py"]

EXPOSE 10091