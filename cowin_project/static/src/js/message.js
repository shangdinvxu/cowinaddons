/**
 * Created by 123 on 2018/2/2.
 */
odoo.define('cowin_project.message_me_view_js', function (require) {

    "use strict";
    var core = require('web.core');
    var Model = require('web.Model');
    var Widget = require('web.Widget');


    var QWeb = core.qweb;
    var _t = core._t;

    var MessageList = Widget.extend({
        // template: "MessageMeView",
        events: {
            // 'click span.lead_update_submit': 'update_lead',
            // 'click span.lead_back_click': 'lead_back_fn',
            // 'click .show_time_begin': 'show_time_view',
            // 'click input.brand_check': 'on_click_version',
        },

        init: function (parent, action) {
            this._super.apply(this, arguments);
            var self = this;


        },
        start: function () {
            var self = this;

            new Model("cowin_project.cowin_project")
                .call("action_message_me_view", [[]])
                .then(function (result) {
                    console.log(result)
                    self.$el.append(QWeb.render('MessageMeView', {message_data: result}));
                })
        },


    });

    core.action_registry.add('message_me_view_js', MessageList);

    return MessageList;

});