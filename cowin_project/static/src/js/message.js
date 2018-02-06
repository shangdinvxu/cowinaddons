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
            self.limit = 30;
            self.offset = 0;

        },
        start: function () {
            var self = this;

            new Model("cowin_project.cowin_project")
                .call("action_message_me_view", [[]],{limit:self.limit, offset:self.offset})
                .then(function (result) {
                    console.log(result);
                    if((self.offset + 1)*self.limit<result.total_count){
                        var view_more = true;
                    }else {
                        var view_more = false;
                    }

                    self.$el.addClass('message_container');
                    self.$el.append(QWeb.render('MessageMeView', {message_data: result,view_more:view_more}));
                })
        },


    });

    core.action_registry.add('message_me_view_js', MessageList);

    return MessageList;

});