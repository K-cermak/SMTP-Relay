FROM python:3.13-slim

WORKDIR /app
COPY app.py /app

RUN pip install aiosmtpd

ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
