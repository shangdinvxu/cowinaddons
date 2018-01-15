/**
 * Created by 123 on 2018/1/15.
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

    var _t = core._t;

    Menu.include(/** @lends instance.web.ListView.List# */{
        open_menu: function (id) {
            this.current_menu = id;
            session.active_id = id;
            var $clicked_menu, $sub_menu, $main_menu;
            $clicked_menu = this.$el.add(this.$secondary_menus).find('a[data-menu=' + id + ']');
            this.trigger('open_menu', id, $clicked_menu);

            if (this.$secondary_menus.has($clicked_menu).length) {
                $sub_menu = $clicked_menu.parents('.oe_secondary_menu');
                $main_menu = this.$el.find('a[data-menu=' + $sub_menu.data('menu-parent') + ']');
            } else {
                $sub_menu = this.$secondary_menus.find('.oe_secondary_menu[data-menu-parent=' + $clicked_menu.attr('data-menu') + ']');
                $main_menu = $clicked_menu;
            }

            // Activate current main menu
            this.$el.find('.active').removeClass('active');
            $main_menu.parent().addClass('active');

            // Show current sub menu
            this.$secondary_menus.find('.oe_secondary_menu').hide();
            $sub_menu.show();

            // Hide/Show the leftbar menu depending of the presence of sub-items
            this.$secondary_menus.toggleClass('o_hidden', !$sub_menu.children().length);

            // Activate current menu item and show parents
            this.$secondary_menus.find('.active').removeClass('active');
            if ($main_menu !== $clicked_menu) {
                $clicked_menu.parents().removeClass('o_hidden');
                if ($clicked_menu.is('.oe_menu_toggler')) {
                    $clicked_menu.toggleClass('oe_menu_opened').siblings('.oe_secondary_submenu:first').toggleClass('o_hidden');
                } else {
                    $clicked_menu.parent().addClass('active');
                    if($clicked_menu.parents('ul').eq(0).prev().hasClass('oe_menu_opened')){
                        // console.log('sssss')
                    }else {
                        $clicked_menu.parents('ul').eq(0).prev().toggleClass('oe_menu_opened');
                    }
                }
            }
            // add a tooltip to cropped menu items
            this.$secondary_menus.find('.oe_secondary_submenu li a span').each(function() {
                $(this).tooltip(this.scrollWidth > this.clientWidth ? {title: $(this).text().trim(), placement: 'right'} :'destroy');
           });
        },
    });
});
