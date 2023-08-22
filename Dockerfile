FROM python:3.10.12-slim-bullseye

# Create app directory
WORKDIR /app

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config python3-pip \
    && apt-get install -y nginx \
    && apt-get install -y python3-dev \
    && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV DATABASE_USER=""
ENV DATABASE_PASSWD=""
ENV DATABASE_HOST=""
ENV DATABASE_PORT=""
ENV DATABASE_NAME=""

EXPOSE 80
COPY nginx.conf /etc/nginx
RUN chmod +x ./start.sh
CMD ["./start.sh"]
# CMD ["sleep","infinity"]
# CMD [ "flask", "run","--host","0.0.0.0","--port","5055"]