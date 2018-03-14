odoo.define('cowin_project.Custom_progress_bar', function (require) {
"use strict";

var core = require('web.core');
var utils = require('web.utils');
var Widget = require('web.Widget');
var common = require('web.form_common');
var QWeb = core.qweb;
var _t = core._t;
var ProgressBar = require('web.ProgressBar');
/**
 * options
 * - readonly
 * - value
 * - max_value
 * - title: title of the gauge, displayed on the left
 */

ProgressBar.include({
    _render_value: function(v) {
        var value = this.value;
        var max_value = this.max_value;
        if(!isNaN(v)) {
            if(this.edit_max_value) {
                max_value = v;
            } else {
                value = v;
            }
        }
        value = value || 0;
        max_value = max_value || 0;

        var widthComplete;
        if(value <= max_value) {
            widthComplete = value/max_value * 100;
        } else {
            widthComplete = 100;
        }

        this.$('.o_progress').toggleClass('o_progress_overflow', value > max_value);
        this.$('.o_progressbar_complete').css('width', widthComplete + '%');

        if(this.readonly) {
            if(max_value !== 100) {
                this.$('.o_progressbar_value').html(utils.human_number(value) + " / " + utils.human_number(max_value));
            } else {
                this.$('.o_progressbar_value').html(utils.round_decimals(value, 2) + "%");
            }
        } else if(isNaN(v)) {
            this.$('.o_progressbar_value').val(this.edit_max_value ? max_value : value);
            if(this.$('.o_progressbar_value').next() && this.$('.o_progressbar_value').next().hasClass('edit_bfh')){

            }else {
                this.$('.o_progressbar_value').after('<span class="edit_bfh">%</span>')
            }
        }
    }
})

// The progressbar field expects a float from 0 to 100.
var Custome_FieldProgressBar = common.AbstractField.extend(common.ReinitializeFieldMixin, {
    initialize_content: function() {
        if(this.progressbar) {
            this.progressbar.destroy();
        }

        this.progressbar = new ProgressBar(this, {
            readonly: this.get('effective_readonly'),
            // readonly: false,
            edit_on_click: false,
            // edit_on_click: false,
            value: this.get('value') || 0,
        });

        var self = this;
        this.progressbar.appendTo('<div>').done(function() {
            self.progressbar.$el.addClass(self.$el.attr('class'));
            self.replaceElement(self.progressbar.$el);

            self.progressbar.on('update', self, function(update) {
                self.set('value', update.changed_value);
            });
        });
    },
    render_value: function() {
        this.progressbar.set_value(this.get('value'));
    },
    is_false: function() {
        return false;
    },
});

core.form_widget_registry.add('custome_fieldprogressBar', Custome_FieldProgressBar);


return {
    // Custom_progress_bar: Custom_progress_bar,
    Custome_FieldProgressBar: Custome_FieldProgressBar,
};


});