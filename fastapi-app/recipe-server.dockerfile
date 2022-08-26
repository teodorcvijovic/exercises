FROM python:3

RUN mkdir -p /opt/src/app
WORKDIR /opt/src/app

COPY . .

RUN pip install -r ./requirements.txt

ENV PYTHONPATH="/opt/src/app"

EXPOSE 8080

ENTRYPOINT ["python", "./main.py"]