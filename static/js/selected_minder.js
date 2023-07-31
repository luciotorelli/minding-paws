// selected_minder.js

function saveToSessionStorage(minderUser, minderName) {
  var minderData = {
    minderUser: minderUser,
    minderName: minderName,
  };

  sessionStorage.setItem("minderData", JSON.stringify(minderData));

  // Redirect to the create-booking page
  window.location.href = "/create-booking/";
}
