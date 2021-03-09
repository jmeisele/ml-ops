FROM python:3.8

COPY ./requirements.txt requirements.txt 

RUN pip install -r requirements.txt 

COPY ./locustfile.py locustfile.py

EXPOSE 8089

# CMD ["locust", "-f", "locust/locustfile.py", "--host", "http://127.0.0.1:3000"]
CMD ["locust", "-f", "locustfile.py"]