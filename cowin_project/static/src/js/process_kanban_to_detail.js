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
            'click .manage_team_btn':'manage_team_fun',
            'click .add_new_role':'show_add_new_sels',
            'click .cancel_sel':'hide_add_new_sels',
            'click .confirm_sel':'confirm_add_new_sels',
            'click .confirm_project_team_setting':'confirm_project_team_setting_func',
            'click .member_name .fa':'del_member_func',
            'click .copy_this_setting':'get_all_settings',
            'click .confirm_copy':'confirm_copy_func',
            'click .button_wrap .add_new_tache':'add_new_tache_func'
        },
        add_new_tache_func:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            var self = this;
            var tache_index = $(target).parents('.detail_line').attr('tache-index');
            Dialog.confirm(this, _t("确定增加这条环节?"), {
                confirm_callback: function() {
                    return new Model("cowin_project.cowin_project")
                        .call("new_sub_tache",[[self.id]],{'sub_tache_id':self.tache_arr[parseInt(tache_index)],'meta_sub_project_id':self.tache_arr[parseInt(tache_index)].meta_sub_project_id})
                        .then(function (result) {
                            console.log(result);
                        })
                },
            });
        },
        //确定复制配置
        confirm_copy_func:function () {
            var self = this;
            $('.copy_sel option:selected').each(function () {
                self.copy_meta_sub_pro_id = parseInt($(this).attr('data-id'));
            })
            return new Model("cowin_project.cowin_project")
                    .call("rpc_copy_permission_configuration",[[self.id]],{current_meta_sub_pro_id:self.current_meta_sub_pro_id,copy_meta_sub_pro_id:self.copy_meta_sub_pro_id})
                    .then(function (result) {
                        console.log(result);
                        $('.process_data_main_wrap').html('');
                        $('.process_data_main_wrap').append(QWeb.render('project_manage_team_tmp', {result: result}))
                    })
        },
        //复制已有模板
        get_all_settings:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            var self = this;
            self.current_meta_sub_pro_id = parseInt($(target).parents('.header_line').attr('meta_sub_pro_id'));
            var self = this;
            return new Model("cowin_project.cowin_project")
                    .call("rpc_copy_all_permission_configuration",[[self.id]])
                    .then(function (result) {
                        console.log(result);
                        $('.process_data_main_wrap').append(QWeb.render('copy_settings_tmpl', {result: result,current:self.current_meta_sub_pro_id}));
                        $('.copy_settings_tmpl .add_new_content').show()
                    })
        },
        //删除
        del_member_func:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            $(target).parents('.member_name').remove()
        },
        //保存项目管理团队设置
        confirm_project_team_setting_func:function () {
            var self = this;
            $('.detail_lines_wrap').each(function (i) {
                $(this).find('.detail_line').each(function (j) {
                    self.meta_sub_project_infos[i].approval_role_infos[j].employee_infos = [];
                    $(this).find('.member_name').each(function () {
                        self.meta_sub_project_infos[i].approval_role_infos[j].employee_infos.push({'employee_id':parseInt($(this).attr('employee_id'))});
                    })
                })
            })
            console.log(self.meta_sub_project_infos);

            return new Model("cowin_project.cowin_project")
                    .call("rpc_save_permission_configuration", [[self.id]],{meta_sub_project_infos:self.meta_sub_project_infos})
                    .then(function (result) {
                        console.log(result);
                        if(result.default_is_full){
                            if($('.no_perfect').length>0){
                                $('.no_perfect').remove()
                            }
                        }else {
                            if($('.no_perfect').length==0){
                                $("<span class='no_perfect'>未完善</span>").insertBefore($('.manage_team_btn .fa'));
                            }
                        }

                    })
        },
        //确定员工选择
        confirm_add_new_sels:function () {
            var self = this;
            var sel = [];
            var render_names = []
            $('.selectpicker option:selected').each(function () {
                sel.push(parseInt($(this).attr('data-id')));
            })
            var add_sel_node = $(".detail_lines_wrap[meta_sub_pro_id="+ self.add_meta_sub_pro_id +"] .detail_line[approval_role_id="+ self.add_approval_role_id +"] .team_role_names_wrap");
            $.each(sel,function (x,n) {
                $.each(self.employee_infos,function (y,v) {
                    if(n == v.employee_id){
                        render_names.push(v)
                    }
                })
            })
            $(add_sel_node).prepend(QWeb.render('names_tmpl', {result: render_names,is_admin:self.is_admin}));
            self.hide_add_new_sels();

        },
        //显示选择框
        show_add_new_sels:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            var self = this;
            self.add_approval_role_id = $(target).parents('.detail_line').attr('approval_role_id');
            self.add_meta_sub_pro_id = $(target).parents('.detail_lines_wrap').attr('meta_sub_pro_id');
            $('.add_new_wrap').show();
        },
        //关闭选择框
        hide_add_new_sels:function () {
             $('.add_new_wrap').hide();
             $('.copy_wrap').hide();
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

            //项目管理团队是否完善
            self.perfect = true;
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