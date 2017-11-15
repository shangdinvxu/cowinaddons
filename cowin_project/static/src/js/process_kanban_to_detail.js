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
            'click .initiate':'initiate_func',
            'click .view_tache':'view_tache_func'
        },
        //查看按钮的点击事件
        view_tache_func:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            var tache_index = $(target).parents('.process_data_item_line').attr('tache-index');
            var tache_id = parseInt($(target).parents('.process_data_item_line').attr('data-tache-id'));
            var self = this;

            var action = {
                view_type: 'form',
                view_mode: 'form',
                views: [[false, 'form']],
                res_model: self.model_arr[parseInt(tache_index)],
                res_id: self.tache_arr[tache_index].res_id,
                name: self.tache_arr[tache_index].name,
                type: 'ir.actions.act_window',
                target:'new'
            }
            self.do_action(action)

        },
        //发起按钮的点击事件
        initiate_func:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            var tache_index = $(target).parents('.process_data_item_line').attr('tache-index');
            var tache_id = parseInt($(target).parents('.process_data_item_line').attr('data-tache-id'));
            var self = this;
            self.tache_arr[tache_index].project_id = self.id;
            self.tache_arr[tache_index].tache_id = tache_id;

            var action = {
                view_type: 'form',
                view_mode: 'form',
                views: [[false, 'form']],
                res_model: self.model_arr[parseInt(tache_index)],
                context: {
                    'tache': self.tache_arr[tache_index],
                    'default_foundation_id':self.tache_arr[tache_index].round_financing_and_foundation.foundation_id,
                    'default_ownership_interest':self.tache_arr[tache_index].round_financing_and_foundation.ownership_interest,
                    'default_round_financing_and_foundation_id':self.tache_arr[tache_index].round_financing_and_foundation.round_financing_and_foundation_id,
                    'default_round_financing_id':self.tache_arr[tache_index].round_financing_and_foundation.round_financing_id,
                    'default_the_amount_of_financing': self.tache_arr[tache_index].round_financing_and_foundation.the_amount_of_financing,
                    'default_the_amount_of_investment':self.tache_arr[tache_index].round_financing_and_foundation.the_amount_of_investment
                },
                type: 'ir.actions.act_window',
                name: self.tache_arr[tache_index].name,
                target:'new'
            }
            self.do_action(action)
        },
        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.id = action.id;
            var self = this;
            //存储每个环节的model_name
            self.model_arr = [];
            //存储环节
            self.tache_arr = [];
        },
        start: function () {
            var self = this;
            return new Model("cowin_project.cowin_project")
                    .call("rpc_get_info", [self.id])
                    .then(function (result) {
                        console.log(result);
                        //获取每个环节的model_name存入数组
                        result.process.forEach(function (value) {
                            value.tache_ids.forEach(function (model) {
                                self.model_arr.push(model.model_name);
                                self.tache_arr.push((model))
                            });
                        });

                        self.id = parseInt(result.id);
                        self.$el.append(QWeb.render('project_process_detail_tmp', {result: result}))
                    })
        }
    });
    core.action_registry.add('process_kanban_to_detail', ProcessKanbanToDetail);

    return ProcessKanbanToDetail;
});