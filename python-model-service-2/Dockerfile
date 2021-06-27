# FROM python:stretch
FROM python:3.8

COPY . /python-model-service-2

WORKDIR /python-model-service-2

RUN pip3 install -r requirements.txt 

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "5"]