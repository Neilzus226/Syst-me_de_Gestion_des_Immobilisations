from odoo import models, fields, api, exceptions

class SigiTableauAmortissement(models.Model):
    _name = 'sigi.tableau_amortissement'
    _description = 'Lignes du tableau d\'amortissement'
    _order = 'annee asc'

    affectation_ligne_id = fields.Many2one('sigi.affectation_ligne', ondelete='cascade')
    matiere_id = fields.Many2one(related='affectation_ligne_id.matiere_id', string="Matière", store=True,)
    annee = fields.Integer(string="Exercice")
    base_amortissable = fields.Float(string="Base d'acquisition")
    montant = fields.Float(string="Annuité")
    cumul = fields.Float(string="Cumul Amortissement")
    valeur_restante = fields.Float(string="VNC")

    