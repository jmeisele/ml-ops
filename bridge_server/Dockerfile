FROM python:3.8

COPY . ./app

RUN pip3 install -r requirements.txt

WORKDIR /app

CMD ["python3", "app.py"]