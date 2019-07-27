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
    var scroll = new SmoothScroll('a[href*="#"]', {updateURL: false});
    document.addEventListener('scrollStart', function (event) {
        let navlinks = document.getElementsByClassName("navlinks").item(0);
        navlinks.removeAttribute("style");
    }, false);

    // Project cards
    function closeCard(e) {
        e.target.parentElement.remove();
    }
    let projects = document.getElementsByClassName("project");
    for (var p = 0; p < projects.length; p++) {
        projects.item(p).addEventListener("click", function(e) {
            let element = e.target;
            while (!element.classList.contains("project")) {
                element = element.parentElement;
            }
            if (!element.classList.contains("inactive")) {
                let clone = element.cloneNode(true);
                clone.getElementsByClassName("close-button").item(0).onclick = closeCard;
                clone.classList.add("expanded");
                document.body.appendChild(clone);
            }
            
        });
    }

    // Technology buttons
    let buttons = document.getElementsByClassName("tech-button");
    for (var b = 0; b < buttons.length; b++) {
        buttons.item(b).addEventListener("click", function(e) {
            var button = e.target;
            if (button.classList.contains("inactive")) {
                button.classList.remove("inactive");
                button.classList.add("active");
            } else {
                button.classList.add("inactive");
                button.classList.remove("active");
            }
            var actives = document.getElementsByClassName("active");
            var technologies = [];
            for (var a = 0; a < actives.length; a++) {
                technologies.push(actives[a].innerHTML);
            }
            var projects = document.getElementsByClassName("project");
            for (var p = 0; p < projects.length; p++) {
                var projectTechnologies = projects[p].getAttribute("data-tech").split(",");
                if (projectTechnologies.filter(
                    value => technologies.includes(value)).length || technologies.length == 0
                ) {
                    projects[p].classList.remove("inactive");
                } else {
                    projects[p].classList.add("inactive");
                }
            }
        });
    }
}