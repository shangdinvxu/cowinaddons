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
            'click .view_more_message span':'get_more_message'
        },
        //获取更多信息
        get_more_message:function () {
            var self = this;
            $('.view_more_message').remove();
            self.offset = self.offset + self.limit;
            new Model("cowin_project.cowin_project")
                .call("action_message_me_view", [[]],{limit:self.limit, offset:self.offset})
                .then(function (result) {
                    console.log(result);
                    if(self.offset + self.limit<result.total_count){
                        var view_more = true;
                    }else {
                        var view_more = false;
                    }
                    $('.message_container').append(QWeb.render('MessageMeView', {message_data: result,view_more:view_more}));
                })
        },

        init: function (parent, action) {
            this._super.apply(this, arguments);
            var self = this;
            self.limit = 80;
            self.offset = 0;

        },
        start: function () {
            var self = this;

            new Model("cowin_project.cowin_project")
                .call("action_message_me_view", [[]],{limit:self.limit, offset:self.offset})
                .then(function (result) {
                    console.log(result);
                    if(self.offset + self.limit<result.total_count){
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