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

RUN ln -s /code/uptemplates/auth        /usr/local/lib/python3.6/site-packages/haplugin/auth/templates
RUN ln -s /code/uptemplates/flashmsg    /usr/local/lib/python3.6/site-packages/Hatak_Flashmsg-0.1.2-py3.5.egg/haplugin/flashmsg/templates
RUN ln -s /code/uptemplates/formskit    /usr/local/lib/python3.6/site-packages/Hatak_Formskit-0.2.3.7-py3.5.egg/haplugin/formskit/templates
RUN ln -s /code/uptemplates/hatak       /usr/local/lib/python3.6/site-packages/hatak-0.2.7.11-py3.5.egg/bael/hatak/templates
RUN ln -s /code/uptemplates/statics     /usr/local/lib/python3.6/site-packages/Hatak_Statics-0.2.5-py3.5.egg/haplugin/statics/templates

EXPOSE 8000

CMD ["backend", "dev"]
