/**
 * Created by 123 on 2018/3/20.
 */

odoo.define('cowin_foundation.foundation_info', function (require) {
    "use strict";

    var core = require('web.core');
    var Model = require('web.Model');
    var Widget = require('web.Widget');
    var View = require('web.View');
    var QWeb = core.qweb;
    var ControlPanelMixin = require('web.ControlPanelMixin');
    var ControlPanel = require('web.ControlPanel');
    var Dialog = require('web.Dialog');
    var ActionManager = require('web.ActionManager');
    var SearchView = require('web.SearchView');
    var data = require('web.data');
    var pyeval = require('web.pyeval');
    var _t = core._t;

    var FoundationInfo = Widget.extend({
        events:{
            'click .edit_foundation':'edit_foundation_func',
            'click #foundation_tab .list_of_contributors':'list_of_contributors_func',
            'click .add_new_contributor':'add_new_contributor_func',
            'click .edit_list':'edit_list_func'
        },
        //编辑出资人
        edit_list_func:function (e) {
            var e = e || window.event;
            var target = e.target || e.srcElement;
            var self = this;
            var index = $(target).parents('tr').attr('data-index');
            var action = {
                'name': '编辑出资人',
                'view_type': 'form',
                'view_mode': 'form',
                'views': [[false, 'form']],
                'res_model': 'cowin_foudation.sponsor',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'res_id': parseInt(self.sponsor_info[parseInt(index)].id)
            };
            var options = {
                on_close: function () {
                    self.list_of_contributors_func();
                }
            };
            this.do_action(action, options);
        },
        //新增出资人
        add_new_contributor_func:function () {
            var self = this;
            var action = {
                'name': '新增出资人',
                'view_type': 'form',
                'view_mode': 'form',
                'views': [[false, 'form']],
                'res_model': 'cowin_foudation.sponsor',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'context':{'default_foundation_id': self.id},
            };
            var options = {
                on_close: function () {
                    self.list_of_contributors_func();
                }
            };
            this.do_action(action, options);
        },
        //出资人列表tab显示
        list_of_contributors_func: function () {
            var self = this;
            new Model("cowin_foundation.cowin_foundation")
                    .call("rpc_get_sponsor_info", [parseInt(self.id)],{})
                    .then(function (result){
                        console.log(result);
                        //保存出资人信息到全局
                        self.sponsor_info = result.sponsor_info;
                        $('#list_of_contributors').html('');
                        $('#list_of_contributors').append(QWeb.render('list_of_contributors_templ',{result:result.sponsor_info}));

                        //用bootstrap table 插件显示表格
                        var columns = [
                            {
                                title:'',
                                formatter: function (value, row, index) {
                                    return index+1;
                                }
                            },{
                                field: 'name',
                                title: '出资人名称',
                            },{
                                field: 'registered_address',
                                title: '注册地址',
                            },{
                                field: 'capital_contribution',
                                title: '出资金额（万元）',
                            },{
                                field: 'capital_ratio',
                                title: '出资比例',
                            },{
                                field: 'amount_of_payment',
                                title: '实缴金额（万元）',
                            },{
                                field: 'amount_of_payment_ratio',
                                title: '实缴比例',
                            },{
                                field: 'the_nature_of_the_investor',
                                title: '出资人性质',
                            },{
                                field: 'institutional_investor',
                                title: '是否投资机构',
                                formatter: function (value) {
                                    if(value==1) return '是'
                                    else return '否'
                                }
                            },{
                                field: 'mailing_address_of_shareholders',
                                title: '股东邮寄地址',
                            },{
                                field: 'contract_person',
                                title: '联系人',
                            },{
                                field: 'contract_phone',
                                title: '联系电话',
                            },{
                                field: 'ID_number',
                                title: '证件号码',
                            },{
                                field: 'contract_email',
                                title: '邮箱',
                            },{
                                field: '',
                                title: '操作',
                                formatter: function () {
                                    return '<span class="edit_list">编辑</span>'
                                }
                            }
                        ];
                        $('#list_of_contributors #table').bootstrapTable({
                            columns:columns,
                            data:result.sponsor_info,
                        });
                    });
        },
        //基金情况表编辑
        edit_foundation_func:function () {
            var action = {
                'name': '基金',
                'view_type': 'form',
                'view_mode': 'form',
                'views': [[false, 'form']],
                'res_id': this.id,
                'res_model': 'cowin_foundation.cowin_foundation',
                'type': 'ir.actions.act_window',
                'target': 'current',
            };
            this.do_action(action);
        },

        on_attach_callback: function() {
            console.log('yfei');

        },

        on_detach_callback: function() {
            console.log('离开页面');
        },

        do_push_state: function(state) {
            this._super(state);
        },

        init: function (parent, action, options) {
            this._super(parent);
            this._super.apply(this, arguments);
            options = options || {};
            this.context = options.context || {};

            if(action.active_id){
                //基金的id
                this.id = action.active_id;
            }else {
                this.id = action.params.active_id;
            }

            this.action = action;
        },
        start: function () {
            var self = this;
            var defered = new Model("cowin_foundation.cowin_foundation")
                    .call("rpc_get_foundation_info", [parseInt(self.id)],{})
                    .then(function (result){
                        console.log(result);
                        self.$el.html('');
                        self.$el.append(QWeb.render('foundation_info_templ', {result: result.foundation_info}))
                    });
            return defered
        },

    });

    core.action_registry.add('foundation_info', FoundationInfo);

    return FoundationInfo;
});