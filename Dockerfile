FROM python:3.10

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

ENV TOKEN NONE

VOLUME [ "/app/database" ]

CMD ["python", "main.py"]