$(document).ready(function() {
    $('.state-change').click(function(){
        var state = $(this).data('state'),
            appId = $(this).data('app-id'),
            url = $('#applications').data('change-state-url'),
            name = $(this).text();

        $.post(url, {'state': state, 'application': appId}, function(data){
            updateApplicationState(appId, state, name);
        });
    });

    $('#change-state-form').submit(function(){
        var url = $(this).attr('action'),
            state = $($(this).find('option:selected')).val(),
            name = $($(this).find('option:selected')).text();

        $.post(url, $(this).serialize(), function(data){
            if (data['updated']){
                data['updated'].forEach(function(id){
                    updateApplicationState(id, state, name);
                });
            }
        });

        return false;
    });

    $('#id_text').keyup(function(){
        $('#preview').html($(this).val());
    });

    function updateApplicationState(id, state, stateName){
        $('#application-'+id+'-state').removeClass('submitted');
        $('#application-'+id+'-state').removeClass('accepted');
        $('#application-'+id+'-state').removeClass('rejected');
        $('#application-'+id+'-state').removeClass('default');
        $('#application-'+id+'-state').removeClass('waitlisted');
        $('#application-'+id+'-state').addClass(state);
        $('#application-'+id+'-state').html(stateName+' <span class="caret"></span>');
    }


});
