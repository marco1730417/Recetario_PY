# email_utils.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from smtplib import SMTPResponseException

load_dotenv()  # Asegúrate de cargar variables de entorno

def sendMail(to, subject, message):
    msg = MIMEMultipart('alternative')
    msg['From'] = os.getenv('SMTP_USER')
    msg['To'] = to  
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'html'))

    try:
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = int(os.getenv('SMTP_PORT'))  # convertir a entero

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls()  # importante para seguridad
        server.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASSWORD'))
        server.sendmail(os.getenv('SMTP_USER'), to, msg.as_string())
        server.quit()

        print(f"Correo enviado a {to}")

    except SMTPResponseException as e:
        print(f"SMTP Error: {e.smtp_code} - {e.smtp_error.decode()}")
    except Exception as e:
        print(f"Error al enviar el correo: {str(e)}")
