FROM alpine/git as builder

WORKDIR /app

RUN git clone https://github.com/lurbaby/protectOne-crm.git .

FROM python:3.11-slim-bullseye

COPY --from=builder /app/tg_bot /app/tg_bot

WORKDIR /app/tg_bot

RUN pip install aiogram

ENTRYPOINT ["python", "main.py"]
