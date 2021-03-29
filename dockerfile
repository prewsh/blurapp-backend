FROM python:3.6-stretch

LABEL Author="Odafe Kevin"
LABEL E-mail="xsaysoft@gmail.com"

COPY . /blurapp
WORKDIR /blurapp
RUN pip install -r requirements.txt
CMD [ "python", "run.py" ]
