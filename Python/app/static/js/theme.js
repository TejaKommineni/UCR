$(document).ready(function() {
    hashHandler();
    alertHandler();
});

hashHandler = function() {
    // if there is a hash
    if (location.hash){
        // get the id of the element to show from the hash
        var id = location.hash.substring(1)
        while(id){
            // show the tab
            $('a[href=#' + id + ']').tab('show');
            // set the next id/tab to be the closest parent
            id = $('a[href=#' + id+ ']').closest(".tab-pane").attr('id');
        }
    }
    $(document.body).on("click", "a[data-toggle]", function(event) {
        location.hash = this.getAttribute("href");
    });
}

alertHandler = function() {
      if ($('#message-box').find('.alert-custom').length){
          $('#message-box').toggleClass('in');
          $('#message-box').click(function(){
            $('#message-box').toggleClass('in');
            $('#message-box').off();
            });
          setTimeout(function(){
            if($('#message-box').hasClass('in')){
                $('#message-box').toggleClass('in');
            }
          },5000);
      }

}


$(window).on('popstate', function() {
    var anchor = location.hash || $("a[data-toggle=tab]").first().attr("href");
    $('a[href=' + anchor + ']').tab('show');
});