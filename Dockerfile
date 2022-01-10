FROM python:3.9.9-slim

WORKDIR /app

COPY . .


## set timezone to asia jakarta
RUN apt update -y && apt install make -y && apt install gunicorn -y && apt install locales -y

RUN export LC_ALL=C

RUN ln -sf /usr/share/zoneinfo/Asia/Jakarta /etc/localtime
RUN echo "Asia/Jakarta" > /etc/timezone

RUN dpkg-reconfigure --frontend noninteractive tzdata


RUN make install

ENV PORT=3000

CMD ["make", "start"]
