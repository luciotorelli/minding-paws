//fill_minder_fields.js

var minderId = sessionStorage.getItem("minderId");
var minderUser = sessionStorage.getItem("minderUser");
var minderName = sessionStorage.getItem("minderName");
var minderPhotoUrl = sessionStorage.getItem("minderPhotoUrl");
var minderAvailability = sessionStorage.getItem("minderAvailability");

// Create a new option element so it is pre-selected on the hidden minder field.
var selectedMinderOption = document.createElement("option");
selectedMinderOption.value = minderId;
selectedMinderOption.textContent = minderUser;
selectedMinderOption.selected = true;
var selectTag = document.getElementById("id_minder");
selectTag.appendChild(selectedMinderOption);

// Fill hidden minder name field
document.getElementById("id_minder_name").value = minderName;

// Check if the minderPhotoUrl is a placeholder
var placeholderValue = "placeholder";
if (minderPhotoUrl.includes(placeholderValue)) {
  document.getElementById("minder_photo_booking").src = "https://res.cloudinary.com/dls3mbdix/image/upload/v1690889814/static/img/profile-placeholder_hgqisr.webp";
} else {
  document.getElementById("minder_photo_booking").src = minderPhotoUrl;
}

// Add minderName to the p element with id "minder-name-booking"
document.getElementById("minder-name-booking").textContent = 'You are booking with ' + minderName;

// Add minderAvailability to the p element with id "minder-name-booking"
document.getElementById("minder-availability-booking").textContent = 'Please note the minder usual availability. ' + minderName + ' is usually available: ' + minderAvailability;