FROM tecktron/python-waitress:slim

WORKDIR /app

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./fixyoutube ./fixyoutube
COPY .en[v] .
ENV APP_MODULE=fixyoutube:app
