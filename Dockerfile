FROM python:3.9.9-slim

WORKDIR /app

COPY . .

RUN apt update && apt install make

RUN make install

CMD ["make", "run"]

EXPOSE 3000