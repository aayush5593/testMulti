FROM python:3.12-slim

WORKDIR /loggerService

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "logger.py"]
