FROM python:3

RUN mkdir -p /opt/src/app
WORKDIR /opt/src/app

COPY . .

RUN pip install -r ./requirements.txt

# project root folder
ENV PYTHONPATH="/opt/src/app"

ENTRYPOINT ["python", "./main.py"]