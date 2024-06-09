FROM python:3.10

RUN apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y --no-install-recommends gcc && \
  pip install --no-cache-dir --upgrade pip 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN groupadd -g 7777 crypto-quants &&\
  useradd -m -d /home/crypto-quants crypto-quants -s /bin/false -u 7777 -g crypto-quants 

USER crypto-quants 

COPY --chown=crypto-quants:crypto-quants requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN mkdir /home/crypto-quants/app

WORKDIR /home/crypto-quants/app

COPY --chown=crypto-quants:crypto-quants . .

RUN chmod 554 /home/crypto-quants/app/deployment/*.sh

ENV PATH /home/crypto-quants/.local/bin:$PATH

ENTRYPOINT [ "./deployment/app.sh" ]
