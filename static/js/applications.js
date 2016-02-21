$(document).ready(function() {
    $("#select-all-box").click(function () {
        $(".application-box").prop('checked', $(this).prop('checked'));
    });

    $('.application-box, #select-all-box').click(function() {
        updateSelectedCount();
    });

    $('.state-change').click(function(e){
        var state = $(this).data('state'),
            appId = $(this).data('app-id'),
            url = $('#applications').data('change-state-url'),
            name = $(this).text();

        $.post(url, {'state': state, 'application': appId}, function(data){
            updateApplicationState(appId, state, name);
        });
        e.preventDefault();
    });

    $('#change-state-form').submit(function(){
        var url = $(this).attr('action'),
            state = $($(this).find('option:selected')).val(),
            name = $($(this).find('option:selected')).text();

        $.post(url, $(this).serialize(), function(data){
            if (data['updated']){
                data['updated'].forEach(function(id){
                    updateApplicationState(id, state, name);
                    $('#application-'+id+'-box').prop('checked', false);
                });
            }
        });

        return false;
    });

    $('.rsvp-change').click(function(){
        var rsvp_status = $(this).data('rsvp'),
            appId = $(this).data('app-id'),
            url = $('#applications').data('change-rsvp-url'),
            name = $(this).text();

        $.post(url, {'rsvp_status': rsvp_status, 'application': appId}, function(data){
            updateApplicationRsvp(appId, rsvp_status, name);
        });
    });

    $('#id_text').keyup(function(){
        updatePreview($(this).val());
    });

    $('.rsvp-buttons .btn').click(function(){
        var option = $(this).data('option');
        if (option == 'yes' || option == 'no'){
            var rsvp_link = '\n[rsvp-url-'+option+']';
            var message = $('#id_text').val()+rsvp_link;
            $('#id_text').val(message);
            updatePreview(message);
        }
    });

    function updatePreview(value) {
        var message = value;
        message = message.replace(/\[rsvp-url-yes\]/g, '<a href="">http://djangogirls.org/rsvp-YES-generated-url</a>');
        message = message.replace(/\[rsvp-url-no\]/g, '<a href="">http://djangogirls.org/rsvp-NO-generated-url</a>');
        $('#preview').html(message);
    }

    function updateApplicationState(id, state, stateName){
        $('#application-'+id+'-state')
            .removeClass('submitted accepted rejected default waitlisted')
            .addClass(state)
            .html(stateName+' <span class="caret"></span>');
    }

    function updateApplicationRsvp(id, rsvp, rsvpName){
        $('#application-'+id+'-rsvp-status')
            .removeClass('waiting yes no')
            .addClass(rsvp)
            .html(rsvpName+' <span class="caret"></span>');
    }

    function updateSelectedCount(){
        $('#selected-count').html($('.application-box:checked').length);
    }

});
