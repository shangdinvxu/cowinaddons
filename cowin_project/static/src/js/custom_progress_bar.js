odoo.define('cowin_project.Custom_progress_bar', function (require) {
    "use strict";

    var utils = require('web.utils');
    var ProgressBar = require('web.ProgressBar');

    ProgressBar.include({

        // _render_value: function(v) {
        //     var value = this.value;
        //     var max_value = this.max_value;
        //     if(!isNaN(v)) {
        //         if(this.edit_max_value) {
        //             max_value = v;
        //         } else {
        //             value = v;
        //         }
        //     }
        //     value = value || 0;
        //     max_value = max_value || 0;
        //
        //     var widthComplete;
        //     if(value <= max_value) {
        //         widthComplete = value/max_value * 100;
        //     } else {
        //         widthComplete = 100;
        //     }
        //
        //     this.$('.o_progress').toggleClass('o_progress_overflow', value > max_value);
        //     this.$('.o_progressbar_complete').css('width', widthComplete + '%');
        //
        //     if(this.readonly) {
        //         if(max_value !== 100) {
        //             this.$('.o_progressbar_value').html(utils.human_number(value) + " / " + utils.human_number(max_value));
        //         } else {
        //             this.$('.o_progressbar_value').html(utils.round_decimals(value, 2) + "%");
        //         }
        //     } else if(isNaN(v)) {
        //         this.$('.o_progressbar_value').val(this.edit_max_value ? max_value : value);
        //     }}
    });



});