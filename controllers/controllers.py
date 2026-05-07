# -*- coding: utf-8 -*-
# from odoo import http


# class Immobilisations(http.Controller):
#     @http.route('/immobilisations/immobilisations', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/immobilisations/immobilisations/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('immobilisations.listing', {
#             'root': '/immobilisations/immobilisations',
#             'objects': http.request.env['immobilisations.immobilisations'].search([]),
#         })

#     @http.route('/immobilisations/immobilisations/objects/<model("immobilisations.immobilisations"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('immobilisations.object', {
#             'object': obj
#         })

