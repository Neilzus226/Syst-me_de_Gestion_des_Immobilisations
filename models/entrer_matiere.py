from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SigiEntrer_Matiere(models.Model):
    _name = 'sigi.entrer_matiere'
    _description = 'Entrer les matières'
    _inherit=['mail.thread','mail.activity.mixin']
    
    name = fields.Char(string="Reference Entrée", readonly=True, default=lambda self: _('Nouveau'))
    date_entree = fields.Date(string="Date d'entrée",tracking=True)
    nature = fields.Many2one('sigi.nature', string="Nature",tracking=True)
    emplacement = fields.Many2one('sigi.emplacement', string="Magasin",tracking=True)
    fournisseur= fields.Many2one('sigi.fournisseur', string="Fournisseur",tracking=True)
    immo_count=fields.Integer(string="Total Immo",compute="get_immo_count")

    state = fields.Selection([
        ('brouillon', 'Brouillon'),
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
    ], string="État", default='brouillon', tracking=True)


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('Nouveau')) == _('Nouveau'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sigi.entrer_matiere') or _('Nouveau')
        return super(SigiEntrer_Matiere, self).create(vals_list)

    @api.depends('ligne_ids.quantite')
    def get_immo_count(self):
        for record in self:
            total = sum(line.quantite for line in record.ligne_ids)
            record.immo_count = total

    def list_immo(self):
        self.ensure_one()
        return {
            'name': 'Liste des Immo',
            'type': 'ir.actions.act_window',
            'res_model': 'sigi.stock_matiere', 
            'view_mode': 'list,form',
            'domain': [('matiere_id', 'in', self.ligne_ids.mapped('matiere_id').ids)],
            'target': 'current',
        }

    def action_confirm(self):
        for record in self:
            if not record.ligne_ids:
                from odoo.exceptions import UserError
                raise UserError("Vous ne pouvez pas confirmer une entrée sans lignes de détails.")

            for ligne in record.ligne_ids:
                for i in range(ligne.quantite):
                    numero = self.env['ir.sequence'].next_by_code('sigi.stock.matiere.sequence') or 'Nouveau'
                    self.env['sigi.stock_matiere'].create({
                        'name': numero,
                        'matiere_id': ligne.matiere_id.id,
                        'marque_id': ligne.marque_id.id,
                        'modele_id': ligne.modele_id.id,
                        'cout': ligne.cout,
                        'status': 'disponible',
                    })
            
            # On change l'état du document
            record.state = 'confirme'
        return True

    def action_cancel(self):
        """Fonction pour annuler l'entrée"""
        for record in self:
            record.state = 'annule'
        return True

    ligne_ids = fields.One2many('sigi.entrer_matiere_ligne', 'entrer_id', string="Détails des Entreés de Matières")

class EntrerMatiereLigne(models.Model):
    _name = 'sigi.entrer_matiere_ligne'
    _description = 'Ligne de détail acquisition'
    _inherit=['mail.thread','mail.activity.mixin']
   

    entrer_id = fields.Many2one('sigi.entrer_matiere', string="Parent", ondelete='cascade')
    matiere_id = fields.Many2one('sigi.matiere',string="Matière")
    date_achat = fields.Date(string="Date d'aquisition")
    marque_id = fields.Many2one('sigi.marque', string="Marque",tracking=True)
    modele_id = fields.Many2one('sigi.modele', string="Modèle")
    unite_id = fields.Many2one('sigi.unite', string="Unité")
    categorie_id = fields.Many2one('sigi.categorie', string="Catégorie")
    quantite = fields.Integer(string="Quantité", default=1)
    cout = fields.Float(string="Valeur  unitaire")
