/**
 * Created by 123 on 2017/10/23.
 */
odoo.define('cowin_settings.process_conf', function (require) {
    "use strict";

    var core = require('web.core');
    var Model = require('web.Model');
    var Widget = require('web.Widget');
    var View = require('web.View');
    var QWeb = core.qweb;
    var ControlPanelMixin = require('web.ControlPanelMixin');
    var ControlPanel = require('web.ControlPanel');
    var Dialog = require('web.Dialog');
    var ControlPanelMixin = require('web.ControlPanelMixin');
    var SearchView = require('web.SearchView');
    var data = require('web.data');
    var _t = core._t;


    var ProcessConf = Widget.extend({
        template: 'process_conf_tmp',
        events:{
            'click .process_conf_click_to_detail': 'to_process_conf_detail'
        },
        to_process_conf_detail:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            var active_detail_id = $(target).parent('tr').attr('data-id');
            var action = {
                type: 'ir.actions.client',
                name: 'process',
                tag: 'process_conf_detail',
                active_id: active_detail_id,
                params:{'active_id': active_detail_id}
            };
            this.do_action(action);
        },
        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.bom_id = action.bom_id;
            var self = this;
        },
        start: function () {
            var self = this;
            return new Model("cowin_settings.process")
                    .call("get_infos", [""])
                    .then(function (result) {
                        console.log(result);
                        self.$("#process_detail").append(QWeb.render('process_conf_projects', {result: result}))
                    })

        }
    });
    core.action_registry.add('process_conf', ProcessConf);

    return ProcessConf;
});