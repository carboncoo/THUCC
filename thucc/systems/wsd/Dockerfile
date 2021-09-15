FROM python:3.8.5
LABEL maintainer="thumt<thumt17@gmail.com>"
# 清华源
ENV PIP_SOURCE "https://mirrors.aliyun.com/pypi/simple"

WORKDIR /app

RUN pip3 install -i ${PIP_SOURCE} fastapi uvicorn omegaconf numpy scipy gensim==3.8.1

# COPY ./requirements.txt ./
# RUN pip install -i ${PIP_SOURCE} requirements.txt
COPY ./src .
EXPOSE 80

CMD ["uvicorn", "wsgi:app", "--host", "0.0.0.0", "--port", "80", "--workers", "4", "--reload"]