from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import re
import requests


def check_email_format(email):
    """
    Check email format
    """
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if email and not (re.fullmatch(pattern, email)):
        raise ValidationError(_("Invalid Email Address, Please Type Correct One!"))


class EmailValidationAbstract(models.AbstractModel):
    _name = "email.validation.abstract"
    _description = "Email Validation Abstract"

    def email_validation(self, email):
        """
        Email Validation Using disify API
        """
        if email:
            url = f"https://disify.com/api/email/{email}"
            result_record = self.env["email.validation.results"].create({
                "name": email + " - Validation Results",
                "email": email,
            })
            try:
                response = requests.get(url, timeout=3)
                data = response.json()
                disposable = data.get("disposable", False)
                result_record.write({
                    "format": str(data.get("format", False)),
                    "domain": str(data.get("domain", False)),
                    "alias": str(data.get("alias", False)),
                    "disposable": str(disposable),
                    "dns": str(data.get("dns", False)),
                    "whitelist": str(data.get("whitelist", False)),
                })
                self.message_post(body=f"Email {email} -  is disposable") if disposable else False
            except Exception as e:
                self.message_post(
                    body="Something Went Wrong With Email Validation, Check Error Message In Email Validation Results")
                result_record.write({
                    "note": str(e),
                })

    def action_email_identity_verification(self, email, uid):
        """
        Check email identity verification by sending email to user to verify
        """
        if not (uid and isinstance(uid, int)):
            raise ValidationError(_("There is no user associated with this record!"))
        email_template = self.env.ref(
            'email_validation.email_identity_verification_email_template')
        verification_record = self.env["email.identity.verification"].create({
            "name": email + " - Identity Verification",
            "email": email,
            "user_id": uid,
            "res_model": self._name,
            "res_id": self.id,
        })
        verification_link = verification_record._notify_get_action_link('controller', controller='/email_identity_verification')
        email_template.body_html = f"""<p style="padding: 16px 0px 16px 0px;">
                    <a style="background-color:#875A7B; padding: 8px 16px 8px 16px; text-decoration: none; color: #fff; border-radius: 5px;"
                       t-attf-href="{verification_link}">
                        Verify Email
                    </a>
                     </p>"""
        email_template.email_to = email
        email_template.send_mail(verification_record.id, force_send=True)
        email_template.body_html = "<p></p>"
        email_template.email_to = False
        self.message_post(
            body=f"Verification Link Was Sent To - {email}")
