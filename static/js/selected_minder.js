// selected_minder.js

function saveToSessionStorage(minderUser, minderId, minderName, minderPhotoUrl, minderAvailability) {
  sessionStorage.setItem("minderUser", minderUser);
  sessionStorage.setItem("minderId", minderId);
  sessionStorage.setItem("minderName", minderName);
  sessionStorage.setItem("minderPhotoUrl", minderPhotoUrl);
  sessionStorage.setItem("minderAvailability", minderAvailability);

  // Redirect to the create-booking page
  window.location.href = "/create-booking/";
}
