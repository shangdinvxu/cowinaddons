/**
 * Created by 123 on 2017/12/18.
 */
odoo.define('cowin_project.follow_up_invest_kanban_to_detail', function (require) {
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


    var FollowInvestKanbanToDetail = Widget.extend({
        template: '',
        events:{
            'click .process_data_rounds .fund': 'fund_func',
            'click .initiate':'initiate_func',
            'click .view_tache':'view_tache_func',
            'click .manage_team_btn':'manage_team_fun',
            'click .button_wrap .add_new_tache':'add_new_tache_func',
        },
        //环节增加
        add_new_tache_func:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            var self = this;
            var tache_index = $(target).parents('.detail_line').attr('tache-index');
            if($(target).parents('.detail_line').find('.tache_name_').text()=='投资退出申请书'){
                tache_index = parseInt(tache_index);
                var data = {
                    'sub_tache_ids':[self.tache_arr[tache_index].sub_tache_id,self.tache_arr[tache_index+1].sub_tache_id,self.tache_arr[tache_index+2].sub_tache_id,self.tache_arr[tache_index+3].sub_tache_id],
                    'meta_sub_project_id':self.tache_arr[parseInt(tache_index)].meta_sub_project_id
                }
            }else {
                var data = {
                    'sub_tache_ids':[self.tache_arr[parseInt(tache_index)].sub_tache_id],
                    'meta_sub_project_id':self.tache_arr[parseInt(tache_index)].meta_sub_project_id
                }
            }

            Dialog.confirm(this, _t("确定增加这条环节?"), {
                confirm_callback: function() {
                    return new Model("cowin_project.cowin_project")
                        .call("rpc_get_post_info",[[self.id]],data)
                        .then(function (result) {
                            result.no_initate = self.no_initate
                            console.log(result);
                            self.tache_arr=[];
                            result.process.forEach(function (value) {
                                value.tache_ids.forEach(function (model) {
                                    self.tache_arr.push(model)
                                });
                            });
                            $('.process_data_main_wrap').html('');
                            $('.process_data_main_wrap').append(QWeb.render('process_info_right_tmpl', {result: result}));
                        })
                },
            });
        },
        //项目管理团队
        manage_team_fun:function () {
            var self = this;
            $('.active_fund').html($('.active_fund').text());
            $('.active_fund').removeClass('active_fund');
            $('.manage_team_btn').addClass('manage_team_btn_active');
            return new Model("cowin_project.cowin_project")
                    .call("rpc_get_permission_configuration", [[self.id]])
                    .then(function (result) {
                        console.log(result);
                        self.employee_infos = result.employee_infos;
                        self.is_admin = result.is_admin;
                        self.meta_sub_project_infos = result.meta_sub_project_infos;

                        $('.process_data_main_wrap').html('');
                        $('.process_data_main_wrap').append(QWeb.render('project_manage_team_tmp', {result: result}))
                    })
        },
        //查看
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
                    'default_foundation_id':self.tache_arr[tache_index].round_financing_and_foundation.foundation_id,
                    'default_ownership_interest':self.tache_arr[tache_index].round_financing_and_foundation.ownership_interest,
                    'default_round_financing_and_foundation_id':self.tache_arr[tache_index].round_financing_and_foundation.round_financing_and_foundation_id,
                    'default_round_financing_id':self.tache_arr[tache_index].round_financing_and_foundation.round_financing_id,
                    'default_the_amount_of_financing': self.tache_arr[tache_index].round_financing_and_foundation.the_amount_of_financing,
                    'default_the_amount_of_investment':self.tache_arr[tache_index].round_financing_and_foundation.the_amount_of_investment,
                    'default_invest_manager_id':self.pagedata.sub_project_info ? self.pagedata.sub_project_info.invest_manager_id:'',
                    'default_name':self.pagedata.name,
                    'default_image':self.pagedata.image,
                    'default_project_number':self.pagedata.sub_project_info ? self.pagedata.sub_project_info.project_number:'',
                    'default_project_source':self.pagedata.project_source,
                    'default_project_source_note':self.pagedata.project_source_note,
                    'default_project_company_profile':self.pagedata.project_company_profile,
                    'default_project_appraisal':self.pagedata.project_appraisal,
                    'default_project_note':self.pagedata.project_note,
                    'default_industry':self.pagedata.industry,
                    'default_stage':self.pagedata.stage,
                    'default_production':self.pagedata.production,
                    'default_registered_address':self.pagedata.registered_address,
                    'default_peration_place':self.pagedata.peration_place,
                    'default_founding_time':self.pagedata.founding_time,
                    'default_person':self.pagedata.contract_person,
                    'default_contract_phone':self.pagedata.contract_phone,
                    'default_contract_email':self.pagedata.contract_email,
                    'default_attachment_ids':self.pagedata.attachment_ids,
                    'default_attachment_note':self.pagedata.attachment_note,
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
                target:'current'
            }
            self.do_action(action)

        },
        //发起
        initiate_func:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            var tache_index = $(target).parents('.process_data_item_line').attr('tache-index');
            var tache_id = parseInt($(target).parents('.process_data_item_line').attr('data-tache-id'));
            var self = this;
            self.tache_arr[tache_index].project_id = self.id;
            self.tache_arr[tache_index].tache_id = tache_id;

            //测试
            new Model("cowin_project.cowin_project")
                    .call("rpc_load_and_return_action", [parseInt(self.id)],{'tache_info':self.tache_arr[tache_index]})
                    .then(function (result) {
                        result.context['tache'] = self.tache_arr[tache_index];
                        console.log(result)
                        self.do_action(result);
                    })

            // var action = {
            //     view_type: 'form',
            //     view_mode: 'form',
            //     views: [[false, 'form']],
            //     res_model: self.tache_arr[parseInt(tache_index)].model_name,
            //     res_id: self.tache_arr[tache_index].res_id,
            //     context: {
            //         'tache': self.tache_arr[tache_index],
            //         'default_foundation_id':self.tache_arr[tache_index].round_financing_and_foundation.foundation_id,
            //         'default_ownership_interest':self.tache_arr[tache_index].round_financing_and_foundation.ownership_interest,
            //         'default_round_financing_and_foundation_id':self.tache_arr[tache_index].round_financing_and_foundation.round_financing_and_foundation_id,
            //         'default_round_financing_id':self.tache_arr[tache_index].round_financing_and_foundation.round_financing_id,
            //         'default_the_amount_of_financing': self.tache_arr[tache_index].round_financing_and_foundation.the_amount_of_financing,
            //         'default_the_amount_of_investment':self.tache_arr[tache_index].round_financing_and_foundation.the_amount_of_investment,
            //         'default_invest_manager_id':self.pagedata.sub_project_info ? self.pagedata.sub_project_info.invest_manager_id:'',
            //         'default_name':self.pagedata.name,
            //         'default_image':self.pagedata.image,
            //         'default_project_number':self.pagedata.sub_project_info ? self.pagedata.sub_project_info.project_number:'',
            //         'default_project_source':self.pagedata.project_source,
            //         'default_project_source_note':self.pagedata.project_source_note,
            //         'default_project_company_profile':self.pagedata.project_company_profile,
            //         'default_project_appraisal':self.pagedata.project_appraisal,
            //         'default_project_note':self.pagedata.project_note,
            //         'default_industry':self.pagedata.industry,
            //         'default_stage':self.pagedata.stage,
            //         'default_production':self.pagedata.production,
            //         'default_registered_address':self.pagedata.registered_address,
            //         'default_peration_place':self.pagedata.peration_place,
            //         'default_founding_time':self.pagedata.founding_time,
            //         'default_person':self.pagedata.contract_person,
            //         'default_contract_phone':self.pagedata.contract_phone,
            //         'default_contract_email':self.pagedata.contract_email,
            //         'default_attachment_ids':self.pagedata.attachment_ids,
            //         'default_attachment_note':self.pagedata.attachment_note,
            //         'default_sub_project_id':self.tache_arr[tache_index].sub_project.sub_project_id,
            //     },
            //     type: 'ir.actions.act_window',
            //     name: self.tache_arr[tache_index].name,
            //     target:'new'
            // }
            // self.do_action(action);

            // ajax监听事件 用以刷新页面
            var sub_id = $('.active_fund').attr('data-sub-id');
            var refresh_page = null;
            refresh_page = function (self,model) {
                $(document).ajaxComplete(function (event, xhr, settings) {
                    if (settings.data){
                        var data = JSON.parse(settings.data);
                        if (data.params.model && data.params.model == model) {
                            if (data.params.method == 'create'){
                                $('.close').click(function () {
                                    return new Model("cowin_project.cowin_project")
                                        .call("rpc_get_post_info", [parseInt(self.id)],{meta_project_id:parseInt(sub_id)})
                                        .then(function (result) {
                                            result.no_initate = self.no_initate
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

        //基金切换
        fund_func:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            $('.active_fund').html($('.active_fund').text());
            $('.active_fund').removeClass('active_fund');
            $('.manage_team_btn').removeClass('manage_team_btn_active')
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
                        $('.process_data_main_wrap').append(QWeb.render('after_invest_info_right_tmpl', {result: result}))
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
            action.menu_id = action.params.menu_id;
            var self = this;
            console.log(action)
            //存储环节
            self.tache_arr = [];
        },
        start: function () {
            var self = this;
            return new Model("cowin_project.cowin_project")
                    .call("rpc_get_post_info", [parseInt(self.id)],{})
                    .then(function (result) {
                        console.log(result);
                        self.pagedata = result;
                        //获取每个环节的model_name存入数组
                        result.process.forEach(function (value) {
                            value.tache_ids.forEach(function (model) {
                                self.tache_arr.push(model)
                            });
                        });
                        self.id = parseInt(result.id);
                        self.$el.append(QWeb.render('follow_up_invest_detail_tmp', {result: result}))
                    })
        }
    });
    core.action_registry.add('follow_invest_kanban_to_detail', FollowInvestKanbanToDetail);

    return FollowInvestKanbanToDetail;
});