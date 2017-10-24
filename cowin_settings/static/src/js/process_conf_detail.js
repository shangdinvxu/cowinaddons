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
            'click .new_group_button':'create_new_group_func',
            'click .alia_cancel':'close_create_wrap',
            'click .alia_confirm':'confirm_create_group'
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
                        $("#conf_detail_container").replaceWith(QWeb.render('process_conf_detail_tmp', {result: result}))
                    })
        },
        close_create_wrap:function () {
            $(".close_this_container").hide()
        },
        create_new_group_func:function () {
            console.log('ssssssss');
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