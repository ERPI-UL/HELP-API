from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

templates = Jinja2Templates(directory="static/templates")

conf = ConnectionConfig(
    MAIL_USERNAME="",
    MAIL_PASSWORD="",
    MAIL_FROM="noreply@univ-lorraine.fr",
    MAIL_PORT=25,
    MAIL_SERVER="smtp-int.univ-lorraine.fr",
    MAIL_FROM_NAME="Indico",
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=False,
    VALIDATE_CERTS=False,
    MAIL_STARTTLS=False,
    TEMPLATE_FOLDER='app/static/templates',
)


HTML = """
<p>Hi this test mail, thanks for using Fastapi-mail</p> 
"""


async def test_jinja(request: Request):
    """ Test jinja template rendering"""
    return templates.TemplateResponse('reset.html',
                                      {"request": request, "PRENOM": "Jean",
                                       "NOM": "VALJEAN", "URL": "https://indico.lf2l.fr/reset?token=123456789"})


async def simple_send(email: str):
    """ Send a simple email"""
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=[email],  # List of recipients, as many as you can pass
        template_body={"URL": "https://indico.lf2l.fr/reset?token=123456789"},
    )
    fast_mail = FastMail(conf)
    await fast_mail.send_message(message, template_name="reset.html")
    return {"message": "Mail sent"}


async def send_reset_link(email: str, token: str, firstname: str, lastname: str):
    """ Send a reset link to a user via email"""
    message = MessageSchema(
        subject="Indico - Mot de passe",
        recipients=[email],  # List of recipients, as many as you can pass
        template_body={"URL": f"https://indico.lf2l.fr/reset?token={token}",
                       "PRENOM": firstname, "NOM": lastname},
    )
    fast_mail = FastMail(conf)
    await fast_mail.send_message(message, template_name="reset.html")
    return {"message": "Mail sent"}


async def send_invite_link(email: str, username: str,
                           token: str, firstname: str,
                           lastname: str, sender_firstname: str,
                           sender_lastname: str, role: str):
    """ Send an invitation link to a user via email"""
    message = MessageSchema(
        subject="Indico - Invitation",
        recipients=[email],  # List of recipients, as many as you can pass
        template_body={"URL": f"https://indico.lf2l.fr/invite?token={token}", "USERNAME": username,
                       "PRENOM": firstname, "NOM": lastname,
                       "SENDER": f"{sender_firstname} {sender_lastname}", "ROLE": role})
    fast_mail = FastMail(conf)
    await fast_mail.send_message(message, template_name="invite.html")
    return {"message": "Mail sent"}
