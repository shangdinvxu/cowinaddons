/**
 * Created by 123 on 2018/3/20.
 */

odoo.define('cowin_plugin.test', function (require) {
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

    var Test = Widget.extend({
        init:function (parent, action, options) {
             this._super(parent);
            this._super.apply(this, arguments);
            console.log(parent)
             console.log(action)
             console.log(options)
        },
        start: function () {
            var self = this;
            console.log(self);
            this.$el.append("<div>Are you sure you want to perform this action?</div>" +
                    "<button class='ok_button'>Ok</button>" +
                    "<button class='cancel_button'>Cancel</button>");
                this.$el.find("button.ok_button").click(function() {
                    self.trigger("user_choose", true);
                });
                this.$el.find("button.cancel_button").click(function() {
                    self.trigger("user_choose", false);
                });
        },
        user_choose:function () {
            alert('yes')
        },

    });

    core.action_registry.add('test', Test);

    return Test;
});