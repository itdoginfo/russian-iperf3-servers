FROM python:3.13.5-alpine3.22

RUN pip install pyyaml && apk add iperf3

COPY . .

CMD ["python", "check-iperf3.py"]