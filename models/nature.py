from odoo import models, fields, api

class SigiNature(models.Model):
    _name = 'sigi.nature'
    _description = 'Nature des aquisitions'
    _inherit=['mail.thread','mail.activity.mixin']


    code = fields.Char(string="Code",tracking=True)
    name= fields.Char(string="Nature", required=True,tracking=True)

    def action_valider(self):
        pass
    