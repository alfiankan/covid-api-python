FROM python:3.9.9-slim

WORKDIR /app

COPY . .

RUN apt update -y && apt install make -y && apt install gunicorn -y && apt install cron -y

RUN touch /app/logs/syncjoblog.log

COPY sync-cron /etc/cron.d/sync-cron

RUN chmod 0644 /etc/cron.d/sync-cron

RUN crontab /etc/cron.d/sync-cron



RUN make install

ENV PORT=3000

CMD ["make", "start"]
