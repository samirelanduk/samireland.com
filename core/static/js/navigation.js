const SmoothScroll = require("smooth-scroll");

module.exports = {
    toggleNav: function() {
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
    },

    scroll: function() {
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
            if (window.location.pathname == "/") {
                nav.classList.add("logo-visible");
            }
        } else {
            nav.classList.remove("shadowed");
            if (window.location.pathname == "/") {
                nav.classList.remove("logo-visible");
            }
        }
    },

    setupSmoothScrolling: function() {
        new SmoothScroll('a[href*="#"]', {updateURL: false});
        document.addEventListener("scrollStart", function (event) {
            let navlinks = document.getElementsByClassName("navlinks").item(0);
            navlinks.removeAttribute("style");
        }, false);
    }
}