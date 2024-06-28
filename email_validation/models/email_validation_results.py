from odoo import _, api, fields, models


class EmailValidationResults(models.Model):
    _name = "email.validation.results"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Email Validation Results"
    _order = "create_date desc"

    email = fields.Char(string="Email", required=True, readonly=True, tracking=True)
    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True, tracking=True)
    format = fields.Char(string="Format", readonly=True, tracking=True)
    domain = fields.Char(string="Domain", readonly=True, tracking=True)
    alias = fields.Char(string="Alias", readonly=True, tracking=True)
    disposable = fields.Char(string="Disposable", readonly=True, tracking=True)
    dns = fields.Char(string="DNS", readonly=True, tracking=True)
    whitelist = fields.Char(string="Whitelist", readonly=True, tracking=True)
    note = fields.Text(string="Error Notes", readonly=True, tracking=True)
