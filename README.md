# SMTP Relay

By Karel Cermak | [Karlosoft](https://karlosoft.com).

## Description
- SMTP Relay is a simple SMTP server that forwards emails to another SMTP server.
- It is ideal for older devices (e.g. copiers) that support only basic SMTP authentication and not modern TLS.


## Installation
- Get a Linux distribution (Ubuntu or Debian is recommended).
- Install Docker: https://docs.docker.com/engine/install/
- Clone this repository and copy the example environment file:

```
git clone https://github.com/K-cermak/SMTP-Relay.git

cd SMTP-Relay

cp .env.example .env
```

<br>

- Edit the .env file, for example with nano or vim:
```
SMTP_PORT=1025              # PORT ON WHICH THE RELAY WILL BE AVAILABLE

LOCAL_USER=user             # LOCAL USER FOR SMTP AUTHENTICATION
LOCAL_PASS=password         # LOCAL PASSWORD FOR SMTP AUTHENTICATION

RELAY_HOST=smtp.gmail.com   # REMOTE SMTP HOST
RELAY_PORT=587              # REMOTE SMTP PORT
RELAY_USER=you@example.com  # REMOTE SMTP USER
RELAY_PASS=password         # REMOTE SMTP PASSWORD
```


- Start the container:
```
docker compose up -d
```

- If you get a "permission denied" error when accessing the Docker socket, you may need to adjust the permissions: https://stackoverflow.com/questions/48957195/how-to-fix-docker-permission-denied
