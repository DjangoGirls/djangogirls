$(document).ready(function() {

    $('.gallery').sss({
        showNav: false
    });

    function imitate_link(element) {
        var url = $(element).attr('rel');
        if (url != undefined) window.location = url;
    }

    $('.event .credit').click(function() {
        imitate_link(this);
        return false;
    });

    $('.event .credit span').click(function() {
        imitate_link(this);
        return false;
    });

    $('.show-more a').click(function(){
        $('.upcoming-events .row-container').css('max-height', '100%');
        $('.upcoming-events .row-container').css('overflow', 'visible');
        $('.show-more').css('display', 'none');
    });
});
