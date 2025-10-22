FROM python:3.13.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY .env.docker .env.local

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
