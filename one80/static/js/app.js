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
    $('.gallery_tagged a').hover(function(){
      $('.image-annotate-canvas').mouseover()
          .find('.image-annotate-area[data-id='+$(this).attr('data-id') + ']').mouseover();
    }, function(){
      $('.image-annotate-canvas')
          .find('.image-annotate-area[data-id='+$(this).attr('data-id') + ']').mouseout()
          .end()
          .mouseout();
    });

    // carousels
    var carousel_items = {
        'carousel_wrapper2': 4
      , 'carousel_wrapper': 2
    }
    $('#carousel_wrapper2 ol, #carousel_wrapper ol').each(function(){
      var key = $(this).parent().attr('id');
      $(this).carouFredSel({
          circular: false
        , infinite: false
        , responsive: true
        , width: '100%'
        , align: false
        , items: {
              visible: carousel_items[key]
            , start: $(this).find('li.current')
            }
        , scroll: carousel_items[key]
        , auto: false
        , prev: '#arrow_prev'
        , next: '#arrow_fw'
      });
    });

    // mouseover galleries
    $('.image_previews').mouseoverGallery();

    // legacy placeholders
    $('input[placeholder], textarea[placeholder]').placeholder();

    // // image annotations should pass events down
    // $('body.not-logged-in .image-annotate-view').click(function(){
    //   $(this).parent().nextAll('.image-annotate-add').click();
    // });
    //
    // // infinite scroll
    // $('#main_1col').onScrollBeyond(function(evt){
    //   $.throttle(1000, function(evt){
    //     // page number
    //     var doc = $(window)
    //       , page = (typeof doc.data('page') != 'number' && 1) || doc.data('page');
    //
    //     if(isNaN(page)) return false;
    //
    //     // increment page #
    //     doc.data('page', page + 1);
    //
    //     $.ajax({
    //       url: location.href + (!location.search && '?') + '&page=' + doc.data('page'),
    //     }).success(function(){
    //       switch(true){
    //         case location.href.match('/search/'):
    //         break;
    //         default:
    //         break;
    //       }
    //
    //     }).error(function(){
    //       doc.data('page', NaN);
    //     });
    //
    //   }, {
    //     buffer: 0,
    //     fireOnBeyondElement: true,
    //     fireOnDocEnd: true
    //   });
    // });

  });
})(jQuery);