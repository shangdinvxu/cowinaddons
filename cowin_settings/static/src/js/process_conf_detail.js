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