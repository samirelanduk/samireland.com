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
    if (position > nav.offsetHeight) {
        nav.classList.add("visible");
    } else {
        nav.classList.remove("visible");
    }
    if (position > (header.offsetHeight - nav.offsetHeight)) {
        nav.classList.add("shadowed");
    } else {
        nav.classList.remove("shadowed");
    }
});

window.onload = function() {
    // Navlinks
    let links = document.getElementsByTagName("a");
    for (var a = 0; a < links.length; a++) {
        if (links[a].getAttribute("href")[0] === "#") {
            links.item(a).addEventListener("click", function(e) {
                e.preventDefault();
                let navlinks = document.getElementsByClassName("navlinks").item(0);
                navlinks.removeAttribute("style");
                document.getElementById(
                    e.target.getAttribute("href").slice(1)
                ).scrollIntoView({behavior: "smooth"});
            });
        }
    }
}