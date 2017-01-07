$(function() {
    $('[data-required-form]').each(function() {
        var $this = $(this);
        var $checkboxes = $this.find('[type="checkbox"]');
        var $submit = $this.find('[type="submit"]');

        var validate = function() {
            var allChecked = true;
            $checkboxes.each(function() {
                allChecked = allChecked && $(this).is(':checked');
            });
            if (allChecked) {
                $submit.removeAttr('disabled');
            } else {
                $submit.attr('disabled', 'disabled');
            }
        }

        $this.attr('novalidate', 'novalidate');
        $this.on('change', '[type="checkbox"]', validate);
        validate();
    });
});
