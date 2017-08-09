FROM python:3.5

MAINTAINER Yujiro Takeda <siro.cola@gmail.com>

# install python packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

Add .ssh/id_rsa /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa
