import os
import ssl
import hmac
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

        if "To" not in incoming_msg:
            incoming_msg["To"] = ", ".join(envelope.rcpt_tos)

        try:
            await asyncio.to_thread(self.forward, incoming_msg, envelope.rcpt_tos)
            print("E-mail successfully forwarded")

        except Exception as e:
            print("Error forwarding e-mail:", e)
            return "451 4.3.0 Error forwarding e-mail, try again later"

        return "250 Message accepted for delivery"

    def forward(self, msg, rcpt_tos):
        with smtplib.SMTP(self.relay_host, self.relay_port, timeout=30) as smtp:
            smtp.starttls(context=ssl.create_default_context())
            smtp.login(self.relay_user, self.relay_pass)
            smtp.send_message(msg, from_addr=self.relay_from, to_addrs=rcpt_tos)


def to_bytes(value):
    return value.encode() if isinstance(value, str) else value


def authenticator_func(server, session, envelope, mechanism, auth_data):
    valid_user = os.getenv("LOCAL_USER")
    valid_pass = os.getenv("LOCAL_PASS")

    login = None
    if mechanism in ("LOGIN", "PLAIN") and isinstance(auth_data, LoginPassword):
        login = to_bytes(auth_data.login)
        password = to_bytes(auth_data.password)

        if valid_user and valid_pass:
            user_ok = hmac.compare_digest(login, valid_user.encode())
            pass_ok = hmac.compare_digest(password, valid_pass.encode())

            if user_ok and pass_ok:
                print("Authentication successful")
                return AuthResult(success=True)

    login_str = login.decode(errors="replace") if login is not None else None
    print(f"Authentication failed - login: {login_str}")
    return AuthResult(success=False, handled=False)


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
        auth_required=True,
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
