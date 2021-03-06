/**
 * Created by 123 on 2017/12/18.
 */
odoo.define('cowin_project.approval_after_invest_kanban_to_detail', function (require) {
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
    var pyeval = require('web.pyeval');
    var _t = core._t;

    var meta_sub_project_id;
    var sub_approval_flow_settings_id;
    var sub_tache_id;
    var approval_tache_index;    //当前审核节点


    var ApprovalAfterInvestKanbanToDetail = Widget.extend({
        template: '',
        events:{
            'click .process_data_rounds .fund': 'fund_func',
            'click .to_approval':'to_approval_func',
            'click .approval_btn':'approval_btn_func',
            'click .view_approval':'view_approval_func',
            'click .approval_body div':'view_approval_tache',
            'click .operate_records':'operate_records_func',
        },
         //操作记录
        operate_records_func:function () {
            var self = this;
            return new Model("cowin_project.cowin_project")
                    .call("rpc_get_operation_record",[self.id])
                    .then(function (result) {
                        console.log(result);
                        $('#process_record').html('');
                        $('#process_record').append(QWeb.render('operate_records_tmpl', {result: result}))
                    })
        },
        //查看审核的环节
        view_approval_tache:function () {
            var tache_index = approval_tache_index;
            var self = this;
            var context ={
                    'tache': self.tache_arr[tache_index],
                };
            if(self.tache_arr[tache_index].round_financing_and_foundation){
                context = {
                    'tache': self.tache_arr[tache_index],
                    'default_foundation_id': self.tache_arr[tache_index].round_financing_and_foundation.foundation_id,
                    'default_ownership_interest':self.tache_arr[tache_index].round_financing_and_foundation.ownership_interest,
                    'default_round_financing_and_foundation_id':self.tache_arr[tache_index].round_financing_and_foundation.round_financing_and_foundation_id,
                    'default_round_financing_id':self.tache_arr[tache_index].round_financing_and_foundation.round_financing_id,
                    'default_the_amount_of_financing': self.tache_arr[tache_index].round_financing_and_foundation.the_amount_of_financing,
                    'default_the_amount_of_investment':self.tache_arr[tache_index].round_financing_and_foundation.the_amount_of_investment,
                    'default_invest_manager_id':self.tache_arr[tache_index].sub_project.invest_manager_id,
                    'default_name':self.tache_arr[tache_index].sub_project.name,
                    'default_project_number':self.tache_arr[tache_index].sub_project.project_number,
                    'default_sub_project_id':self.tache_arr[tache_index].sub_project.sub_project_id,
                }
            }

            var action = {
                view_type: 'form',
                view_mode: 'form',
                views: [[false, 'form']],
                res_model: self.tache_arr[parseInt(tache_index)].model_name,
                res_id: self.tache_arr[tache_index].res_id,
                name: self.tache_arr[tache_index].name,
                type: 'ir.actions.act_window',
                context: context,
                target:'new'
            }
            self.do_action(action)
        },
        //查看审核页面
        view_approval_func:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            var self = this;
            meta_sub_project_id = $(target).parents('.process_data_item_line').attr('data-sub-project-id');
            sub_approval_flow_settings_id = $(target).parents('.process_data_item_line').attr('data-sub-approval-id');
            sub_tache_id = $(target).parents('.process_data_item_line').attr('data-sub-tache-id');
            approval_tache_index = $(target).parents('.process_data_item_line').attr('tache-index');
            var data = {
                "tache":{
                    "meta_sub_project_id":parseInt(meta_sub_project_id),
                    "sub_approval_flow_settings_id":parseInt(sub_approval_flow_settings_id)
                }
            };

            return new Model("cowin_project.cowin_project")
                    .call("rpc_get_approval_flow_info", [parseInt(self.id)],data)
                    .then(function (result) {
                        $('#process_data').html('')
                        console.log(result);
                        $('#process_data').append(QWeb.render('approval_page', {result: result,edit:false}))
                    })
        },
        //审核同意、不同意
        approval_btn_func:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            if($(target).hasClass('approval_yes')){
                var approval_result = true;
            }else if($(target).hasClass('approval_no')){
                var approval_result = false;
            }else {
                var approval_result = null;
            }
            var opinion = $('.approval_opinion').val();
            var self = this;
            var data = {
                "tache":{
                    "meta_sub_project_id":parseInt(meta_sub_project_id),
                    "sub_approval_flow_settings_id":parseInt(sub_approval_flow_settings_id),
                    'sub_tache_id': parseInt(sub_tache_id),
                },
                'approval_flow_settings_record':{
                    'approval_result': approval_result,
                    'approval_opinion': opinion,
                },
                'prev_or_post_investment': false
            };
            return new Model("cowin_project.cowin_project")
                    .call("rpc_save_approval_flow_info", [parseInt(self.id)],data)
                    .then(function (result) {
                        console.log(result);
                        $('#process_data').html('');
                        $('#process_data').append(QWeb.render('process_info', {result: result}))
                    })
        },
        //到审核页面
        to_approval_func:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            var self = this;
            meta_sub_project_id = $(target).parents('.process_data_item_line').attr('data-sub-project-id');
            sub_approval_flow_settings_id = $(target).parents('.process_data_item_line').attr('data-sub-approval-id');
            sub_tache_id = $(target).parents('.process_data_item_line').attr('data-sub-tache-id');
            approval_tache_index = $(target).parents('.process_data_item_line').attr('tache-index');
            var data = {
                "tache":{
                    "meta_sub_project_id":parseInt(meta_sub_project_id),
                    "sub_approval_flow_settings_id":parseInt(sub_approval_flow_settings_id)
                }
            };

            return new Model("cowin_project.cowin_project")
                    .call("rpc_get_approval_flow_info", [parseInt(self.id)],data)
                    .then(function (result) {
                        $('#process_data').html('')
                        console.log(result);
                        $('#process_data').append(QWeb.render('approval_page', {result: result,edit:true}))
                    })

        },
        //基金切换
        fund_func:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            $('.active_fund').html($('.active_fund').text());
            $('.active_fund').removeClass('active_fund');
            $(target).addClass('active_fund');
            $(target).append("<span class='fa fa-chevron-right'></span>");
            var sub_id = $(target).attr('data-sub-id');
            var self =this;
            self.tache_arr = [];
            return new Model("cowin_project.cowin_project")
                    .call("rpc_get_post_info", [parseInt(self.id)],{meta_project_id:parseInt(sub_id)})
                    .then(function (result) {
                        console.log(result);
                        $('.process_data_main_wrap').html('');
                        // 获取每个环节的model_name存入数组
                        result.process.forEach(function (value) {
                            value.tache_ids.forEach(function (model) {
                                self.tache_arr.push((model))
                            });
                        });
                        self.id = parseInt(result.id);
                        $('.process_data_main_wrap').append(QWeb.render('approval_info_right_tmpl', {result: result}))
                    })
        },

        init: function (parent, action) {
            this._super(parent);
            this._super.apply(this, arguments);
            if(action.active_id){
                this.id = action.active_id;
            }else {
                this.id = action.params.active_id;
            }
            var self = this;
            // console.log(action);
            //存储环节
            self.tache_arr = [];
        },
        start: function () {
            var self = this;
            return new Model("cowin_project.cowin_project")
                    .call("rpc_get_post_info", [parseInt(self.id)],{})
                    .then(function (result) {
                        console.log(result);
                        //获取每个环节的model_name存入数组
                        result.process.forEach(function (value) {
                            value.tache_ids.forEach(function (model) {
                                self.tache_arr.push(model)
                            });
                        });

                        self.id = parseInt(result.id);
                        self.$el.append(QWeb.render('project_approval_after_invest_detail_tmp', {result: result}))
                    })
        }
    });
    core.action_registry.add('approval_after_invest_kanban_to_detail', ApprovalAfterInvestKanbanToDetail);

    return ApprovalAfterInvestKanbanToDetail;
});