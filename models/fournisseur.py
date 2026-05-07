from odoo import models, fields, api

class SigiFournisseur(models.Model):
    _name = 'sigi.fournisseur'
    _description = 'Les Fournisseurs des aquisitions'
    _inherit=['mail.thread','mail.activity.mixin']

    _rec_name = 'libele_long'

    libele_long= fields.Char(string="Libélé Long", required=True,tracking=True)
    libele_court= fields.Char(string="Libélé Court",required=True,tracking=True)
    contact= fields.Char(string="Contact",tracking=True)
    addresse= fields.Char(string="Adressse",tracking=True)
    
    def action_valider(self):
        pass
