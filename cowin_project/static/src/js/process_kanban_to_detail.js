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
            'click .process_add_fun':'process_add_fun',
            //  详情 tab
            'click .project_details':'project_details_func',
            'click .add_new_invest':'add_new_invest_func',
            'click .add_invest_foot .save':'save_add_invest',
            'click .add_invest_foot .cancel':'cancel_add_invest',
            'click .add_btn td':'add_exit_func',
            'change .add_invest_select select':'add_invest_select_change_func',
            'click .btn_wrap .delete':'delete_func',
            'click .btn_wrap .edit':'edit_func',
            'click .add_invest_foot .save_edit':'save_edit_func',
            'input .invest_exit_infos .the_amount_of_withdrawals':'calc_exit_inter',
            'input .invest_exit_infos .project_valuation':'calc_exit_inter',
            'click .tab_detail_view_item':'tab_detail_view_item_func',
            'click .exit_detail_content .close':'close_view_withdraw',
            'click .delete_value_item':'delete_value_item_func'
        },
        //编辑投资里删除退出详情
        delete_value_item_func:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            var self = this;
            $(target).parents('tr').hide();
        },
        close_view_withdraw:function () {
            $('.tab_detail_view_withdraw_wrap').hide();
        },
        //查看退出情况
        tab_detail_view_item_func:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            var self = this;
            var index = $(target).parents('tr').attr('item-index');
            $('.tab_detail_view_withdraw_wrap').show();
            $('.tab_detail_view_withdraw_wrap').find('.exit_detail_content').find('tbody').html('');
            $('.tab_detail_view_withdraw_wrap').find('.exit_detail_content').find('tbody').append(QWeb.render('view_withdraw_tmpl',{result: self.tab_detail_infos[parseFloat(index)]}));
        },
        //计算退出比例
        calc_exit_inter:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            var x = $(target).parents('tr').find('.the_amount_of_withdrawals').val();
            var y = $(target).parents('tr').find('.project_valuation').val();
            var z = parseFloat(x)/parseFloat(y);
            $(target).parents('tr').find('.ownership_interest').val(Number(z*100).toFixed(2) + '%');
        },
        //详情页面编辑的保存
        save_edit_func:function () {
            var self = this;
            var back_datas = {
                'foundation_id': parseInt(self.edit_foundation_id),
                'the_amount_of_investment': $('.add_content .the_amount_of_investment').val(),
                'foundation':$('.add_content .foundation').val()
            };
            back_datas['withdrawal_ids'] = [];
            $('.invest_exit_infos .value_info').each(function (index) {
                if($(this).find('.ownership_interest').val() && $(this).find('.the_amount_of_withdrawals').val() && $(this).find('.project_valuation').val()){
                    if($(this).css('display') == 'none'){
                        var op_id = parseInt($(this).attr('data-id'));
                        var op_type = 2;  //删除
                    }else if($(this).attr('data-id')=='false'){
                        var op_type = 0;   //新增
                        var op_id = 0;
                    }else {
                        var op_type = 1;  //修改
                        var op_id = parseInt($(this).attr('data-id'));
                    }
                    var interest = (parseFloat($(this).find('.ownership_interest').val().replace("%",""))/100).toFixed(4);
                    // var interest = $(this).find('.ownership_interest').val().replace("%","")/100;
                    back_datas['withdrawal_ids'].push([op_type, op_id,{
                         'ownership_interest': interest,
                         'the_amount_of_withdrawals': $(this).find('.the_amount_of_withdrawals').val() ? parseInt($(this).find('.the_amount_of_withdrawals').val()) : null,
                         'project_valuation': $(this).find('.project_valuation').val() ? parseInt($(this).find('.project_valuation').val()):null,
                         'id': parseInt($(this).attr('data-id'))
                     }])
                }
            });
            console.log(back_datas)
            new Model("cowin_project.cowin_project")
                        .call("rpc_update_detail_info", [self.id],{vals:back_datas})
                        .then(function (result) {
                            console.log(result);

                            self.tab_detail_infos = [];
                            //获取详情页数据存到全局
                            result.forEach(function (value) {
                                value.data.forEach(function (data) {
                                    self.tab_detail_infos.push(data.withdrawals)
                                });
                            });
                            console.log(self.tab_detail_infos);

                            $("#process_detail").html('');
                            $("#process_detail").append(QWeb.render('process_deatil_tmpl', {result: result}))
                        })
        },
        //详情页面 编辑按钮
        edit_func:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            $('.add_external_invest_wrap').show();
            $('.add_content .add_header').html('编辑投资');

            var self = this;
            var index = $(target).parents('tr').attr('item-index');
            self.edit_foundation_id = $(target).parents('tr').attr('foundation-id');

            data = [{
                'id':null,
                'name':$(target).parents('tr').prev().find('td').html()
            }];
            // console.log(data);
            $('.add_invest_select').html('');
            $('.add_invest_select').append(QWeb.render('add_invest_select_tmpl',{result:data}));
            $('.add_invest_select select').prop('disabled',true);
            $('.invest_infos_item .foundation').val($(target).parents('tr').find('.foundation').text());
            $('.invest_infos_item .the_amount_of_financing').val($(target).parents('tr').find('.the_amount_of_financing').text());
            $('.invest_infos_item .the_amount_of_financing').prop('disabled',true);
            $('.invest_infos_item .the_amount_of_investment').val($(target).parents('tr').find('.the_amount_of_investment').text());
            $('.invest_infos_item .project_valuation').val($(target).parents('tr').find('.project_valuation').text());
            $('.invest_infos_item .project_valuation').prop('disabled',true);

            $('.add_invest_foot .save').addClass('save_edit').removeClass('save');
            console.log(self.tab_detail_infos[parseInt(index)]);
            $('.invest_exit_infos tbody').html('');
            $('.invest_exit_infos tbody').append(QWeb.render('withdraw_infos_tmpl', {result: self.tab_detail_infos[parseInt(index)],add:false}))
        },
        //详情页tab  删除
        delete_func:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            var self = this;
            var foundation_id = $(target).parents('tr').attr('foundation-id');

            Dialog.confirm(this, _t("确定删除这条数据?"), {
                confirm_callback: function() {
                    new Model("cowin_project.cowin_project")
                        .call("rpc_delete_foundation_infos", [self.id],{vals:{'foundation_id':parseInt(foundation_id)}})
                        .then(function (result) {
                            console.log(result);

                            self.tab_detail_infos = [];
                            //获取详情页数据存到全局
                            result.forEach(function (value) {
                                value.data.forEach(function (data) {
                                    self.tab_detail_infos.push(data.withdrawals)
                                });
                            });
                            console.log(self.tab_detail_infos);

                            $("#process_detail").html('');
                            $("#process_detail").append(QWeb.render('process_deatil_tmpl', {result: result}))
                        })
                },
            });
        },
        //详情页添加外部投资选择轮次的change事件
        add_invest_select_change_func:function () {
            var self = this;
            var round_financing_id = parseInt($('.add_invest_select option:selected').attr('data-id'));

            new Model("cowin_project.cowin_project")
                    .call("rpc_get_financing_infos", [self.id],{vals:{'round_financing_id':round_financing_id}})
                    .then(function (result) {
                        if(result.id && result.name){
                            $('.invest_infos .the_amount_of_financing').prop('disabled',true);
                            $('.invest_infos .project_valuation').prop('disabled',true);
                        }else {
                            $('.invest_infos .the_amount_of_financing').prop('disabled',false);
                            $('.invest_infos .project_valuation').prop('disabled',false);
                        }

                        $('.invest_infos .the_amount_of_financing').val(result.id);
                        $('.invest_infos .project_valuation').val(result.name);
                    })
        },
        //添加退出情况
        add_exit_func:function () {
            $('.invest_exit_infos tbody tr').eq(0).clone(true).insertBefore($('.add_btn'));
            $('.add_btn').prev().find('input').val('');
            $('.add_btn').prev().attr('data-id',false);
        },
        //取消新增投资
        cancel_add_invest:function () {
            $('.add_external_invest_wrap').hide();
        },
        //保存新增投资
        save_add_invest:function () {
            var self = this;
            var data = {};
            data['project_id'] = self.id;
            data['round_financing_id'] = $('.add_invest_select option:selected').attr('data-id');
            data['foundation'] = $('.invest_infos_item .foundation').val();
            data['the_amount_of_investment'] = $('.invest_infos_item .the_amount_of_investment').val();
            data['the_amount_of_financing'] = $('.invest_infos_item .the_amount_of_financing').val();
            data['project_valuation'] = $('.invest_infos_item .project_valuation').val();
            data['withdrawals'] = [];
            $('.invest_exit_infos .value_info').each(function (index) {
                if($(this).find('.ownership_interest').val() && $(this).find('.the_amount_of_withdrawals').val() && $(this).find('.project_valuation').val()){
                    //百分数转成四位小数
                    var interest = (parseFloat($(this).find('.ownership_interest').val().replace("%",""))/100).toFixed(4);
                    data['withdrawals'].push({
                         'ownership_interest': interest,
                         'the_amount_of_withdrawals': $(this).find('.the_amount_of_withdrawals').val() ? parseInt($(this).find('.the_amount_of_withdrawals').val()) : null,
                         'project_valuation': $(this).find('.project_valuation').val() ? parseInt($(this).find('.project_valuation').val()):null
                     })
                }
            });

            console.log(data);
            if($('.invest_infos_item .foundation').val() == '' || $('.invest_infos_item .the_amount_of_financing').val() == '' || $('.invest_infos_item .the_amount_of_investment').val() == '' || $('.invest_infos_item .project_valuation').val() == ''){
                Dialog.alert(self, _t("警告！"), {
                    title: _t('请完善数据！'),
                });
            }else {
                new Model("cowin_project.cowin_project")
                    .call("rpc_create_detail_info", [self.id],{vals:data})
                    .then(function (result) {
                        self.tab_detail_infos = [];
                        //获取详情页数据存到全局
                        result.forEach(function (value) {
                            value.data.forEach(function (data) {
                                self.tab_detail_infos.push(data.withdrawals)
                            });
                        });
                        console.log(self.tab_detail_infos);

                        $("#process_detail").html('');
                        $("#process_detail").append(QWeb.render('process_deatil_tmpl', {result: result}))
                    })
            }
        },
        //新增外部投资
        add_new_invest_func:function () {
            var self = this;
            $('.add_invest_foot span').eq(0).addClass('save').removeClass('save_edit');
            new Model("cowin_project.cowin_project")
                    .call("rpc_get_financing", [[]])
                    .then(function (result) {
                        console.log(result);
                        $('.add_external_invest_wrap input').val('');

                        $('.add_invest_select').html('');
                        $('.add_invest_select').append(QWeb.render('add_invest_select_tmpl',{result:result}));
                        $('.add_content .invest_exit_infos tbody').html('');
                        $('.add_content .invest_exit_infos tbody').append(QWeb.render('withdraw_infos_tmpl',{result:[],add:true}));

                        //获取轮次带出的信息
                        new Model("cowin_project.cowin_project")
                            .call("rpc_get_financing_infos", [self.id],{vals:{'round_financing_id':result[0].id}})
                            .then(function (result) {
                                if(result.id && result.name){
                                    $('.invest_infos_item .the_amount_of_financing').prop('disabled',true);
                                    $('.invest_infos_item .project_valuation').prop('disabled',true);
                                }else {
                                    $('.invest_infos_item .the_amount_of_financing').prop('disabled',false);
                                    $('.invest_infos_item .project_valuation').prop('disabled',false);
                                }
                                $('.invest_infos_item .the_amount_of_financing').val(result.id);
                                $('.invest_infos_item .project_valuation').val(result.name);
                            });
                        $('.add_external_invest_wrap').show();
                        $('.add_content .add_header').html('新增投资')
                    })
        },
        //tab 详情
        project_details_func:function () {
            var self = this;
            new Model("cowin_project.cowin_project")
                    .call("rpc_get_detail_info", [parseInt(self.id)])
                    .then(function (result) {
                        console.log(result);

                        //获取详情页数据存到全局
                        result.forEach(function (value) {
                            value.data.forEach(function (data) {
                                self.tab_detail_infos.push(data.withdrawals)
                            });
                        });
                        console.log(self.tab_detail_infos);

                        $("#process_detail").html('');
                        $("#process_detail").append(QWeb.render('process_deatil_tmpl', {result: result}))
                    })
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
                    .call("rpc_copy_all_permission_configuration",[[self.id]], {'current_meta_sub_pro_id': self.current_meta_sub_pro_id})
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
                        if($(this).attr('weiyuan')){
                            self.meta_sub_project_infos[i].investment_decision_committee_scope_id = parseInt($(this).attr('weiyuan'))
                        }else {
                            self.meta_sub_project_infos[i].investment_decision_committee_scope_id = null;
                        }
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
            var render_names = [];
            var weiyuan_id;
            $('.selectpicker option:selected').each(function () {
                if($(this).hasClass('weiyuan')){
                    var weiyuan = $(this).attr('data-id').split(', ');
                    weiyuan_id = parseInt($(this).attr('data-scope-id'));
                    sel = weiyuan
                }else {
                    sel.push(parseInt($(this).attr('data-id')));
                }
            })
            var add_sel_node = $(".manage_team_edit_wrap .detail_lines_wrap[meta_sub_pro_id="+ self.add_meta_sub_pro_id +"] .detail_line[approval_role_id="+ self.add_approval_role_id +"] .team_role_names_wrap");
            $.each(sel,function (x,n) {
                $.each(self.employee_infos,function (y,v) {
                    if(n == v.employee_id){
                        render_names.push(v)
                    }
                })
            })
            $(add_sel_node).prepend(QWeb.render('names_tmpl', {result: render_names,is_admin:self.is_admin,edit:true,weiyuan: weiyuan_id,is_readonly:false}));
            self.hide_add_new_sels();

        },
        //显示选择框
        show_add_new_sels:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            var self = this;
            self.add_approval_role_id = $(target).parents('.detail_line').attr('approval_role_id');
            self.add_meta_sub_pro_id = $(target).parents('.detail_lines_wrap').attr('meta_sub_pro_id');



            //判断是否是要单独请求方法获取选择的人员
            if($(target).parents('.detail_line').attr('need_call_rpc')!='false'){
                new Model("cowin_project.cowin_project")
                    .call($(target).parents('.detail_line').attr('need_call_rpc'), [[self.id]])
                    .then(function (result) {
                        console.log(result);
                        $('.add_new_wrap .add_new_body').html('');

                        //type=1表示投资决策委员会
                        if($(target).parents('.detail_line').attr('need_call_rpc')=='rpc_get_investment_decision_committee_infos'){
                            $('.add_new_wrap .add_new_body').append(QWeb.render('add_new_objs', {result: result,type: 1}));
                        }else {
                            $('.add_new_wrap .add_new_body').append(QWeb.render('add_new_objs', {result: result,type: 2}));
                        }
                    })
            }
            else {
                $('.add_new_wrap .add_new_body').html('');
                $('.add_new_wrap .add_new_body').append(QWeb.render('add_new_objs', {result: self.employee_infos,type: 3}));
            }


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

            // console.log($(target).parents('.post_investment'));
            if($(target).parents('.post_investment').length==0){
                var method = 'rpc_get_info';
            }else {
                var method = 'rpc_get_post_info';
            }

            return new Model("cowin_project.cowin_project")
                    .call(method, [parseInt(self.id)],{meta_project_id:parseInt(sub_id)})
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
            // if(launch_again == 'true'){
            //     var action = {
            //         name: "详细",
            //         type: 'ir.actions.act_window',
            //         res_model: self.tache_arr[tache_index].model_name,
            //         view_type: 'form',
            //         res_id: self.tache_arr[tache_index].res_id,
            //         view_mode: 'form',
            //         views: [[false, 'form']],
            //         target: "current",
            //         flags: {'initial_mode': 'edit'},
            //         context:{'is_launch_again':self.tache_arr[tache_index].is_launch_again}
            //     };
            //     this.do_action(action);
            // }else {

                // var action = {
                //     name: "详细",
                //     type: 'ir.actions.act_window',
                //     res_model: self.tache_arr[tache_index].model_name,
                //     view_type: 'form',
                //     res_id: self.tache_arr[tache_index].res_id,
                //     view_mode: 'form',
                //     views: [[false, 'form']],
                //     target: "current",
                //     flags: {'initial_mode': 'edit'},
                //     context:{'is_launch_again':self.tache_arr[tache_index].is_launch_again}
                // };
                // 测试
                new Model("cowin_project.cowin_project")
                        .call("rpc_load_and_return_action", [parseInt(self.id)],{'tache_info':self.tache_arr[tache_index]})
                        .then(function (result) {
                            result.context['tache'] = self.tache_arr[tache_index];
                            result.target = 'current';
                            console.log(result);
                            result.flags = {'initial_mode': 'edit'};
                            result.context.is_launch_again = self.tache_arr[tache_index].is_launch_again;
                            self.do_action(result);
                        })
            // }

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

            //存储详情页数据
            self.tab_detail_infos = [];

            //项目管理团队是否完善
            self.perfect = true;

            this.action = action;
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