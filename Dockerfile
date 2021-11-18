FROM python:3.8-bullseye
WORKDIR /app
RUN pip install -U pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .