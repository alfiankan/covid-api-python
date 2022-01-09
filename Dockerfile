FROM python:3.9.9-slim

WORKDIR /app

COPY . .

RUN apt update -y && apt install make -y && apt install gunicorn -y

RUN make install

ENV PORT=3000

CMD ["make", "start"]
