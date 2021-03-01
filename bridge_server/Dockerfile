FROM python:3.8

COPY . ./app

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 8002

CMD ["python3", "app.py"]