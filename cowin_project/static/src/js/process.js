/**
 * Created by 123 on 2017/10/14.
 */
odoo.define('cowin_project.project_process', function (require) {
    "use strict";

    var core = require('web.core');
    var Model = require('web.Model');
    var Widget = require('web.Widget');
    var View = require('web.View');
    var Dialog = require('web.Dialog');
    var ControlPanelMixin = require('web.ControlPanelMixin');
    var SearchView = require('web.SearchView');
    var data = require('web.data');
    var _t = core._t;


    var ProjectProcess = Widget.extend({
        template: 'process_tmp',
        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.bom_id = action.bom_id;
            var self = this;
        },
        start: function () {
            var self = this;

        }
    });
    core.action_registry.add('project_process', ProjectProcess);

    return ProjectProcess;
});