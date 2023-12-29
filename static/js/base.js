/*
Toggle the mobile hamburger menu.
*/
document.getElementById("mobile-menu-toggle").addEventListener("click", function () {
    document.getElementById("navbar-default").classList.toggle('hidden');
});

/*
Toggle the dropdown button to add categories and items.
*/
if (document.getElementById("dropdown-button")) {
    document.getElementById("dropdown-button").addEventListener("click", function () {
        document.getElementById("dropdown-menu").classList.toggle('hidden');
    });
}

/*
Dismiss messages.
*/
document.addEventListener("DOMContentLoaded", function () {
    // dismiss message after timeout
    setTimeout(function () {
    let messages = document.querySelectorAll(".message");
        messages.forEach(function (message) {
            message.style.display = "none";
            message.remove();
        });
    }, 4000);

    // dismiss message on button click
    let buttons = document.querySelectorAll(".close");
    buttons.forEach(function (button) {
        button.addEventListener("click", function () {
            button.closest(".message").style.display = "none";
        });
    });
});