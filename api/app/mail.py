from fastapi import Request
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="static/templates")

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
async def testJinja(request:Request):
    return templates.TemplateResponse('reset.html',{"request":request,"PRENOM":"Jean","NOM":"VALJEAN","URL": "https://indico.lf2l.fr/reset?token=123456789"})

async def simple_send(email: str):
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=[email],  # List of recipients, as many as you can pass 
        template_body={"URL": "https://indico.lf2l.fr/reset?token=123456789"},
        )
    fm = FastMail(conf)
    await fm.send_message(message,template_name="reset.html")
    return {"message": "Mail sent"}
async def sendResetLink(email: str,token:str,firstname:str,lastname:str):
    message = MessageSchema(
        subject="Indico - Mot de passe",
        recipients=[email],  # List of recipients, as many as you can pass 
        template_body={"URL": f"https://indico.lf2l.fr/reset?token={token}","PRENOM":firstname,"NOM":lastname},
        )
    fm = FastMail(conf)
    await fm.send_message(message,template_name="reset.html")
    return {"message": "Mail sent"}
async def sendInviteLink(email:str,username:str,token:str,firstname:str,lastname:str,senderFirstname:str,senderLastname:str,role:str):
    message = MessageSchema(
        subject="Indico - Invitation",
        recipients=[email],  # List of recipients, as many as you can pass 
        template_body={"URL": f"https://indico.lf2l.fr/invite?token={token}","USERNAME":username,"PRENOM":firstname,"NOM":lastname,"SENDER":f"{senderFirstname} {senderLastname}","ROLE":role},
        )
    fm = FastMail(conf)
    await fm.send_message(message,template_name="invite.html")
    return {"message": "Mail sent"}