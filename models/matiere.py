from odoo import models, fields, api

class SigiMatiere(models.Model):
    _name = 'sigi.matiere'
    _description = 'les Matieres'
    _inherit=['mail.thread','mail.activity.mixin']

    
    code = fields.Char(string="Code",tracking=True)
    name= fields.Char(string="Non ", required=True,tracking=True)
    duree = fields.Integer(string="Durée de Vie",tracking=True)

    affectation_ligne_ids = fields.One2many(
        'sigi.affectation_ligne', 
        'matiere_id', 
        string="Lignes d'affectation"
    )
     
    def action_valider(self):
        pass