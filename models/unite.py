from odoo import models, fields, api

class SigiUnite(models.Model):
    _name = 'sigi.unite'
    _description = 'Les unités et leurs symboles'
    _inherit=['mail.thread','mail.activity.mixin']


    name = fields.Char(string="Nom Unité",required=True)
    symbole = fields.Char(string="Symbole de l'unité")

    def action_valider(self):
        pass