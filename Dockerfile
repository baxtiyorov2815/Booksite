FROM python:3-slim

ENV DJANGO_SETTINGS_MODEL=core.settings
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirments.txt .

RUN apt-get update && \
 apt-get install -y netcat-openbsd && \
 python3 -m pip install -r requirments.txt

COPY . .

EXPOSE 8000

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]


CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]