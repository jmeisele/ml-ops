# FROM python:stretch
FROM python:3.8

COPY . /python-model-service-1

WORKDIR /python-model-service-1

RUN pip3 install -r requirements.txt 

EXPOSE 8000 

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "5" ]