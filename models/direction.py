from odoo import models, fields, api

class SigiDirection(models.Model):
    _name = 'sigi.direction'
    _description = 'Direction des Affections'
    _inherit=['mail.thread','mail.activity.mixin']


    name= fields.Char(string="Nom", required=True,tracking=True)
    code = fields.Char(string="Code",tracking=True)

    def action_valider(self):
        pass
    
    