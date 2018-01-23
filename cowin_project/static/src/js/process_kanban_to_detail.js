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
            'click .cancel_project_team_setting':'cancel_project_team_setting_func',
            'click .member_name .fa':'del_member_func',
            'click .copy_this_setting':'get_all_settings',
            'click .confirm_copy':'confirm_copy_func',
            'click .button_wrap .add_new_tache':'add_new_tache_func',
            'click .operate_records':'operate_records_func',
            'click .manage_team_edit':'manage_team_edit_func',
            'click .operate_contacts':'show_operate_contacts',
            'click .process_add_fun':'process_add_fun'
        },
         //新增基金
        process_add_fun:function () {
            var self = this;

            //测试
            new Model("cowin_project.cowin_project")
                    .call("rpc_new_found_round_entity", [parseInt(self.id)],{'data_version':self.data_version})
                    .then(function (result) {
                        // result.context['tache'] = self.tache_arr[1];
                        result.target = 'current';
                        // result.res_id = false;
                        console.log(result);
                        self.do_action(result);
                    })
        },
        //联系人
        show_operate_contacts:function () {
            var self = this;
            return new Model("cowin_project.cowin_project")
                    .call("rpc_get_contract_info",[self.id])
                    .then(function (result) {
                        console.log(result);
                        $('#process_contact').html('');
                        $('#process_contact').append(QWeb.render('operate_contacts_templ', {result: result}))
                    })
        },
        //编辑项目管理团队
        manage_team_edit_func:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            var self = this;
            var show_meta_sub_pro_id = $(target).parents('.header_line').attr('meta_sub_pro_id');
            $('.manage_team_edit_wrap').remove();
            $('#process_data .process_data_main_wrap').append(QWeb.render('manage_team_edit_page', {result: self.manage_team_data,edit:true}));
            $('.manage_team_edit_wrap .add_new_content .header_line').hide();
            $('.manage_team_edit_wrap .add_new_content .detail_lines_wrap').hide();
            $('.manage_team_edit_wrap div[meta_sub_pro_id='+ parseInt(show_meta_sub_pro_id) +']').show()
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
        //环节增加
        add_new_tache_func:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            var self = this;
            var tache_index = $(target).parents('.detail_line').attr('tache-index');
            if(self.tache_arr[tache_index].model_name=="cowin_project.sub_invest_decision_app"){
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
                        .call("rpc_new_tache_prev",[[self.id]],data)
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
                        $('.manage_team_edit_wrap .add_new_content').html('');
                        $('.manage_team_edit_wrap .add_new_content').append(QWeb.render('project_manage_team_tmp', {result: result,edit:true}));
                        $('.copy_wrap').remove();
                        $('.manage_team_edit_wrap .add_new_content .header_line').hide();
                        $('.manage_team_edit_wrap .add_new_content .detail_lines_wrap').hide();
                        $('.manage_team_edit_wrap div[meta_sub_pro_id='+ parseInt(self.current_meta_sub_pro_id) +']').show();
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

        //取消项目管理团队编辑设置
        cancel_project_team_setting_func:function () {
            $('.manage_team_edit_wrap').remove();
        },
        //保存项目管理团队设置
        confirm_project_team_setting_func:function () {
            var self = this;
            $('.manage_team_edit_wrap .detail_lines_wrap').each(function (i) {
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
                        self.manage_team_data = result;
                        self.employee_infos = result.employee_infos;
                        self.is_admin = result.is_admin;
                        self.meta_sub_project_infos = result.meta_sub_project_infos;

                        if(result.default_is_full){
                            if($('.no_perfect').length>0){
                                $('.no_perfect').remove()
                            }
                        }else {
                            if($('.no_perfect').length==0){
                                $("<span class='no_perfect'>未完善</span>").insertBefore($('.manage_team_btn .fa'));
                            }
                        }
                        $('.process_data_main_wrap').html('');
                        $('.process_data_main_wrap').append(QWeb.render('project_manage_team_tmp', {result: result}));
                        Dialog.confirm(this, _t("保存成功"), {});
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
            var add_sel_node = $(".manage_team_edit_wrap .detail_lines_wrap[meta_sub_pro_id="+ self.add_meta_sub_pro_id +"] .detail_line[approval_role_id="+ self.add_approval_role_id +"] .team_role_names_wrap");
            $.each(sel,function (x,n) {
                $.each(self.employee_infos,function (y,v) {
                    if(n == v.employee_id){
                        render_names.push(v)
                    }
                })
            })
            $(add_sel_node).prepend(QWeb.render('names_tmpl', {result: render_names,is_admin:self.is_admin,edit:true}));
            self.hide_add_new_sels();

        },
        //显示选择框
        show_add_new_sels:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            var self = this;
            self.add_approval_role_id = $(target).parents('.detail_line').attr('approval_role_id');
            self.add_meta_sub_pro_id = $(target).parents('.detail_lines_wrap').attr('meta_sub_pro_id');

            $('.add_new_body option').each(function () {
               $(this)[0].selected = false;
            });
            $('.add_new_body .dropdown-menu li').each(function () {
                $(this).attr('class','');
            });
            $('.add_new_body .filter-option').html('');

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
                        self.manage_team_data = result;
                        self.employee_infos = result.employee_infos;
                        self.is_admin = result.is_admin;
                        self.meta_sub_project_infos = result.meta_sub_project_infos;

                        $('.process_data_main_wrap').html('');
                        $('.process_data_main_wrap').append(QWeb.render('project_manage_team_tmp', {result: result,edit:false}))
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
                        result.no_initate = self.no_initate
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


            new Model("cowin_project.cowin_project")
                        .call("rpc_approval_view_action_action", [parseInt(self.id)],{'tache_info':self.tache_arr[tache_index]})
                        .then(function (result) {
                            console.log(result)
                            self.do_action(result);
                        })


            // var context ={
            //         'tache': self.tache_arr[tache_index],
            //     };
            // if(self.tache_arr[tache_index].round_financing_and_foundation){
            //     context = {
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
            //     }
            // }
            //
            // var action = {
            //     view_type: 'form',
            //     view_mode: 'form',
            //     views: [[false, 'form']],
            //     res_model: self.tache_arr[parseInt(tache_index)].model_name,
            //     res_id: self.tache_arr[tache_index].res_id,
            //     name: self.tache_arr[tache_index].name,
            //     type: 'ir.actions.act_window',
            //     context: context,
            //     target:'current'
            // }
            // self.do_action(action)
        },
        //发起按钮的点击事件
        initiate_func:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            //是否重新发起
            if($(target).hasClass('initiate')){
                var launch_again = $(target).attr('again');
            }else {
                var launch_again = $(target).parents('.initiate').attr('again');
            }

            var tache_index = $(target).parents('.process_data_item_line').attr('tache-index');
            var tache_id = parseInt($(target).parents('.process_data_item_line').attr('data-tache-id'));
            var self = this;
            self.tache_arr[tache_index].project_id = self.id;
            self.tache_arr[tache_index].tache_id = tache_id;

            //重新发起走另外的方法
            if(launch_again == 'true'){
                var action = {
                    name: "详细",
                    type: 'ir.actions.act_window',
                    res_model: self.tache_arr[tache_index].model_name,
                    view_type: 'form',
                    res_id: self.tache_arr[tache_index].res_id,
                    view_mode: 'form',
                    views: [[false, 'form']],
                    target: "current",
                    flags: {'initial_mode': 'edit'},
                };
                this.do_action(action);
            }else {
                // 测试
                new Model("cowin_project.cowin_project")
                        .call("rpc_load_and_return_action", [parseInt(self.id)],{'tache_info':self.tache_arr[tache_index]})
                        .then(function (result) {
                            result.context['tache'] = self.tache_arr[tache_index];
                            result.target = 'current';
                            console.log(result);
                            self.do_action(result);
                        })
            }

        },

        init: function (parent, action, options) {
            this._super(parent);
            this._super.apply(this, arguments);
            options = options || {};
            this.context = options.context || {};

            //项目查询界面的判断，没有发起按钮
            this.no_initate = action.params.no_initate;

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
                        result.no_initate = self.no_initate
                        console.log(result);
                        self.pagedata = result;

                        self.data_version = result.data_version;

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