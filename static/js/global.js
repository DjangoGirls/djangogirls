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
});
