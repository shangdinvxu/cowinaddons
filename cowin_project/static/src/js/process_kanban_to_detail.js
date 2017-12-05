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
    var pyeval = require('web.pyeval');
    var _t = core._t;


    var ProcessKanbanToDetail = Widget.extend({
        template: '',
        events:{
            'click .initiate':'initiate_func',
            'click .view_tache':'view_tache_func',
            'click .process_data_rounds .fund': 'fund_func',
            'click .manage_team_btn':'manage_team_fun'
        },
        manage_team_fun:function () {
            var self = this;
            return new Model("cowin_project.cowin_project")
                    .call("rpc_get_permission_configuration", [[self.id]])
                    .then(function (result) {
                        console.log(result);
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
                    .call("rpc_get_info", [parseInt(self.id)],{meta_project_id:parseInt(sub_id)})
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
                        $('.process_data_main_wrap').append(QWeb.render('process_info_right_tmpl', {result: result}))
                    })
        },
        //查看按钮的点击事件
        view_tache_func:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            var tache_index = $(target).parents('.process_data_item_line').attr('tache-index');
            var tache_id = parseInt($(target).parents('.process_data_item_line').attr('data-tache-id'));
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

            // ajax监听事件 用以刷新页面
            var sub_id = $('.active_fund').attr('data-sub-id');
            var refresh_page = null;

            refresh_page = function (self,model) {
                $(document).ajaxComplete(function (event, xhr, settings) {
                    if (settings.data){
                        var data = JSON.parse(settings.data);
                        if (data.params.model == model) {
                            if (data.params.method == 'write'){
                                $('.close').click(function () {
                                    return new Model("cowin_project.cowin_project")
                                        .call("rpc_get_info", [parseInt(self.id)],{meta_project_id:parseInt(sub_id)})
                                        .then(function (result) {
                                            console.log(result);
                                            $('.process_data_main_wrap').html('');
                                            // 获取每个环节的model_name存入数组
                                            self.tache_arr = [];
                                            result.process.forEach(function (value) {
                                                value.tache_ids.forEach(function (model) {
                                                    self.tache_arr.push((model))
                                                });
                                            });
                                            self.id = parseInt(result.id);
                                            $('.process_data_main_wrap').append(QWeb.render('process_info_right_tmpl', {result: result}));
                                        })
                                })
                            }
                        }
                    }
                })
            }
            refresh_page(self,self.tache_arr[tache_index].model_name);

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
                res_model: self.tache_arr[parseInt(tache_index)].model_name,
                context: {
                    'tache': self.tache_arr[tache_index],
                    'default_foundation_id':self.tache_arr[tache_index].round_financing_and_foundation.foundation_id,
                    'default_ownership_interest':self.tache_arr[tache_index].round_financing_and_foundation.ownership_interest,
                    'default_round_financing_and_foundation_id':self.tache_arr[tache_index].round_financing_and_foundation.round_financing_and_foundation_id,
                    'default_round_financing_id':self.tache_arr[tache_index].round_financing_and_foundation.round_financing_id,
                    'default_the_amount_of_financing': self.tache_arr[tache_index].round_financing_and_foundation.the_amount_of_financing,
                    'default_the_amount_of_investment':self.tache_arr[tache_index].round_financing_and_foundation.the_amount_of_investment,
                    'default_invest_manager_id':self.tache_arr[tache_index].sub_project.invest_manager_id,
                    'default_name':self.tache_arr[tache_index].sub_project.name,
                    'default_project_number':self.tache_arr[tache_index].sub_project.project_number,
                    'default_sub_project_id':self.tache_arr[tache_index].sub_project.sub_project_id,
                },
                type: 'ir.actions.act_window',
                name: self.tache_arr[tache_index].name,
                target:'new'
            }
            self.do_action(action);
            
            // ajax监听事件 用以刷新页面
            var sub_id = $('.active_fund').attr('data-sub-id');
            var refresh_page = null;
            refresh_page = function (self,model) {
                $(document).ajaxComplete(function (event, xhr, settings) {
                    if (settings.data){
                        var data = JSON.parse(settings.data);
                        if (data.params.model == model) {
                            if (data.params.method == 'create'){
                                $('.close').click(function () {
                                    return new Model("cowin_project.cowin_project")
                                        .call("rpc_get_info", [parseInt(self.id)],{meta_project_id:parseInt(sub_id)})
                                        .then(function (result) {
                                            console.log(result);
                                            $('.process_data_main_wrap').html('');
                                            // 获取每个环节的model_name存入数组
                                            self.tache_arr = [];
                                            result.process.forEach(function (value) {
                                                value.tache_ids.forEach(function (model) {
                                                    self.tache_arr.push((model))
                                                });
                                            });
                                            self.id = parseInt(result.id);
                                            $('.process_data_main_wrap').append(QWeb.render('process_info_right_tmpl', {result: result}));
                                            $('.process_funds_rounds').html('');
                                            $('.process_funds_rounds').append(QWeb.render('process_info_left_tmpl', {result: result,active_flag:sub_id}));
                                        })
                                })
                            }
                        }
                    }
                })
            }
            refresh_page(self,self.tache_arr[tache_index].model_name);
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
                    .call("rpc_get_info", [parseInt(self.id)],{})
                    .then(function (result) {
                        console.log(result);
                        //获取每个环节的model_name存入数组
                        result.process.forEach(function (value) {
                            value.tache_ids.forEach(function (model) {
                                self.tache_arr.push(model)
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