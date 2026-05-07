from odoo import models, fields, api

class SigiModele(models.Model):
    _name = 'sigi.modele'
    _description = 'Modele des équipements'
    _inherit=['mail.thread','mail.activity.mixin']


    code = fields.Char(string="Code",tracking=True)
    name = fields.Char(string="Nom du modèle", required=True,tracking=True)

    def action_valider(self):
        pass
