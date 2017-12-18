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
        },
        start: function () {
            var self = this;
            return new Model("cowin_project.cowin_project")
                    .call("rpc_get_post_info", [parseInt(self.id)],{})
                    .then(function (result) {
                        console.log(result);

                        // self.id = parseInt(result.id);
                        self.$el.append(QWeb.render('follow_up_invest_detail_tmp', {result: result}))
                    })
        }
    });
    core.action_registry.add('follow_invest_kanban_to_detail', FollowInvestKanbanToDetail);

    return FollowInvestKanbanToDetail;
});