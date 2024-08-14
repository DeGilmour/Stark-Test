
FROM python:3.10-slim

WORKDIR /stark


COPY requirements.txt .


RUN pip install -r requirements.txt


COPY . .


EXPOSE 8080


CMD ["python", "invoice.py"]
