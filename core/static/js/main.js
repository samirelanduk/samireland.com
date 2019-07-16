function toggleNav() {
    let navlinks = document.getElementsByClassName("navlinks").item(0);
    if (navlinks.style.height) {
        navlinks.style.removeProperty("height");
        navlinks.removeAttribute("style");
    } else {
        let height = 0;
        let links = navlinks.getElementsByTagName("a");
        for (var i = 0; i < links.length; i++) {
            height += links.item(i).clientHeight;
        }
        navlinks.style = "height: " + height + "px";
    }
}

window.addEventListener("scroll", function() {
    let position = window.pageYOffset;
    let nav = document.getElementsByTagName("nav").item(0);
    let header = document.getElementsByTagName("header").item(0);
    this.console.log(header)

    if (position > (header.offsetHeight - nav.offsetHeight)) {
        nav.classList.add("visible");
    } else {
        nav.classList.remove("visible");
    }

});

window.onload = function() {
    // Navlinks
    let navlinks = document.getElementsByClassName(
        "navlinks").item(0).getElementsByTagName("a");
    for (var a = 0; a < navlinks.length; a++) {
        navlinks.item(a).addEventListener("click", function(e) {
            e.preventDefault();
            let activeLinks = document.getElementsByClassName(
                "navlinks").item(0).getElementsByClassName("active");
            for (var a = 0; a < activeLinks.length; a++) {
                activeLinks.item(a).classList.remove("active");
            }
            e.target.parentElement.removeAttribute("style");
            e.target.classList.add("active");
            document.getElementById(
                e.target.getAttribute("href").slice(1)
            ).scrollIntoView({behavior: "smooth"});
        })
    }
}