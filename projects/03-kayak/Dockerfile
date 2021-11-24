FROM python:3.7

WORKDIR /pez-jedha/kayak

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8888

CMD jupyter lab --ip=* --port=8888 --allow-root --no-browser 
