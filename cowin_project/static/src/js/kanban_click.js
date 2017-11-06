/**
 * Created by 123 on 2017/10/30.
 */
odoo.define('project.update_kanban', function (require) {
'use strict';

var core = require('web.core');
var data = require('web.data');
var Dialog = require('web.Dialog');
var Model = require('web.Model');
var session = require('web.session');

var KanbanView = require('web_kanban.KanbanView');
var KanbanRecord = require('web_kanban.Record');

var QWeb = core.qweb;
var _t = core._t;

KanbanRecord.include({
    on_card_clicked: function () {
        if (this.model === 'project.project') {
            this.$('.o_project_kanban_boxes a').first().click();
        }else if(this.model === 'cowin_project.cowin_project'){
            console.log('sssssssss');
            console.log(this.record.id.raw_value)
            var action = {
                type: 'ir.actions.client',
                name: 'process',
                tag: 'process_kanban_to_detail',
                id: this.record.id.raw_value,
            }
            this.do_action(action);
        }
        else {
            this._super.apply(this, arguments);
        }
    }
});
});
