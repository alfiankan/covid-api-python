FROM python:3.9.9-slim

WORKDIR /app

COPY . .



RUN apt update -y && apt install make -y && apt install gunicorn -y && apt install locales -y

RUN export LC_ALL=C && dpkg-reconfigure locales


RUN make install

ENV PORT=3000

CMD ["make", "start"]
