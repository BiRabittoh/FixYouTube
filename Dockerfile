FROM tecktron/python-waitress:slim

WORKDIR /app

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./fxyoutube ./fxyoutube
ENV APP_MODULE=fxyoutube:app
