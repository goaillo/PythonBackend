FROM python:3.10.12-slim-bullseye

# Create app directory
WORKDIR /app

RUN apt-get update \
    && apt-get install --no-install-recommends -y gcc default-libmysqlclient-dev pkg-config python3-pip \
    && apt-get install --no-install-recommends -y nginx \
    && apt-get install --no-install-recommends -y python3-dev \
    && apt-get install --no-install-recommends -y build-essential \
    && apt-get install --no-install-recommends -y uwsgi-plugin-python3 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV DATABASE_USER=""
ENV DATABASE_PASSWD=""
ENV DATABASE_HOST=""
ENV DATABASE_PORT=""
ENV DATABASE_NAME=""
ENV FLASK_SECRET_KEY=""

EXPOSE 80
COPY nginx.conf /etc/nginx
RUN mkdir -p files
RUN mkdir -p tmp
RUN chown -R www-data .
RUN chmod +x ./start.sh

CMD ["./start.sh"]
