from python:3.10.19-alpine3.22

workdir /app

copy requirements.txt .

run pip install -r requirements.txt

copy . .

cmd ["python", "main.py"]