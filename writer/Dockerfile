FROM  python:3.8-slim-buster

WORKDIR /app

COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY writer.py writer.py

CMD [ "python3", "writer.py" ]