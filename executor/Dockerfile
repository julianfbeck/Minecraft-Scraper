FROM  python:3.8-slim-buster

WORKDIR /app

COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY executor.py executor.py
COPY ping.py ping.py

CMD [ "python3", "-u","executor.py" ]