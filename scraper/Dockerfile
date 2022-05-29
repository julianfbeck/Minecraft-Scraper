FROM  python:3.8-slim-buster

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y masscan   libpcap-dev
WORKDIR /app

COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY scraper.py scraper.py

CMD [ "python3","-u", "scraper.py" ]