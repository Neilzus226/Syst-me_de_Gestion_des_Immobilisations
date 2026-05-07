from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SigiMutation(models.Model):
    _name = 'sigi.mutation'
    _description = 'Mutation de Biens Codifiés'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Ref Mutation", readonly=True, default=lambda self: _('Nouveau'))
    
    # On lie la mutation à la ligne d'affectation (le bien codifié)
    affectation_ligne_id = fields.Many2one('sigi.affectation_ligne', string="Ref Matière", required=True,domain=[('etat_amortissement', 'in', ['en_cours', 'amorti'])])

    # Récupération automatique de la matière via la ligne d'affectation
    matiere_id = fields.Many2one('sigi.matiere', related='affectation_ligne_id.matiere_id', string="Matière", readonly=True)

    date_mutation = fields.Date(string="Date", default=fields.Date.today, required=True)

    # Direction actuelle (Départ)
    direction_depart_id = fields.Many2one('sigi.direction', string="Origine", compute="_compute_direction_depart", store=True)

    # Nouvelle Direction (Arrivée)
    direction_arrive_id = fields.Many2one('sigi.direction', string="Destination", required=True
    )

    motif = fields.Text(string="Motif")
    
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirme', 'Confirmé')
    ], string="État", default='draft', tracking=True)

    @api.depends('affectation_ligne_id')
    def _compute_direction_depart(self):
        for record in self:
            if record.affectation_ligne_id:
                # On récupère la direction actuelle depuis la ligne d'affectation
                record.direction_depart_id = record.affectation_ligne_id.direction_id
            else:
                record.direction_depart_id = False

    def action_confirmer(self):
        self.ensure_one()
        if self.direction_depart_id == self.direction_arrive_id:
            raise ValidationError("La direction de destination doit être différente de la direction d'origine !")
        
        # LOGIQUE DE MUTATION : 
        # On met à jour la direction sur la ligne d'affectation pour refléter le changement
        if self.affectation_ligne_id:
            self.affectation_ligne_id.write({
                'direction_id': self.direction_arrive_id.id
            })
        
        self.write({'state': 'confirme'})
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
    
            if vals.get('name', _('Nouveau')) == _('Nouveau'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sigi.mutation') or _('Nouveau')
        
        # On passe la liste entière au super
        return super(SigiMutation, self).create(vals_list)