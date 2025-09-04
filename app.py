import os
import asyncio
import smtplib

from email.message import EmailMessage
from email import message_from_bytes

from aiosmtpd.controller import Controller
from aiosmtpd.smtp import AuthResult, LoginPassword


class ForwardingHandler:
    def __init__(self, relay_host, relay_port, relay_user, relay_pass, relay_from):
        self.relay_host = relay_host
        self.relay_port = relay_port
        self.relay_user = relay_user
        self.relay_pass = relay_pass
        self.relay_from = relay_from

    async def handle_DATA(self, server, session, envelope):
        print("== Got new e-mail ==")
        print("From:", envelope.mail_from)
        print("To:", envelope.rcpt_tos)

        
        incoming_msg = message_from_bytes(envelope.content)

        if "From" in incoming_msg:
            incoming_msg.replace_header("From", self.relay_from)
        else:
            incoming_msg["From"] = self.relay_from

        to_header = ", ".join(envelope.rcpt_tos)
        if "To" in incoming_msg:
            incoming_msg.replace_header("To", to_header)
        else:
            incoming_msg["To"] = to_header

        try:
            with smtplib.SMTP(self.relay_host, self.relay_port) as smtp:
                smtp.starttls()
                smtp.login(self.relay_user, self.relay_pass)
                smtp.send_message(incoming_msg)
            print("E-mail successfully forwarded")

        except Exception as e:
            print("Error forwarding e-mail:", e)

        return "250 Message accepted for delivery"


def authenticator_func(server, session, envelope, mechanism, auth_data):
    valid_user = os.getenv("LOCAL_USER")
    valid_pass = os.getenv("LOCAL_PASS")

    if mechanism == "LOGIN":
        login, password = auth_data
        if login == valid_user and password == valid_pass:
            return AuthResult(success=True)

    elif mechanism == "PLAIN":
        login, password = auth_data
        login = login.decode() if isinstance(login, bytes) else login
        password = password.decode() if isinstance(password, bytes) else password
        
        if login == valid_user and password == valid_pass:
            return AuthResult(success=True)

    return AuthResult(success=False)


def main():
    relay_host = os.getenv("RELAY_HOST")
    relay_port = int(os.getenv("RELAY_PORT", "587"))
    relay_user = os.getenv("RELAY_USER")
    relay_pass = os.getenv("RELAY_PASS")
    relay_from = os.getenv("RELAY_USER")

    listen_host = "0.0.0.0"
    listen_port = 25

    handler = ForwardingHandler(relay_host, relay_port, relay_user, relay_pass, relay_from)
    controller = Controller(
        handler,
        hostname=listen_host,
        port=listen_port,
        authenticator=authenticator_func,
        auth_require_tls=False,
    )
    controller.start()

    print(f"SMTP relay is running...")

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        controller.stop()


if __name__ == "__main__":
    main()
