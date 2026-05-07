from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SigiSortie(models.Model):
    _name = 'sigi.sortie'
    _description = 'Sortie de Matière'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Réf Sortie", readonly=True, default=lambda self: _('Nouveau'))
    affectation_ligne_id = fields.Many2one('sigi.affectation_ligne', string="Réf Matière ",required=True,domain=[('etat_amortissement', 'in', ['en_cours', 'amorti'])])
    matiere_id = fields.Many2one('sigi.matiere', related='affectation_ligne_id.matiere_id', string="Matière", readonly=True,store=True)
    date_sortie = fields.Date(string="Date de sortie", default=fields.Date.today,tracking=True)
    motif_sortie = fields.Char( string="Motif de sortie", required=True,tracking=True)
    
    montant_sortie = fields.Float(string="Montant de sortie")
    vnc_cloture = fields.Float(string="VNC à la sortie", compute="_compute_vnc_cloture")
    lieu = fields.Char(string="Lieu",tracking=True)

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirme', 'Confirmé')
    ], string="État", default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('Nouveau')) == _('Nouveau'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sigi.sortie') or _('Nouveau')
        return super(SigiSortie, self).create(vals_list)

    @api.depends('matiere_id', 'date_sortie')
    
    def _compute_vnc_cloture(self):
        for record in self:
            vnc = 0.0
            if record.matiere_id and record.date_sortie:
            # On cherche la ligne d'amortissement de l'année de sortie
                ligne = self.env['sigi.tableau_amortissement'].search([
                    ('matiere_id', '=', record.matiere_id.id),
                    ('annee', '=', record.date_sortie.year)
                ], limit=1)
            
                if ligne:
                    vnc = ligne.valeur_restante
                else:
                    vnc = 0.0
            record.vnc_cloture = vnc
    
    def valider_sortie(self):
        self.ensure_one()
        # 1. On clôture l'affectation (on met une date de fin)
        self.affectation_ligne_id.write({
            'date_fin': self.date_sortie,
            'etat_amortissement': 'termine'
        })

        self.write({'state': 'confirme'})
        
        
        return True