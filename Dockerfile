FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code/src/
RUN mkdir -p /project.egg-info

WORKDIR /code
RUN ln -s /project.egg-info /code/src/Konwentor.egg-info

COPY code/requrietments.txt .
RUN pip install -r requrietments.txt

COPY code .
RUN python setup.py develop

EXPOSE 8000

CMD ["backend", "dev"]
