FROM python:3.7.2-slim-stretch

RUN apt-get update \
 && apt-get install -y git

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY controller.py /

ENTRYPOINT ["ryu-manager", "controller.py"]
