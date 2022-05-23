import smtplib
import ssl
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME="",
    MAIL_PASSWORD="",
    MAIL_FROM = "noreply@univ-lorraine.fr",
    MAIL_PORT = 25,
    MAIL_SERVER = "smtp-int.univ-lorraine.fr",
    MAIL_FROM_NAME="Indico",
    MAIL_TLS = False,
    MAIL_SSL = False,
    USE_CREDENTIALS = False,
    VALIDATE_CERTS = False
)


html = """
<p>Hi this test mail, thanks for using Fastapi-mail</p> 
"""

async def simple_send(email: str):
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=[email],  # List of recipients, as many as you can pass 
        body=html,
        subtype="html"
        )
    fm = FastMail(conf)
    await fm.send_message(message)
    return {"message": "Mail sent"}


# class Mail:
#     def __init__(self):
#         self.port:int = 25
#         self.smtp_server_domain_name:str = "smtp-int.univ-lorraine.fr"
#         self.sender_mail:str = "noreply@univ-lorraine.fr"

#     def send(self, emails:list[str], subject:str, content:str):
#         ssl_context = ssl.create_default_context()
#         service = smtplib.SMTP_SSL(
#             self.smtp_server_domain_name, self.port, context=ssl_context)
#         service.login(self.sender_mail, self.password)

#         for email in emails:
#             result = service.sendmail(
#                 self.sender_mail, email, f"Subject: {subject}\n{content}")

#         service.quit()


# if __name__ == '__main__':
#     mails:list[str] = input("Enter emails: ").split()
#     subject:str = input("Enter subject: ")
#     content:str = input("Enter content: ")

#     mail = Mail()
#     mail.send(mails, subject, content)
