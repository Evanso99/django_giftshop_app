document.addEventListener("DOMContentLoaded", function() {
    const inputField = document.getElementById("id_username"); // Replace with your field ID
    const helpText = document.querySelector(".help-text");

    inputField.addEventListener("focus", function() {
        helpText.style.display = "block";
    });

    inputField.addEventListener("blur", function() {
        helpText.style.display = "none";
    });
});

