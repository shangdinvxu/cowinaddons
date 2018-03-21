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
    var ActionManager = require('web.ActionManager')
    var SearchView = require('web.SearchView');
    var data = require('web.data');
    var pyeval = require('web.pyeval');
    var _t = core._t;

    var FoundationInfo = Widget.extend({
        init: function (parent, action, options) {
            this._super(parent);
            this._super.apply(this, arguments);
            options = options || {};
            this.context = options.context || {};

            if(action.active_id){
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

                        self.$el.append(QWeb.render('foundation_info_templ', {result: result.foundation_info}))
                    });
            return defered
        },
        on_detach_callback: function() {
            console.log('离开页面')
        },

    });

    core.action_registry.add('foundation_info', FoundationInfo);

    return FoundationInfo;
});