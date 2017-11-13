/**
 * Created by 123 on 2017/10/30.
 */
odoo.define('cowin_project.process_kanban_to_detail', function (require) {
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


    var ProcessKanbanToDetail = Widget.extend({
        template: '',
        events:{
            'click .initiate':'initiate_func'
        },
        initiate_func:function () {
            var self = this;
            var action = {
                view_type: 'form',
                view_mode: 'form',
                views: [[false, 'form']],
                res_model: 'cowin_project.cowin_subproject',
                context: {'res_id': self.id},
                type: 'ir.actions.act_window',
                target:'new'
            }
            self.do_action(action)
        },
        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.id = action.id;
            var self = this;
        },
        start: function () {
            var self = this;
            return new Model("cowin_project.cowin_project")
                    .call("rpc_get_info", [self.id])
                    .then(function (result) {
                        console.log(result);
                        self.id = parseInt(result.id);
                        self.$el.append(QWeb.render('project_process_detail_tmp', {result: result}))
                    })
        }
    });
    core.action_registry.add('process_kanban_to_detail', ProcessKanbanToDetail);

    return ProcessKanbanToDetail;
});