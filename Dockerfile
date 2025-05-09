FROM python:3.10-slim

ENV RAY_SERVE_HOST=0.0.0.0

RUN apt-get update && apt-get install -y git && apt-get clean
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY serve_app.py .

CMD ["python", "serve_app.py"]

EXPOSE 8000

