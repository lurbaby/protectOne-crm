# Використовуйте python образ як базовий
FROM python:3.11-slim-bullseye

# Встановіть git та інші залежності, які можуть знадобитися
RUN apt-get update && \
    apt-get install -y --no-install-recommends git

RUN pip install aiogram

# Клонуйте ваш репозиторій в робочу директорію
RUN git clone https://github.com/lurbaby/protectOne-crm.git /

# Перемкніться в директорію де знаходиться ваш проект
WORKDIR /

# Визначте команду для запуску вашого Python додатку
ENTRYPOINT ["python", "main.py"]


