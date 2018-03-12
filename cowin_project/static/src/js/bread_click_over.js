/**
 * Created by 123 on 2018/1/11.
 */
odoo.define('linkloving_core.TreeView', function (require) {
    "use strict";

    var core = require('web.core');
    var data = require('web.data');
    var data_manager = require('web.data_manager');
    var Model = require('web.Model');
    var Widget = require('web.Widget');
    var Pager = require('web.Pager');
    var pyeval = require('web.pyeval');
    var View = require('web.View');
    var framework = require('web.framework');
    var ActionManager = require('web.ActionManager');

    var QWeb = core.qweb;
    var _t = core._t;

    ActionManager.include(/** @lends instance.web.ListView.List# */{
        select_action: function(action, index) {
            var self = this;
            var def = this.webclient && this.webclient.clear_uncommitted_changes() || $.when();
            console.log(action);
            console.log(index);

            var custom_tags = ['process_kanban_to_detail', 'follow_invest_kanban_to_detail', 'approval_kanban_to_detail', 'approval_after_invest_kanban_to_detail', 'approval_after_invest_kanban_to_detail'];
            var flag = _.contains(custom_tags, action.action_descr.tag);
            if(flag){
                self.clear_action_stack(self.action_stack.splice(self.action_stack.indexOf(action) + 0));
                return this.do_action(action.action_descr);
            } else {
                return def.then(function() {
                    // Set the new inner_action/widget and update the action stack
                    var old_action = self.inner_action;
                    var action_index = self.action_stack.indexOf(action);
                    var to_destroy = self.action_stack.splice(action_index + 1);
                    self.inner_action = action;
                    self.inner_widget = action.widget;

                    return $.when(action.restore(index)).done(function() {
                        // Hide the ControlPanel if the widget doesn't use it
                        if (!self.inner_widget.need_control_panel) {
                            self.main_control_panel.do_hide();
                        }
                        // Attach the DOM of the action and restore the scroll position only if necessary
                        if (action !== old_action) {
                            // Clear the action stack (this also removes the current action from the DOM)
                            self.clear_action_stack(to_destroy);

                            // Append the fragment of the action to restore to self.$el
                            framework.append(self.$el, action.get_fragment(), {
                                in_DOM: self.is_in_DOM,
                                callbacks: [{widget: action.widget}],
                            });
                        }
                        self.trigger_up('current_action_updated', {action: action});
                    });
                }).fail(function() {
                    return $.Deferred().reject();
                });
            }
        },


        do_load_state: function(state, warm) {
            var self = this;
            var action_loaded;

            if (state.action) {
                if (_.isString(state.action) && core.action_registry.contains(state.action)) {
                    var action_client = {
                        type: "ir.actions.client",
                        tag: state.action,
                        params: state,
                        _push_me: state._push_me,
                    };
                    if (warm) {
                    // if (false) {
                        this.null_action();
                    }
                    action_loaded = this.do_action(action_client);
                } else {
                    var run_action = (!this.inner_widget || !this.inner_widget.action) || this.inner_widget.action.id !== state.action;

                    //  自定义返回数据操作,构建历史操作信息
                    if (this.inner_widget && this.inner_widget.action && this.inner_widget.action.type == 'ir.actions.client') {

                        var custom_tags = ['process_kanban_to_detail', 'follow_invest_kanban_to_detail', 'approval_kanban_to_detail', 'approval_after_invest_kanban_to_detail', 'approval_after_invest_kanban_to_detail'];

                        var run_history_back = _.contains(custom_tags, this.inner_widget.action.tag);


                        if (run_history_back) {
                            return this.history_back();
                         }
                    }



                    if (run_action) {
                        var add_context = {};
                        if (state.active_id) {
                            add_context.active_id = state.active_id;
                        }
                        if (state.active_ids) {
                            // The jQuery BBQ plugin does some parsing on values that are valid integers.
                            // It means that if there's only one item, it will do parseInt() on it,
                            // otherwise it will keep the comma seperated list as string.
                            add_context.active_ids = state.active_ids.toString().split(',').map(function(id) {
                                return parseInt(id, 10) || id;
                            });
                        } else if (state.active_id) {
                            add_context.active_ids = [state.active_id];
                        }
                        add_context.params = state;
                        if (warm) {
                            this.null_action();
                        }
                        action_loaded = this.do_action(state.action, {
                            additional_context: add_context,
                            res_id: state.id,
                            view_type: state.view_type,
                        });
                    }
                }
            } else if (state.model && state.id) {
                // TODO handle context & domain ?
                if (warm) {
                    this.null_action();
                }
                var action = {
                    res_model: state.model,
                    res_id: state.id,
                    type: 'ir.actions.act_window',
                    views: [[_.isNumber(state.view_id) ? state.view_id : false, 'form']]
                };
                action_loaded = this.do_action(action);
            } else if (state.sa) {
                // load session action
                if (warm) {
                    this.null_action();
                }
                action_loaded = this.rpc('/web/session/get_session_action',  {key: state.sa}).then(function(action) {
                    if (action) {
                        return self.do_action(action);
                    }
                });
            }

            return $.when(action_loaded || null).done(function() {
                if (self.inner_widget && self.inner_widget.do_load_state) {
                    return self.inner_widget.do_load_state(state, warm);
                }
            });
        },
    });


//  * Client action to reload the whole interface.
//  * If params.menu_id, it opens the given menu entry.
//  * If params.wait, reload will wait the openerp server to be reachable before reloading

function Reload2(parent, action) {
    var end_url = action.url;

    var l = window.location;
    var url = l.protocol + "//" + l.host + end_url;

    framework.redirect(url);
}

core.action_registry.add("reload2", Reload2);
});





