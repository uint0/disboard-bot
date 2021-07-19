FROM python:3.9-slim

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt \
 && rm /tmp/requirements.txt

WORKDIR /srv
COPY disboard/ /srv/
COPY config /etc/disboard

ENV DISBOARD_CONF_DIR=/etc/disboard

ENTRYPOINT ["uvicorn", "webapp:app"]