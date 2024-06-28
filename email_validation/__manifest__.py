{
    "name": "Email Validation",
    "version": "17.0.0.0",
    "sequence": 10,
    "author": "Givi",
    "license": "LGPL-3",
    "category": "Validation",
    "website": "",
    "summary": "",
    "description": """
    """,
    "depends": ["contacts"],
    "data": [
        "data/email_templates.xml",
        "security/ir.model.access.csv",
        "views/email_validation_results.xml",
        "views/email_identity_verification.xml",
        "views/res_partner.xml",
    ],
    "application": True,
    "installable": True,
    "auto_install": False,
}
