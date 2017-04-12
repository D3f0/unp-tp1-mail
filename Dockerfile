FROM python:2.7

RUN pip install twisted
RUN useradd -ms /bin/bash user

ADD code /code
RUN chown -R user:user /code
USER user
WORKDIR /code

CMD ["python", "main.py"]

