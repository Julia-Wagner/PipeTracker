/*
Toggle the mobile hamburger menu.
*/
document.getElementById("mobile-menu-toggle").addEventListener("click", function() {
    document.getElementById("navbar-default").classList.toggle('hidden');
});

/*
Toggle the dropdown button to add categories and items.
*/
document.getElementById("dropdown-button").addEventListener("click", function() {
    console.log("click");
    document.getElementById("dropdown-menu").classList.toggle('hidden');
});