jQuery(function($) {
    $("div.metric-script").each( function() {
      console.log("dynamically loading the script from " + $(this).text());
      $.getScript($(this).text()+'/@@script')
        .done(function(script, textStatus) {
        })
        .fail(function(jqxhr, setting, exception) {
          console.error('script failed to load, check syntax on ' +
            $(this).text());
        });
    });
});


