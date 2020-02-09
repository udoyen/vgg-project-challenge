FROM iamjohnnym/bionic-python

LABEL maintainer="datameshprojects@gmai.com"

USER root

WORKDIR /app

ADD . /app

RUN apt update
RUN apt install sqlite3 -y
RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80

CMD ["python", "main.py"]