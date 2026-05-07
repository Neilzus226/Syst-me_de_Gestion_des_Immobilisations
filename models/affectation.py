from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class SigiAffectation(models.Model):
    _name = 'sigi.affectation'
    _description = 'Gestion des Affectations'
    _inherit=['mail.thread','mail.activity.mixin']

    

    name = fields.Char(string="Référence Dossier", readonly=True, copy=False, default='/')
    line_ids = fields.One2many('sigi.affectation_ligne', 'affectation_id', string="Lignes d'affectation")
    
    state = fields.Selection([
        ('brouillon', 'Brouillon'),
        ('valide', 'En cours'),
        ('termine', 'Terminé')
    ], default='brouillon', string="État")

    def action_valider(self):
        """ Bouton pour confirmer l'affectation """
        for rec in self:
            if not rec.line_ids:
                raise ValidationError("Ajoutez au moins une unité avant de valider.")
            
            for ligne in rec.line_ids:
                if ligne.unite_id.status != 'disponible':
                    raise ValidationError(f"L'unité {ligne.unite_id.name} n'est plus disponible !")
                
                ligne.unite_id.status = 'affecte'
            
            rec.state = 'valide'

    def action_annuler(self):
        """ Annule l'affectation et libère les unités """
        for rec in self:
            for ligne in rec.line_ids:
                # On remet chaque unité en état disponible
                ligne.unite_id.status = 'disponible'
            
            # On repasse le document en brouillon
            rec.state = 'brouillon'

