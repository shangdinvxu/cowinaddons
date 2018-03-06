odoo.define('cowin_project.Custom_progress_bar', function (require) {
"use strict";

var core = require('web.core');
var utils = require('web.utils');
var Widget = require('web.Widget');
var common = require('web.form_common');
var QWeb = core.qweb;
var _t = core._t;

/**
 * options
 * - readonly
 * - value
 * - max_value
 * - title: title of the gauge, displayed on the left
 */
var Custom_progress_bar = Widget.extend({
    template: "Custome_ProgressBar",

    events: {
        'change input': 'on_change_input',
        'input input': 'on_change_input',
        'keyup input': function(e) {
            if(e.which === $.ui.keyCode.ENTER) {
                this.on_change_input(e);
            }
        },
    },

    init: function (parent, options) {
            this._super(parent);

            options.edit_on_click = true;

            options = _.defaults(options || {}, {
                readonly: true,
                edit_on_click: false,
                value: 0,
                max_value: 100,
                title: '',
                edit_max_value: false,
            });

            this.readonly = options.readonly;
            this.edit_on_click = options.edit_on_click;
            this.value = options.value;
            this.max_value = options.max_value;
            this.title = options.title;
            this.edit_max_value = options.edit_max_value;
        },

    start: function() {
        this._render_value();

        if(!this.readonly) {
            if(this.edit_on_click) {
                var self = this;
                this.$el.on('click', '.o_progress', function(e) {
                    var $target = $(e.currentTarget);
                    self.value = Math.floor((e.pageX - $target.offset().left) / $target.outerWidth() * self.max_value);
                    self._render_value();
                    self.trigger('update', {value: self.value, max_value: self.max_value, changed_value: self.value});
                });
            } else {
                this.$el.on('blur', 'input', _.bind(this.on_change_input, this));
            }

            this.$('.o_progressbar_value').focus().select()
        }

        return this._super();
    },

    on_change_input: function(e) {
            var $input = $(e.target);
            if(e.type === 'change' && !$input.is(':focus')) {
                return;
            }
            if(isNaN($input.val())) {
                this.do_warn(_t("Wrong value entered!"), _t("Only Integer Value should be valid."));
            } else {
                if(e.type === 'input') {
                    if(this.edit_max_value) {
                        this.max_value = $(e.target).val();
                    } else {
                        this.value = $(e.target).val() || 0;
                    }

                    this._render_value($input.val());
                    this.trigger('update', {value: this.value, max_value: this.max_value, changed_value: (this.edit_max_value)? this.max_value : this.value});

                    if(parseFloat($input.val()) === 0) {
                        $input.select();
                    }
                } else {
                    if(this.edit_max_value) {
                        this.max_value = $(e.target).val();
                    } else {
                        this.value = $(e.target).val() || 0;
                    }

                    this._render_value();
                    this.trigger('update', {value: this.value, max_value: this.max_value, changed_value: (this.edit_max_value)? this.max_value : this.value});
                }
            }
    },

    set_value: function(v) {
        this.value = v;
        this._render_value();
    },

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

            // this.$('.o_progress').toggleClass('o_progress_overflow', value > max_value);
            // this.$('.o_progressbar_complete').css('width', widthComplete + '%');

            if(this.readonly) {
                if(max_value !== 100) {
                    this.$('.o_progressbar_value').html(utils.human_number(value) + " / " + utils.human_number(max_value));
                } else {
                    this.$('.o_progressbar_value').html(utils.round_decimals(value, 2) + "%");
                }
            } else if(isNaN(v)) {
                this.$('.o_progressbar_value').val(this.edit_max_value ? max_value : value);
            }}
});

// The progressbar field expects a float from 0 to 100.
var Custome_FieldProgressBar = common.AbstractField.extend(common.ReinitializeFieldMixin, {
    initialize_content: function() {
        if(this.progressbar) {
            this.progressbar.destroy();
        }

        this.progressbar = new Custom_progress_bar(this, {
            readonly: this.get('effective_readonly'),
            // readonly: false,
            edit_on_click: true,
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
    Custom_progress_bar: Custom_progress_bar,
    Custome_FieldProgressBar: Custome_FieldProgressBar,
};


});