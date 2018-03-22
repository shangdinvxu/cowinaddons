/**
 * Created by 123 on 2018/3/20.
 */

odoo.define('cowin_foundation.foundation_info', function (require) {
    "use strict";

    var core = require('web.core');
    var Model = require('web.Model');
    var Widget = require('web.Widget');
    var View = require('web.View');
    var QWeb = core.qweb;
    var ControlPanelMixin = require('web.ControlPanelMixin');
    var ControlPanel = require('web.ControlPanel');
    var Dialog = require('web.Dialog');
    var ActionManager = require('web.ActionManager')
    var SearchView = require('web.SearchView');
    var data = require('web.data');
    var pyeval = require('web.pyeval');
    var _t = core._t;

    var FoundationInfo = Widget.extend({
        events:{
            'click .edit_foundation':'edit_foundation_func',
        },
        //基金情况表编辑
        edit_foundation_func:function () {
            var action = {
                'name': '基金',
                'view_type': 'form',
                'view_mode': 'form',
                'views': [[false, 'form']],
                'res_id': this.id,
                'res_model': 'cowin_foundation.cowin_foundation',
                'type': 'ir.actions.act_window',
                'target': 'current'
            };
            this.do_action(action);
        },

        on_attach_callback: function() {
            console.log('yfei');

        },


        on_detach_callback: function() {
            console.log('离开页面');
        },

        do_push_state: function(state) {
            this._super(state);
        },



        init: function (parent, action, options) {
            this._super(parent);
            this._super.apply(this, arguments);
            options = options || {};
            this.context = options.context || {};

            if(action.active_id){
                this.id = action.active_id;
            }else {
                this.id = action.params.active_id;
            }

            this.action = action;
        },
        start: function () {
            var self = this;
            var defered = new Model("cowin_foundation.cowin_foundation")
                    .call("rpc_get_foundation_info", [parseInt(self.id)],{})
                    .then(function (result){
                        console.log(result);
                        self.form_id = result.foundation_info.form_id;
                        self.$el.append(QWeb.render('foundation_info_templ', {result: result.foundation_info}))
                    });
            return defered
        },

    });

    core.action_registry.add('foundation_info', FoundationInfo);

    return FoundationInfo;
});