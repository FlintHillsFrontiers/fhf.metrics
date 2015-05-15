jQuery(function($) {
    $("div.metric-script").each( function() {
      console.log("Dynamically loading the script from " 
        + $(this).text() + '/@@script');
      $.getScript($(this).text()+'/@@script')
        .done(function(script, textStatus) {
          console.log('Script loaded');
        })
        .fail(function(jqxhr, setting, exception) {
          console.error(exception);
        });
    });
});


