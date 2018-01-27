FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code/src/
RUN mkdir -p ../../Konwentor.egg-info

WORKDIR /code
RUN ln -s ../../Konwentor.egg-info /code/src/Konwentor.egg-info

COPY pkgs/* /usr/local/lib/python3.6/site-packages/

COPY code/requrietments.txt .
RUN pip install -r requrietments.txt

COPY code/ .
RUN python setup.py develop

EXPOSE 8000

CMD uwsgi --ini-paste data/frontend.ini
