from odoo import models, fields, api

class SigiCategorie(models.Model):
    _name = 'sigi.categorie'
    _description = 'Catégorie d’Immobilisation'
    _inherit=['mail.thread','mail.activity.mixin']



    name = fields.Char(string="Nom de la catégorie", required=True,tracking=True)
    code = fields.Char(string="Code",tracking=True)
    methode = fields.Selection([
        ('lineaire', 'Linéaire'),
        ('degressine', 'Dégressif'),
    ], string="Methode",tracking=True)


    def action_valider(self):
        pass