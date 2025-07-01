FROM python:3.13.5-alpine3.22

COPY . .

RUN pip install -r requirements.txt && apk add iperf3

CMD ["python", "check-iperf3.py"]