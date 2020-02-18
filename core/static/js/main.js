const AOS = require("aos");
const navigation = require("./navigation");
const interactions = require("./interaction");

document.addEventListener("DOMContentLoaded", function() {
    // Initialise aos
    AOS.init({once: true, duration: 500, offset: 75});

    // Nav toggler
    document.getElementById("nav-button").onclick = navigation.toggleNav;

    // Scroll behavior
    window.addEventListener("scroll", navigation.scroll);

    // Smooth scrolling
    navigation.setupSmoothScrolling();

    // Project cards
    interactions.enableCards();

    // Project labels
    interactions.enableLabels();
});