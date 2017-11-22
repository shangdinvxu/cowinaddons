/**
 * Created by 123 on 2017/10/23.
 */
odoo.define('cowin_settings.process_conf_detail', function (require) {
    "use strict";

    var core = require('web.core');
    var Model = require('web.Model');
    var Widget = require('web.Widget');
    var View = require('web.View');
    var framework = require('web.framework');
    var QWeb = core.qweb;
    var Dialog = require('web.Dialog');
    var ControlPanelMixin = require('web.ControlPanelMixin');
    var SearchView = require('web.SearchView');
    var data = require('web.data');
    var _t = core._t;

    var ProcessConfDetail = Widget.extend({
        events:{
            'click .new_group_button':'show_new_group_func',
            'click .alia_cancel':'close_create_wrap',
            'click .alia_confirm':'confirm_create_group',
            'click .new_link_button':'show_new_tache_func',
            'click .create_tache_confirm':'confirm_create_tache',
            'click .tache_delete':'delete_tache_func',
            'click .group_delete':'delete_group_func',
            'click .edit_tache':'show_tache_parent',
            'click .confirm_unlock_condition':'confirm_unlock_condition',
            'click .sort_group':'sort_group_show',
            'click .sort_group_save':'sort_group_save',
            'dragover tr':'prevent_default',
            'dragstart tr': 'move_start',
            'drop tr':'move_func',
            'click .cancel_sort':'cancel_sort',
            'click .approval_flow':'show_approval_flow_wrap',
            'click .approval_cancel':'close_approval_flow_wrap',
            'click .delete_node':'delete_node_func',
            'click .add_approval_node':'add_approval_node_func',
            'click .approval_save':'approval_save_func'
        },
        //保存审批流设置
        approval_save_func:function () {
            var self = this;
            var approval_data = {};
            var node_data = [];
            $('.node_operate_wrap').each(function (i) {
                // console.log($(this).find('.node_name').val());
                var s = {};
                s.approval_flow_settings_id = self.approval_flow_settings_id;
                s.name = $(this).find('.node_name').val();
                if($(this).attr('data-setting-node-id')){
                    s.approval_flow_setting_node_id = parseInt($(this).attr('data-setting-node-id'));
                }else {
                    s.approval_flow_setting_node_id = -1;   //值为-1表示次此节点是新增的，要传给后台写进数据库
                }
                if($(this).find('.approval_suspend').length>0){
                    s.put_off = $(this).find('.approval_suspend').is(':checked')
                }else {
                    s.put_off = false;
                }
                s.reject = true;
                s.accept = true;
                s.operation_role_ids = [];
                $(this).find('.selected').each(function (j) {
                    var role_name =$(this).text()
                    $.each(self.select_roles,function (x,value) {
                        if(role_name==value.name){
                            s.operation_role_ids.push(value.operator_role_id);
                        }
                    })
                });
                node_data.push(s);
            });
            node_data.push(self.approval_over);
            approval_data.approval_flow_setting_nodes = node_data
            console.log(approval_data);

            return new Model("cowin_settings.approval_flow_settings")
                .call("rpc_save_all_info",[self.approval_id],approval_data)
                .then(function (result) {
                    console.log(result);

                })
        },
        //添加审批节点
        add_approval_node_func:function () {
            var self = this;
            $('.approval_main_right').append(QWeb.render('add_approval_node_right',{result:self.select_roles}));
            $(QWeb.render('add_approval_node_left')).insertBefore($('.approval_setting_node_wrap:last'));
        },
        //删除审批节点
        delete_node_func:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            var self = this;
            var setting_node_id = $(target).parents('.node_operate_wrap').attr('data-setting-node-id');
            Dialog.confirm(this, _t("确定删除这条审批节点吗?"), {
                confirm_callback: function() {
                    var index = $(target).parents('.node_operate_wrap').index()
                    $(target).parents('.node_operate_wrap').remove();
                    $(".approval_setting_node_wrap:eq("+index+")").remove();

                },
            });
        },
        //关闭审批流页面
        close_approval_flow_wrap:function () {
            $('.approval_flow_container').remove();
        },
        //显示审批流
        show_approval_flow_wrap:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            var tache_id = $(target).parents('.process_detail_group_detail_line').attr('data-tache-id');
            var self = this;
            return new Model("cowin_settings.process")
                .call("rpc_approval_flow_setting_info",[self.id],{tache_id:tache_id})
                .then(function (result) {
                    console.log(result);
                    self.approval_flow_settings_id = result.approval_flow_settings_id;
                    $('.approval_flow_container').remove();

                    self.approval_id = result.approval_flow_settings_id;
                    self.select_roles = result.approval_flow_setting_node_ids[0].all_operator_roles_ids;   //存储所有角色
                    self.approval_over = result.approval_flow_setting_node_ids[result.approval_flow_setting_node_ids.length-1];   //存储审批结束的节点

                    self.$el.append(QWeb.render('approval_flow_tmpl',{result: result}));
                })
        },
        //取消排序
        cancel_sort:function () {
            var self = this;
            return new Model("cowin_settings.process")
                    .call("get_info", [self.id])
                    .then(function (result) {
                        self.$el.html('');
                        self.$el.append(QWeb.render('process_conf_detail_tmp', {result: result}));
                    })
        },
        //拖动开始时的操作
        move_start:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            if(target.nodeName == 'TD'){
                target = $(target).parents('tr');
            }
            this.move_group_id = parseInt($(target).attr('data-id'));
            this.move_group = $(target);
        },
        //拖动完成时的操作,把拖动的组及其下面的环节一起放到目标组下面
        move_func:function (e) {
            e.preventDefault();
            var self = this;
            var targetEle = e.target;    //松开鼠标释放节点时光标所在元素
            if($(targetEle).parents('tr').attr('data-id') == this.move_group_id || $(targetEle).parents('tr').attr('data-stage-id') == this.move_group_id){
                return
            }

            var target_group_id = $(targetEle).parents('tr').attr('data-id');
            var move_taches = $(".process_detail_group_detail_line[data-stage-id="+self.move_group_id+"]");
            $('.process_detail_group_detail_line[data-stage-id='+self.move_group_id+']').remove();
            self.move_group.remove();
            if($(".process_detail_group_detail_line[data-stage-id="+target_group_id+"]:last").length>0){
                var append_ele = $(".process_detail_group_detail_line[data-stage-id="+target_group_id+"]:last");
            }else {
                var append_ele = $(targetEle).parents('tr');
            }
            $(self.move_group).insertAfter(append_ele);
            $(move_taches).insertAfter(self.move_group);
        },
        prevent_default:function (ev) {
            ev.preventDefault(); //阻止向上冒泡
        },
        //保存排序分组
        sort_group_save:function () {
            var self = this;
            var json_data = {};
            $('.process_detail_group_line').each(function (index) {
                json_data[$(this).attr('data-id')] = index
            });
            framework.blockUI();
            new Model("cowin_settings.process")
                    .call("rpc_save_order_by_stage", [self.id],{show_status:json_data})
                    .then(function (result) {
                        console.log(result);
                        $('.create_new_tache').hide();
                        self.$el.html('');
                        self.$el.append(QWeb.render('process_conf_detail_tmp', {result: result}));
                        $('.drag_show').hide();
                        $('.sort_group_save .sort_state').html('排序');
                        $('.sort_group_save').addClass('sort_group');
                        $('.sort_group_save').removeClass('sort_group_save');
                        framework.unblockUI();
                    })
        },
        sort_group_show:function () {
            $('.drag_show').show();
            $('.sort_group .sort_state').html('保存');
            $('.sort_group').addClass('sort_group_save');
            $('.sort_group').removeClass('sort_group');
            $('.process_detail_group_line').attr('draggable','true');
            $('.cancel_sort').css('display','inline-block');
        },
        //确定环节编辑
        confirm_unlock_condition:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            var self = this;
            var edit_tache_name = $('.current_tache').val();

            var stage_id = $(".edit_tache_input_wrap select").find("option:selected").attr('data-id');

            var edit_tache_descs = $('.edit_tache_desc textarea').val();
            var tache_parent_id = $(".condition_wrap select").find("option:selected").attr('data-id');  //解锁条件
             new Model("cowin_settings.process")
                    .call("rpc_edit_tache", [self.id], {stage_id:parseInt(stage_id),tache_parent_id:parseInt(tache_parent_id),tache_id:parseInt(self.unlock_tache_id),tache_name:edit_tache_name,description:edit_tache_descs})
                    .then(function (result) {
                        console.log(result);
                        $('.create_new_tache').hide();
                        self.$el.html('');
                        self.$el.append(QWeb.render('process_conf_detail_tmp', {result: result}));
                    })
        },
        show_tache_parent:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            var self = this;
            $('.unlock_condition').show();
            $('.current_tache').val($(target).parents('.operate_wrap').prevAll('.tache_name').html());
            $('.condition_wrap option').each(function () {
                $(this)[0].selected =  false
                if($(this).html() == $(target).parents('.operate_wrap').prevAll('.tache_parent').html()){
                    $(this)[0].selected = true
                }
            });
            $('.edit_tache_desc textarea').val($(target).parents('.operate_wrap').prevAll('.tache_description').html());
            self.unlock_tache_id = $(target).parents('tr').attr('data-tache-id')
        },
        delete_group_func:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            var self = this;
            var del_group_id = $(target).parents('tr').attr('data-id');
            Dialog.confirm(this, _t("确定删除这条分组吗?"), {
                confirm_callback: function() {
                    new Model("cowin_settings.process")
                        .call("rpc_delete_group", [self.id], {stage_id:del_group_id})
                        .then(function (result) {
                            console.log(result);
                            $('.create_new_tache').hide();
                            self.$el.html('');
                            self.$el.append(QWeb.render('process_conf_detail_tmp', {result: result}));
                        })
                },
            });
        },
        //删除环节
        delete_tache_func:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            var self = this;
            var del_tache_id = $(target).parents('tr').attr('data-tache-id');
            Dialog.confirm(this, _t("确定删除这条环节吗?"), {
                confirm_callback: function() {
                    new Model("cowin_settings.process")
                        .call("rpc_delete_tache", [self.id], {tache_id:del_tache_id})
                        .then(function (result) {
                            console.log(result);
                            $('.create_new_tache').hide();
                            self.$el.html('');
                            self.$el.append(QWeb.render('process_conf_detail_tmp', {result: result}));
                        })
                },
            });
        },
        //新建环节
        confirm_create_tache:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            var self = this;
            var stage_id = $(".create_input_wrap select").find("option:selected").attr('data-id');
            var tache_name = $(".new_tache_name").val();
            var tach_info = $(".tache_info textarea").val();
            if($('.tache_chose_times input').prop('checked')){
                 var more = true;
            }else {
                var more = false;
            }
             new Model("cowin_settings.process")
                    .call("rpc_create_tache", [self.id], {name:tache_name,stage_id:parseInt(stage_id),description:tach_info,once_or_more:more})
                    .then(function (result) {
                        console.log(result);
                        $('.create_new_tache').hide();
                        self.$el.html('');
                        self.$el.append(QWeb.render('process_conf_detail_tmp', {result: result}));
                    })
        },
        show_new_tache_func:function () {
            $('.create_new_tache').show()
        },
        //新建分组
        confirm_create_group:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            var self = this;
            if($('.create_group_input').val().length==0){
                Dialog.alert(target, "分组名不能为空！");
                return;
            }
            new Model("cowin_settings.process")
                    .call("rpc_create_group", [self.id], {name:$('.create_group_input').val(),process_id:self.id})
                    .then(function (result) {
                        console.log(result);
                        $('.create_new_group').hide();
                        self.$el.html('');
                        self.$el.append(QWeb.render('process_conf_detail_tmp', {result: result}));
                    })
        },
        close_create_wrap:function () {
            $(".close_this_container").hide()
        },
        show_new_group_func:function () {
            $(".create_new_group").show();
        },
        init: function (parent, action) {
            this._super(parent);
            this._super.apply(this, arguments);
            if(action.active_id){
                this.id = parseInt(action.active_id);
            }else {
                this.id = parseInt(action.params.active_id);
            }

            var self = this;
        },
        start: function () {
            var self = this;
            return new Model("cowin_settings.process")
                    .call("get_info", [this.id])
                    .then(function (result) {
                        console.log(result);
                        self.$el.append(QWeb.render('process_conf_detail_tmp', {result: result}))
                    })
        }
    });
    core.action_registry.add('process_conf_detail', ProcessConfDetail);

    return ProcessConfDetail;
});