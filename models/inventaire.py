from odoo import models, fields, api, _

class SigiInventaire(models.Model):
    _name = 'sigi.inventaire'
    _description = "Session d'Inventaire"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Référence Inventaire", readonly=True, default=lambda self: _('Nouveau'))
    date_inventaire = fields.Date(string="Date de l'Inventaire", default=fields.Date.today, required=True)
    responsable_id = fields.Many2one('res.users', string="Responsable", default=lambda self: self.env.user)
    
    # Statistiques calculées pour le tableau de bord
    total_biens = fields.Integer(string="Total des Biens", compute="_compute_stats")
    total_en_service = fields.Integer(string="En Service", compute="_compute_stats")
    total_amortis = fields.Integer(string="Amortis", compute="_compute_stats")
    total_sortis = fields.Integer(string="Sortis", compute="_compute_stats")

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirm', 'En cours'),
        ('done', 'Clôturé')
    ], string="État", default='draft', tracking=True)

    @api.depends('date_inventaire')
    def _compute_stats(self):
        for record in self:
            # On compte directement dans la table des biens codifiés (affectation_ligne)
            Ligne = self.env['sigi.affectation_ligne']
            record.total_biens = Ligne.search_count([])
            record.total_en_service = Ligne.search_count([('etat_amortissement', '=', 'en_cours')])
            record.total_amortis = Ligne.search_count([('etat_amortissement', '=', 'amorti')])
            record.total_sortis = Ligne.search_count([('etat_amortissement', '=', 'termine')])

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('Nouveau')) == _('Nouveau'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sigi.inventaire') or _('Nouveau')
        return super(SigiInventaire, self).create(vals_list)

    def action_cloturer(self):
        self.write({'state': 'done'})