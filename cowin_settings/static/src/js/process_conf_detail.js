/**
 * Created by 123 on 2017/10/23.
 */
odoo.define('cowin_settings.process_conf_detail', function (require) {
    "use strict";

    var core = require('web.core');
    var Model = require('web.Model');
    var Widget = require('web.Widget');
    var View = require('web.View');
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
            'click .tache_parent':'show_tache_parent',
            'click .confirm_unlock_condition':'confirm_unlock_condition'
        },
        //确定解锁条件
        confirm_unlock_condition:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            var self = this;
            var tache_parent_id = $(".condition_wrap select").find("option:selected").attr('data-id');  //解锁条件
             new Model("cowin_settings.process")
                    .call("rpc_unlock_condition", [self.id], {tache_parent_id:tache_parent_id,tache_id:self.unlock_tache_id})
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
            $('.current_tache').html($(target).prev().html())
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
                    .call("rpc_create_tache", [self.id], {name:tache_name,stage_id:stage_id,description:tach_info,once_or_more:more})
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
            this._super.apply(this, arguments);
            this.id = parseInt(action.id);
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