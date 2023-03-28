FROM python:3.10.4-slim-buster
COPY . /bot
WORKDIR /bot
RUN pip3 install telethon python-decouple aioredis[hiredis]
CMD ["python3", "bot.py"]
