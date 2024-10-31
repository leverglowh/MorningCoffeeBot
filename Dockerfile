FROM python:3.9-slim
WORKDIR /app

# Add a non-root user
RUN adduser --disabled-password --gecos "" mcb

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot ./bot

USER mcb

CMD ["python", "bot/main.py"]
