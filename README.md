# SMTP Relay

By Karel Cermak | [Karlosoft](https://karlosoft.com).

## Description
- SMTP Relay is a simple SMTP server that forwards emails to another SMTP server.
- Ideal application is to use it with old copy machines that only support SMTP authentication and does not support modern TLS etc.


## How to install
- Get some Linux distro (Ubuntu is recommended)
- Install docker: https://docs.docker.com/engine/install/

```
git clone https://github.com/K-cermak/SMTP-Relay.git

cd SMTP-Relay

cp .env.example .env
```

<br>

- Edit the .env file for example with nano or vim.
```
SMTP_PORT=1025 # PORT WHERE THE SMTP WILL BE AVAILABLE

LOCAL_USER=user             # LOCAL USER FOR SMTP AUTHENTICATION
LOCAL_PASS=password         # LOCAL PASSWORD FOR SMTP AUTHENTICATION

RELAY_HOST=smtp.gmail.com   # REMOTE SMTP HOST
RELAY_PORT=587              # REMOTE SMTP PORT
RELAY_USER=you@example.com  # REMOTE SMTP USER
RELAY_PASS=password         # REMOTE SMTP PASSWORD
```


- Start the Docker:
```
docker compose up -d
```

- If the Docker socket is not accessible, you may need to adjust the permissions: https://stackoverflow.com/questions/48957195/how-to-fix-docker-permission-denied
