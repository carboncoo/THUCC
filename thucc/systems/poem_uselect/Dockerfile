FROM huggingface/transformers-pytorch-gpu
LABEL maintainer="thumt<thumt17@gmail.com>"
# 清华源
ENV PIP_SOURCE "https://mirrors.aliyun.com/pypi/simple"

WORKDIR /app

RUN pip3 install -i ${PIP_SOURCE} fastapi uvicorn
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
COPY ./requirements.txt ./
RUN pip3 install -i ${PIP_SOURCE} -r requirements.txt
COPY ./src .
EXPOSE 80

CMD ["uvicorn", "wsgi:app", "--host", "0.0.0.0", "--port", "80", "--workers", "4", "--reload"]