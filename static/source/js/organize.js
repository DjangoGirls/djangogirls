$(function() {
    $('[data-required-form]').each(function() {
        var $this = $(this);
        var $checkboxes = $this.find('input[type="checkbox"][required]');
        var $textareas = $this.find('textarea[required]')
        var $submit = $this.find('[type="submit"]');

        var validate = function() {
            var allChecked = true;
            $checkboxes.each(function() {
                allChecked = allChecked && $(this).is(':checked');
            });
            $textareas.each(function() {
                allChecked = allChecked && $(this).val().length > 0
            });
            if (allChecked) {
                $submit.removeAttr('disabled');
            } else {
                $submit.attr('disabled', 'disabled');
            }
        }

        $this.attr('novalidate', 'novalidate');
        $this.on('input, change', '[required]', validate);
        validate();
    });
});
