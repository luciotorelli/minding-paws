// fill_minder_fields.js

document.addEventListener("DOMContentLoaded", function () {
    // Get the saved minder data from the Session Storage
    var minderDataString = sessionStorage.getItem("minderData");
  
    // If minder data is present, parse it from JSON
    if (minderDataString) {
      var minderData = JSON.parse(minderDataString);
  
      // Fill the Minder field with the saved value
      var minderField = $("#id_minder");
      minderField.val(minderData.minderUser);
  
      // Fill the Minder Name field with the saved value
      var minderNameField = $("#id_minder_name");
      minderNameField.val(minderData.minderName);
    }
  });
  