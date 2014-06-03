<!-- JQUERY FOR SLIDING NAVIGATION -->   
$(document).ready(function() {
  $('a[href*=#]').each(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'')
    && location.hostname == this.hostname
    && this.hash.replace(/#/,'') ) {
      var $targetId = $(this.hash), $targetAnchor = $('[name=' + this.hash.slice(1) +']');
      var $target = $targetId.length ? $targetId : $targetAnchor.length ? $targetAnchor : false;
       if ($target) {
         var targetOffset = $target.offset().top - 50;

<!-- JQUERY CLICK FUNCTION REMOVE AND ADD CLASS "ACTIVE" + SCROLL TO THE #DIV -->   
         $(this).click(function() {

           $('html, body').animate({scrollTop: targetOffset}, 1000);
           return false;
         });
      }
    }
  });

});