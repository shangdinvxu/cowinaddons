/**
 * Created by 123 on 2018/1/30.
 */
odoo.define('web.menu_showhide_mark', function (require) {
    "use strict";
    /*---------------------------------------------------------
     * Odoo Editable List view linkloving version
     *---------------------------------------------------------*/
    /**
     * handles editability case for lists, because it depends on form and forms already depends on lists it had to be split out
     * @namespace
     */
    /**
    * form页面中的table表多余空白tr删除
    *
    * */

    var core = require('web.core');
    var data = require('web.data');
    var FormView = require('web.FormView');
    var common = require('web.list_common');
    var ListView = require('web.ListView');
    var Menu = require('web.Menu');
    var Model = require('web.Model');
    var utils = require('web.utils');
    var Widget = require('web.Widget');
    var session = require('web.session');
    var QWeb = core.qweb;

    var _t = core._t;

    ListView.List.include({
        render: function () {
            var self = this;
            this.$current.html(
                QWeb.render('ListView.rows', _.extend({}, this, {
                        render_cell: function () {
                            return self.render_cell.apply(self, arguments); }
                    })));
            this.pad_table_to(1);
        },
    })
});
