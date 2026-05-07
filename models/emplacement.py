from odoo import models, fields, api

class SigiEmplacement(models.Model):
    _name = 'sigi.emplacement'
    _description = 'Emplacement des Stock'
    _inherit=['mail.thread','mail.activity.mixin']


    code = fields.Char(string="Code",tracking=True)
    name= fields.Char(string="Nom du Magasin", required=True,tracking=True)

    def action_valider(self):
        pass