FROM python:3.5

# install python packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

