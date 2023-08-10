odoo.define('data_cleaner.custom_buttons', function(require) {
    "use strict";

    var core = require('web.core');
    var FormController = require('web.FormController');

    var _t = core._t;

    FormController.include({
        renderButtons: function($node) {
            this._super.apply(this, arguments);
            
            var self = this;
            var buttons = this.$('.cleaner_spec_inl_el');
            
            buttons.on('click', function() {
                var button = $(this);
                var index = button.data('index');
                
                if (button.hasClass('btn-secondary')) {
                    button.removeClass('btn-secondary');
                    button.addClass('btn-primary');
                    button.text(_t('Selected'));
                } else {
                    button.removeClass('btn-primary');
                    button.addClass('btn-secondary');
                    button.text(_t('Not Selected'));
                }
                
                // Update the backend with the button index (you can adjust this part as needed)
                self._rpc({
                    model: 'cleaner.spec',
                    method: 'confirm_attr',
                    args: [index, 'TESTITEM']
                });
            });
        },
    });
});
