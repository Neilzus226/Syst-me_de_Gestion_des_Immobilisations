from odoo import models, fields, api, exceptions

class SigiAffectationLigne(models.Model):
    _name = 'sigi.affectation_ligne'
    _description = 'Ligne d\'affectation détaillée'
    _inherit=['mail.thread','mail.activity.mixin']

    name = fields.Char(string="Référence", readonly=True, default='/',tracking=True)
    affectation_id = fields.Many2one('sigi.affectation', string="Affectation Parent", ondelete='cascade',tracking=True)
    unite_id = fields.Many2one('sigi.stock_matiere', string="Référence ", required=True,tracking=True)
    matiere_id = fields.Many2one('sigi.matiere', string="Matière", required=True)
    beneficiaire_id = fields.Many2one('res.users', string="Bénéficiaire",tracking=True)
    direction_id = fields.Many2one('sigi.direction', string="Direction",tracking=True)
    
    date_debut = fields.Date(string="Date de mise en service", default=fields.Date.today, required=True,tracking=True)
    date_fin = fields.Date(string="Date de fin réelle")
    
    amortissement_ids = fields.One2many('sigi.tableau_amortissement', 'affectation_ligne_id', string="Tableau d'Amortissement")
    
    etat_amortissement = fields.Selection([
        ('en_cours', 'Service'),
        ('amorti', '    Amorti'),
        ('termine', 'Sorti')
    ], string="Statut", default='en_cours', readonly=True)

    def action_calculer_amortissement(self):
        """ Génère le tableau d'amortissement linéaire complet """
        for ligne in self:
            # 1. Vérifications de sécurité
            if not ligne.unite_id or not ligne.matiere_id:
                raise exceptions.ValidationError("Veuillez sélectionner un bien et une matière.")
            
            valeur_achat = ligne.unite_id.cout
            duree_vie = int(ligne.matiere_id.duree)
            
            if valeur_achat <= 0:
                raise exceptions.UserError("Le coût de l'unité doit être supérieur à 0 pour calculer l'amortissement.")
            if duree_vie <= 0:
                raise exceptions.UserError("La durée de vie de la matière doit être supérieure à 0.")

            # 2. Nettoyage de l'ancien tableau
            ligne.amortissement_ids.unlink()

            # 3. Initialisation des variables
            annuite_standard = round(valeur_achat / duree_vie, 2)
            cumul = 0.0
            annee_debut = ligne.date_debut.year
            
            lignes_to_create = []

            for i in range(duree_vie):
                exercice = annee_debut + i
                
                # Ajustement pour la dernière année (pour tomber pile à zéro)
                if i == (duree_vie - 1):
                    montant_annee = valeur_achat - cumul
                    cumul = valeur_achat
                    vnc = 0.0
                else:
                    montant_annee = annuite_standard
                    cumul += montant_annee
                    vnc = valeur_achat - cumul

                lignes_to_create.append({
                    'affectation_ligne_id': ligne.id,
                    'annee': exercice,
                    'base_amortissable': valeur_achat,
                    'montant': montant_annee,
                    'cumul': cumul,
                    'valeur_restante': round(vnc, 2),
                })

            # 4. Création massive des lignes (plus performant que create en boucle)
            self.env['sigi.tableau_amortissement'].create(lignes_to_create)
            
            # 5. Mise à jour de l'état
            ligne.write({'etat_amortissement': 'amorti'})

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', '/') == '/':
                # Récupération des objets pour construire le nom
                direction = self.env['sigi.direction'].browse(vals.get('direction_id'))
                matiere = self.env['sigi.matiere'].browse(vals.get('matiere_id'))
                
                code_dir = direction.code or 'DIR'
                code_mat = matiere.code or 'MAT'
                
                # Utilisation de la séquence
                seq = self.env['ir.sequence'].next_by_code('sigi.affectation.code') or '000'
                vals['name'] = f"{code_mat}/{code_dir}/{seq}"
                
        return super(SigiAffectationLigne, self).create(vals_list)