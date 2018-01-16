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

            if(action.action_descr.tag=='process_kanban_to_detail'){
                var my_action = {
                    type: 'ir.actions.client',
                    name: '项目流程详细',
                    tag: 'process_kanban_to_detail',
                    // id: this.record.id.raw_value,
                    active_id:action.action_descr.active_id,
                    params:{'no_initate':false,'active_id':action.action_descr.active_id,action:'process_kanban_to_detail',_push_me:false,model:'cowin_project.cowin_project'}
                }
                self.clear_action_stack(self.action_stack.splice(self.action_stack.indexOf(action) + 0));
                this.do_action(my_action);
            }else {
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
    });
})