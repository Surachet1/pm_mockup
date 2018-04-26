from openerp import fields, models, api, _


class SaleServiceType(models.Model):
    _name = 'sale.service.type'
    _order = "sequence"

    sequence = fields.Integer(
        string='Sequence',
        default=1,
    )
    name = fields.Char(
        string='Service Name',
    )
    code = fields.Char(
        string='Code',
    )
    deduct = fields.Boolean(
        string='Deduct Point',
        default=False,
    )
    leave = fields.Boolean(
        string='Leave',
        default=False,
    )

   #@api.multi
   #def name_get(self):
   #    res = []
   #    for rec in self:
   #        res.append((rec.id, rec.code or rec.name))
   #    return res

   #@api.v7
   #def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
   #    if not args:
   #        args = []
   #    if name:
   #        ids = self.search(cr, user, [
   #            ('code', operator, name),
   #        ] + args, limit=limit)
   #    else:
   #        ids = self.search(cr, user, args, context=context, limit=limit)
   #    return self.name_get(cr, user, ids, context=context)
