from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

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
    VALIDATE_CERTS = False,
    TEMPLATE_FOLDER='static/templates',
)


html = """
<p>Hi this test mail, thanks for using Fastapi-mail</p> 
"""

async def simple_send(email: str):
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=[email],  # List of recipients, as many as you can pass 
        body=html,
        subtype="html",
        template_body={"URL": "https://lfl2l.fr"},
        )
    fm = FastMail(conf)
    await fm.send_message(message,template_name="reset.html")
    return {"message": "Mail sent"}