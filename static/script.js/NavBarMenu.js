function NavBarMenu() {
    var elements_links = document.getElementById("elements-links");
    var elements_logins = document.getElementById("elements-logins");
    if (elements_links.style.display === "none") {
        elements_links.style.display = "block";
        elements_logins.style.display = "block";
    } else {
        elements_links.style.display = "none";
        elements_logins.style.display = "none";
    }
}