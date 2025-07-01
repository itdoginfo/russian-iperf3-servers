FROM python:3.13.5-alpine3.22

COPY . .

RUN pip install -r requirements.txt --no-cache-dir && apk add --no-cache iperf3

CMD ["python", "check-iperf3.py"]