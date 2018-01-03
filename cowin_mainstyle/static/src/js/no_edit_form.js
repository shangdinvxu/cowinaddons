/**
 * Created by 123 on 2018/1/2.
 */
odoo.define('web.form', function (require) {
    "use strict";
    /*---------------------------------------------------------
     * Odoo Editable List view linkloving version
     *---------------------------------------------------------*/
    /**
     * handles editability case for lists, because it depends on form and forms already depends on lists it had to be split out
     * @namespace
     */

    var core = require('web.core');
    var data = require('web.data');
    var FormView = require('web.FormView');
    var common = require('web.list_common');
    var ListView = require('web.ListView');
    var Model = require('web.Model');
    var utils = require('web.utils');
    var Widget = require('web.Widget');

    var _t = core._t;

    FormView.include(/** @lends instance.web.ListView.List# */{
        _process_save: function(save_obj) {
            var self = this;
            var prepend_on_create = save_obj.prepend_on_create;
            var def_process_save = $.Deferred();
            try {
                var form_invalid = false,
                    values = {},
                    first_invalid_field = null,
                    readonly_values = {},
                    deferred = [];

                $.when.apply($, deferred).always(function () {

                    _.each(self.fields, function (f) {
                        if (!f.is_valid()) {
                            form_invalid = true;
                            if (!first_invalid_field) {
                                first_invalid_field = f;
                            }
                        } else if (f.name !== 'id' && (!self.datarecord.id || f._dirty_flag)) {
                            // Special case 'id' field, do not save this field
                            // on 'create' : save all non readonly fields
                            // on 'edit' : save non readonly modified fields
                            if (!f.get("readonly")) {
                                values[f.name] = f.get_value(true);
                            } else {
                                readonly_values[f.name] = f.get_value(true);
                            }
                        }

                    });

                    // Heuristic to assign a proper sequence number for new records that
                    // are added in a dataset containing other lines with existing sequence numbers
                    if (!self.datarecord.id && self.fields.sequence &&
                        !_.has(values, 'sequence') && !_.isEmpty(self.dataset.cache)) {
                        // Find current max or min sequence (editable top/bottom)
                        var current = _[prepend_on_create ? "min" : "max"](
                            _.map(self.dataset.cache, function(o){return o.values.sequence})
                        );
                        values['sequence'] = prepend_on_create ? current - 1 : current + 1;
                    }
                    if (form_invalid) {
                        self.set({'display_invalid_fields': true});
                        first_invalid_field.focus();
                        self.on_invalid();
                        def_process_save.reject();
                    } else {
                        self.set({'display_invalid_fields': false});
                        var save_deferral;
                        if (!self.datarecord.id) {
                            // Creation save
                            save_deferral = self.dataset.create(values, {readonly_fields: readonly_values}).then(function(r) {
                                self.display_translation_alert(values);
                                return self.record_created(r, prepend_on_create);
                            }, null);
                        }  else {
                            // Write save
                            save_deferral = self.dataset.write(self.datarecord.id, values, {readonly_fields: readonly_values}).then(function(r) {
                                self.display_translation_alert(values);
                                return self.record_saved(r);
                            }, null);
                        }
                        save_deferral.then(function(result) {
                            def_process_save.resolve(result);
                        }).fail(function() {
                            def_process_save.reject();
                        });
                    }
                });
            } catch (e) {
                console.error(e);
                return def_process_save.reject();
            }
            return def_process_save;
        },
    });
});
