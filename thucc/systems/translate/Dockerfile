FROM python:3.8.5
LABEL maintainer="thumt<thumt17@gmail.com>"
# 清华源
ENV PIP_SOURCE "https://mirrors.aliyun.com/pypi/simple"

WORKDIR /app

RUN pip install -i ${PIP_SOURCE} flask gunicorn gevent

# COPY ./requirements.txt ./
# RUN pip install -i ${PIP_SOURCE} requirements.txt
COPY ./src .
EXPOSE 36789

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:36789", "--timeout", "0", "wsgi:app"]