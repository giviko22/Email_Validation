from odoo import http
from odoo.addons.mail.controllers.mail import MailController


class EmailVerification(http.Controller):

    @http.route(['/email_identity_verification'], type='http', auth='public', website=True)
    def email_identity_verification(self, res_id, token):
        comparison, record, redirect = MailController._check_token_and_record_or_redirect('email.identity.verification',
                                                                                          int(res_id), token)
        try:
            if record.user_id.id == http.request.uid:
                if record.verification_result != "verified":
                    record.write({"verification_result": "verified"})
                    related_document = http.request.env[record.res_model].search([('id', '=', record.res_id)])
                    related_document.message_post(body="Email Was Successfully Verified!") if related_document else False
                return http.request.render('email_validation.verification_success')
            else:
                return http.request.render('email_validation.verification_failed')
        except:
            return MailController._redirect_to_messaging()
