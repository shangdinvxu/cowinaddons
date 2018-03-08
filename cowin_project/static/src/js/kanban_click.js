/**
 * Created by 123 on 2017/10/30.
 */
odoo.define('project.update_kanban', function (require) {
'use strict';

var core = require('web.core');
var data = require('web.data');
var data_manager = require('web.data_manager');
var Model = require('web.DataModel');
var ListView = require('web.ListView');
var Dialog = require('web.Dialog');
var form_common = require('web.form_common');
var Pager = require('web.Pager');
var pyeval = require('web.pyeval');
var QWeb = require('web.QWeb');
var session = require('web.session');
var utils = require('web.utils');
var View = require('web.View');

var KanbanColumn = require('web_kanban.Column');
var quick_create = require('web_kanban.quick_create');
var KanbanRecord = require('web_kanban.Record');
var kanban_widgets = require('web_kanban.widgets');

var qweb = core.qweb;
var _lt = core._lt;
var _t = core._t;
var ColumnQuickCreate = quick_create.ColumnQuickCreate;
var fields_registry = kanban_widgets.registry;

KanbanRecord.include({
    on_card_clicked: function () {
        var self = this;
        if (this.model === 'project.project') {
            this.$('.o_project_kanban_boxes a').first().click();
        }else if(this.model === 'cowin_project.cowin_project'){
            console.log(this)
            if(this.$el.eq(0).hasClass('project_process_kanban')){
                if(this.$el.eq(0).hasClass('project_search_kanban')){
                    var no_initate = true
                }else {
                    var no_initate = false
                }
                var action = {
                    type: 'ir.actions.client',
                    // name: '项目流程详细',
                    name: self.record.name.raw_value,
                    tag: 'process_kanban_to_detail',
                    // id: this.record.id.raw_value,
                    active_id:this.record.id.raw_value,
                    params:{
                        'no_initate':no_initate,
                        'active_id':this.record.id.raw_value,
                        action:'process_kanban_to_detail',
                        _push_me:false,
                        model:'cowin_project.cowin_project',
                        menu_id: 117,
                    }
                };
                this.do_action(action);
            }else if(this.$el.eq(0).hasClass('project_approval_kanban')){
                var action = {
                    type: 'ir.actions.client',
                    // name: '项目审批',
                    name: self.record.name.raw_value,
                    res_model:'cowin_project.cowin_project',
                    res_id:this.id,
                    tag: 'approval_kanban_to_detail',
                    active_id:this.record.id.raw_value,
                    params:{'active_id':this.record.id.raw_value,action:'approval_kanban_to_detail',_push_me:false,model:'cowin_project.cowin_project'}
                }
                this.do_action(action);
            }else if(this.$el.eq(0).hasClass('project_follow_up_invest_kanban')){
                var action = {
                    type: 'ir.actions.client',
                    // name: '投后跟进',
                    name: self.record.name.raw_value,
                    res_model:'cowin_project.cowin_project',
                    res_id:this.id,
                    tag: 'follow_invest_kanban_to_detail',
                    active_id:this.record.id.raw_value,
                    params:{'active_id':this.record.id.raw_value,action:'follow_invest_kanban_to_detail',_push_me:false,model:'cowin_project.cowin_project'}
                }
                this.do_action(action);
            }else if(this.$el.eq(0).hasClass('project_after_invest_approval_kanban')){
                var action = {
                    type: 'ir.actions.client',
                    // name: '投后审批',
                    name: self.record.name.raw_value,
                    tag: 'approval_after_invest_kanban_to_detail',
                    res_model:'cowin_project.cowin_project',
                    res_id:this.id,
                    active_id:this.record.id.raw_value,
                    params:{'active_id':this.record.id.raw_value,action:'approval_after_invest_kanban_to_detail',_push_me:false,model:'cowin_project.cowin_project'}
                }
                this.do_action(action);
            }
        }
        else {
            this._super.apply(this, arguments);
        }
    }
});
});
