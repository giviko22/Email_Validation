from odoo import _, api, fields, models


class EmailIdentityVerification(models.Model):
    _name = "email.identity.verification"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Email Identity Verification"
    _order = "create_date desc"

    email = fields.Char(string="Email", required=True, readonly=True, tracking=True)
    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True, tracking=True)
    verification_result = fields.Selection(selection=[
            ('unverified', 'Unverified'),
            ('verified', 'Verified'),
        ], default="unverified", string="Verification Result", readonly=True, tracking=True)
    user_id = fields.Many2one('res.users', "Email User", readonly=True, tracking=True)
    res_model = fields.Char(string="Model", required=True, readonly=True)
    res_id = fields.Many2oneReference(string='Related Document ID', index=True, model_field='res_model', readonly=True)
