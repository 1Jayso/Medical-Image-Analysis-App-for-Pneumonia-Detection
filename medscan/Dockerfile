FROM python:3.5.7-slim

RUN apt-get update && apt-get install libgl1 libglib2.0-0 libsm6 libxrender1 libxext6 -y
RUN apt-get install -y apt-utils build-essential gcc


WORKDIR /opt

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip \
    pip install -r requirements.txt

COPY . .

Expose 5000

CMD [ "python3",  "manage.py", "runserver", "--host=0.0.0.0"]