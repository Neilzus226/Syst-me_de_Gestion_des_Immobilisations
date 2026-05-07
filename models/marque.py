
from odoo import models, fields, api

class SigiMarque(models.Model):
    _name = 'sigi.marque'
    _description = 'Marque des équipements'
    _inherit=['mail.thread','mail.activity.mixin']


    code = fields.Char(string="Code",tracking=True)
    name = fields.Char(string="Nom de la marque", required=True,tracking=True)
    description = fields.Text(string="Description",tracking=True)

    def action_valider(self):
        pass
