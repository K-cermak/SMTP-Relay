FROM python:3.14-slim

WORKDIR /app
COPY app.py /app

RUN pip install aiosmtpd

ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
