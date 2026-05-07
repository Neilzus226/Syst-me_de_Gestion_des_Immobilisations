{
    'name': 'Gestion des Immobilisations',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Assets',
    'summary': 'Module personnalisé de gestion des actifs immobilisés',
    'description': """
                    Gestion complète des immobilisations des entreprises(TELIA)
                   """,
    'author': 'NEILL SERVICE',
    'depends': [
        'base',
        'mail',
    ],
    'sequence': -100,
    'data': [
        'security/ir.model.access.csv', 
        'data/ir_sequence_data.xml',
        'views/categorie_views.xml',
        'views/marque_views.xml',
        'views/modele_views.xml',
        'views/unite_views.xml',
        'views/fournisseur_views.xml',
        'views/nature_views.xml',
        'views/emplacement_views.xml',
        'views/matiere_views.xml',
        'views/entrer_matiere_views.xml',
        'views/affectation_views.xml',
        'views/direction_views.xml',
        'views/affectation_ligne_views.xml',
        'views/tableau_amortissement_views.xml',
        'views/sortie_views.xml',
        'views/mutation_views.xml',
        'views/inventaire_views.xml',
        'views/menus.xml',
    ],
    'assets': {
    'web.assets_backend': [
        'immobilisations/static/src/css/style.css',
        'immobilisations/static/src/css/style2.css',
    ],
},    
    
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}