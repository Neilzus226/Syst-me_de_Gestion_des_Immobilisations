from odoo import models, fields, api

class SigiStockMatiere(models.Model):
    _name = 'sigi.stock_matiere'
    _description = 'Registre des Unités Individuelles'
    _order = 'name desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Numero", required=True, copy=False, readonly=True, default='Nouveau')

    matiere_id = fields.Many2one('sigi.matiere', string="Matière", required=True, readonly=True)
    marque_id = fields.Many2one('sigi.marque', string="Marque", readonly=True)
    modele_id = fields.Many2one('sigi.modele', string="Modèle", readonly=True)
    cout = fields.Float(string="Prix", default=0.0)
    
    # Le cycle de vie de l'objet
    status = fields.Selection([
        ('disponible', 'Disponible'),
        ('affecte', 'En service'),
        ('maintenance', 'En Réparation'),
        ('hors_service', 'Mis au rebut')
    ], string="Statut", default='disponible', tracking=True)

