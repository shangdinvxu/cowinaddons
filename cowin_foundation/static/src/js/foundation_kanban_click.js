/**
 * Created by 123 on 2018/3/20.
 */
odoo.define('foundation.kanban',function (require) {
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
            if(this.model === 'cowin_foundation.cowin_foundation'){
                if(this.$el.eq(0).hasClass('foundation_infos_kanban')){
                    var action = {
                        type: 'ir.actions.client',
                        name: self.record.name.raw_value,
                        tag: 'foundation_info',
                        active_id: this.record.id.raw_value,
                        params:{
                            model: 'cowin_foundation.cowin_foundation',
                            action: 'foundation_info',
                        }
                    };
                    this.do_action(action);
                }
            }else {
                this._super.apply(this, arguments);
            }
        }
    });

});