FROM python:3.10-alpine

WORKDIR /app

COPY . /app/

RUN pip3 install -r ./adapter/requirements.txt

CMD ["python3", "./adapter/adapter.py"]