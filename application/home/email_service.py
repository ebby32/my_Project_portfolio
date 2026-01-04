import smtplib

from flask import current_app



def send_contact_email(name, telephone, email, message):
    smtp = smtplib.SMTP("smtp.gmail.com", port=587)
    smtp.starttls()

    smtp.login(
        user= current_app.config["EMAIL_USERNAME"],
        password=current_app.config["EMAIL_PASSWORD"]
    )

    smtp.sendmail(
        from_addr=current_app.config["EMAIL_USERNAME"],
        to_addrs=current_app.config["EMAIL_USERNAME"],
        msg= (
            "Subject: Project Portfolio, contact me\n\n"
            f"Name:{name}\n"
            f"Email:{email}\n"
            f"Telephone Number:{telephone}\n"
            f"Message:{message}"
        )
    )

    smtp.quit()