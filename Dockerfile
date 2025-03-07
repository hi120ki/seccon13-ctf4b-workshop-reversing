FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    binutils build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY ctf.py .
COPY lecture.py .

COPY templates templates

CMD ["python", "main.py"]
