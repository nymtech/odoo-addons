from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class WhitelistMixin(models.AbstractModel):
    _name = "whitelist.mixin"
    _description = "whitelist.mixin"

    allowed_user_ids = fields.Many2many(
        "res.users",
        string="Allowed users",
        copy=False,
        default=lambda self: [self.env.user.id],
    )
    can_edit_allowed_user_ids = fields.Boolean(compute="_compute_edit_allowed_user_ids")

    def _get_allowed_group_ids(self):
        """ To implement in submodules, should return a list of xml ids of res.groups """
        raise NotImplementedError()

    @api.depends('allowed_user_ids')
    def _compute_edit_allowed_user_ids(self):
        allowed_groups = self._get_allowed_group_ids()
        self.can_edit_allowed_user_ids = any([self.env.user.has_group(group) for group in allowed_groups])


    @api.constrains("allowed_user_ids")
    def _check_allowed_user_ids(self):
        for rec in self:
            if not rec.allowed_user_ids:
                raise ValidationError(
                    _(
                        """You must select at least one allowed user.\n
                    Record name: %s
                    Technical data: %s(%s)""",
                        rec.display_name,
                        rec._name,
                        rec.id,
                    )
                )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "allowed_user_ids" not in vals:
                vals["allowed_user_ids"] = []
            vals["allowed_user_ids"].append((4, self.env.user.id))
        return super(WhitelistMixin, self).create(vals_list)

    def write(self, vals):
        if not self[:1].can_edit_allowed_user_ids:
            vals.pop('allowed_user_ids', None)
        return super(WhitelistMixin, self).write(vals)


    @api.model
    def whitelist_groups(self, *group_names):
        """
        After a submodule installation `allowed_user_ids` is empty by default, meaning that some records will be hidden for all users.
        To prevent that, you should call this method at installation of the submodule through a "function" tag in an XML file, i.e.

        <function model="account.journal" name="whitelist_groups" eval="['account.group_account_manager']" />

        This will default the `allowed_user_ids` field to the users of the given groups.
        """
        groups = self.env["res.groups"]
        for xml_id in group_names:
            groups |= self.env.ref(xml_id)
        self.search([]).write(
            {
                "allowed_user_ids": [(6, 0, groups.users.ids)],
            }
        )
