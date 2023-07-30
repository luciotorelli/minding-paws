// search_minders.js

// This JavaScript script handles the AJAX search functionality for minders.

$(document).ready(function() {
  const user_input = $("#user-input"); 
  const search_icon = $('#search-icon'); 
  const minders_div = $('#replaceable-content'); 
  const endpoint = '/browse-minders/';
  // The delay before submitting the AJAX request
  const delay_by_in_ms = 600;
  let scheduled_function = false; 

  // Function update minders list
  let ajax_call = function(endpoint, request_parameters) {
      $.getJSON(endpoint, request_parameters)
          .done(response => {
              minders_div.fadeTo('slow', 0).promise().then(() => {
                  minders_div.html(response['html_from_view']);
                  minders_div.fadeTo('slow', 1);
                  search_icon.removeClass('blink');
              });
          });
  };

  // Event listener for keyup in the search input field
  user_input.on('keyup', function() {
      const request_parameters = {
          q: $(this).val() 
      };

      // Start animating the search icon with the CSS class
      search_icon.addClass('blink');

      // If a scheduled function exists, cancel execution to stop multiple AJAX requests
      if (scheduled_function) {
          clearTimeout(scheduled_function);
      }

      // Schedule the AJAX call after the specified delay
      // This avoids making AJAX requests on every keystroke, helps reduce server load
      scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters);
  });
});
