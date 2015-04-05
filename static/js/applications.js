$(document).ready(function() {
    $('.state-change').click(function(){
        var state = $(this).data('state'),
            appId = $(this).data('app-id'),
            url = $('#applications').data('change-state-url'),
            name = $(this).text();

        $.post(url, {'state': state, 'application': appId}, function(data){
            $('#application-'+appId+'-state').removeClass('submitted');
            $('#application-'+appId+'-state').removeClass('accepted');
            $('#application-'+appId+'-state').removeClass('rejected');
            $('#application-'+appId+'-state').removeClass('default');
            $('#application-'+appId+'-state').addClass(state);
            $('#application-'+appId+'-state').html(name+' <span class="caret"></span>');
        });
    });
});
