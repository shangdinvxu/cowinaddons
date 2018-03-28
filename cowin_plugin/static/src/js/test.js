/**
 * Created by 123 on 2018/3/20.
 */

odoo.define('cowin_plugin.test', function (require) {
    "use strict";

    var core = require('web.core');
    var Model = require('web.Model');
    var Widget = require('web.Widget');
    var FormView = require('web.FormView');
    var View = require('web.View');
    var QWeb = core.qweb;
    var ControlPanelMixin = require('web.ControlPanelMixin');
    var ControlPanel = require('web.ControlPanel');
    var Dialog = require('web.Dialog');
    var ActionManager = require('web.ActionManager');
    var SearchView = require('web.SearchView');
    var data = require('web.data');
    var pyeval = require('web.pyeval');
    var data_manager = require('web.data_manager');
    var _t = core._t;

    var Test = Widget.extend({
        init:function (parent, action, options) {
             this._super(parent);
            this._super.apply(this, arguments);
            var context = {
                lang: 'en_US',
                uid: 1,
            };

            this.dataset = new data.DataSetStatic(this, 'peng.peng', context, [1]);
            this.dataset.index = 0;

            this.views = {};
            this.views['form'] = {};

        },


        init_form: function () {
            var self = this;
            var views = [];
            views.push([false, 'form']);
            var options = {
                // action_id: this.action.id,
                load_fields: ['name'],
                // toolbar: this.flags.sidebar,
            };

            var fields_def = data_manager.load_views(self.dataset, views, options).then(function (fields_views) {
                _.each(fields_views, function (fields_view, view_type) {
                    if ( view_type === 'form') {
                        self.views[view_type].fields_view = fields_view;
                    }});
            });

            var def = this.dataset.read_slice(['name']).then(function (res) {
                console.log(res);
                self.datarecord = res[0]
            });


            return $.when(fields_def, def).then(function () {
                // var fields = self.views.form.fields_view.fields;
                var form_controller = new FormView(self, self.dataset, self.views['form'].fields_view);
                // self.$el.html('');
                // self.$el.append(form_controller.$el);
                form_controller.appendTo(self.$el);
                return form_controller.do_show();

            })
        },



        start: function () {
            var self = this;
            console.log(self);
            // this.$el.append("<div>Are you sure you want to perform this action?</div>" +
            //         "<button class='ok_button'>Ok</button>" +
            //         "<button class='cancel_button'>Cancel</button>");
            //     this.$el.find("button.ok_button").click(function() {
            //         self.trigger("user_choose", true);
            //     });
            //     this.$el.find("button.cancel_button").click(function() {
            //         self.trigger("user_choose", false);
            //     });



            return this.init_form();


        },
        user_choose:function () {
            alert('yes')
        },

    });

    core.action_registry.add('test', Test);

    return Test;
});