FROM continuumio/miniconda3

RUN mkdir -m777 /root/app && cd /root/app
WORKDIR /root/app

ADD docker-entrypoint.sh ./
ADD requirements.txt ./
ADD main.py ./

RUN chmod 777 ./docker-entrypoint.sh
RUN chmod 777 ./main.py
RUN conda create -n env python=3.10.12
RUN pip install -r requirements.txt

CMD ["./docker-entrypoint.sh"]