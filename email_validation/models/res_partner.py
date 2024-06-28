from odoo import api, fields, models
from .email_validation_abstract import check_email_format


class ResPartnerInherit(models.Model):
    _name = "res.partner"
    _inherit = ["res.partner", "email.validation.abstract"]

    @api.onchange("email")
    def _onchange_email(self):
        check_email_format(self.email)

    def action_email_identity_verification(self):
        uid = self.user_ids[0].id if self.user_ids else False
        super().action_email_identity_verification(self.email, uid)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            record.email_validation(record.email) if record.email else False
        return records

    def write(self, vals):
        result = super().write(vals)
        if "email" in vals:
            for record in self:
                record.email_validation(record.email)
        return result
