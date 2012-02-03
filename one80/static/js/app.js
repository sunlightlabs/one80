jQuery.noConflict();
(function($){

  // Init the global
  window.one80 || (one80 = {})
  one80.timeNames = {
      'Morning':    [0, 11]
    , 'Afternoon':  [12, 17]
    , 'Evening':    [18, 23]
  }

  // Get the current time of day
  var hours = moment().hours();
  $.each(one80.timeNames, function(i, range){
    var t = one80.timeNames[i];
    if(hours >= t[0] && hours <= t[1]){
      one80.timeName = i;
      return false;
    }
  });

  // Bootstrap app
  $(function(){
    // set timeName for profile page
    $('span.timename').html('Good ' + one80.timeName);

    // expandos
    $('.toggle').click(function(e){
      e.preventDefault();
      var expando = $(this).prev('.expando');
      if(expando.is(':visible')){
        expando.slideUp('fast', 'swing');
        if($(this).is('#toggle_overlay')) $(this).find('em').html('read more');
      }else{
        expando.slideDown('fast', 'swing');
        if($(this).is('#toggle_overlay')) $(this).find('em').html('less');
      }
      $(this).toggleClass('toggled');
    });

    // activate photo detail canvas when links below are hovered
    $('#img_gallery_tagged a').hover(function(){
        $('.image-annotate-canvas').mouseover()
            .find('.image-annotate-area[data-id='+$(this).attr('data-id') + ']').mouseover();
    }, function(){
        $('.image-annotate-canvas')
            .find('.image-annotate-area[data-id='+$(this).attr('data-id') + ']').mouseout()
            .end()
            .mouseout();
    });



    // mouseover galleries
    $('.image_previews').mouseoverGallery();
  });

})(jQuery);