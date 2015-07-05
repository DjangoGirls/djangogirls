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
        $('.past-events .col-md-12').css('max-height', '100%');
        $('.past-events .col-md-12').css('overflow', 'visible');
        $('.show-more').css('display', 'none');
    });
});
