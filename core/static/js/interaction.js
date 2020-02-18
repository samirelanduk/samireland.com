function openCard(e) {
    let element = e.target;
    while (!element.classList.contains("project")) {
        element = element.parentElement;
    }
    if (!element.classList.contains("inactive")) {
        const clone = element.cloneNode(true);
        clone.getElementsByClassName("close-button").item(0).onclick = closeCard;
        clone.classList.add("expanded");
        document.body.appendChild(clone);
        document.body.classList.add("frozen");
    }
}

function closeCard(e) {
    e.target.parentElement.classList.add("gone");
    document.body.classList.remove("frozen");
    setTimeout(function() {
        e.target.parentElement.remove();
    }, 500)
}

function labelClicked(e) {
    const button = e.target;
    if (button.classList.contains("inactive")) {
        button.classList.remove("inactive");
        button.classList.add("active");
    } else {
        button.classList.add("inactive");
        button.classList.remove("active");
    }
    const actives = document.getElementsByClassName("active");
    const technologies = [];
    for (var a = 0; a < actives.length; a++) {
        technologies.push(actives[a].innerHTML);
    }
    const projects = document.getElementsByClassName("project");
    for (let p = 0; p < projects.length; p++) {
        const projectTechnologies = projects[p].getAttribute("data-tech").split(",");
        if (projectTechnologies.filter(
            value => technologies.includes(value)).length || technologies.length == 0
        ) {
            projects[p].classList.remove("inactive");
        } else {
            projects[p].classList.add("inactive");
        }
    }
}

module.exports = {
    enableCards: function() {
        const projects = document.getElementsByClassName("project");
        for (var p = 0; p < projects.length; p++) {
            projects.item(p).addEventListener("click", openCard);
        }
    },

    enableLabels: function() {
        let buttons = document.getElementsByClassName("tech-button");
        for (var b = 0; b < buttons.length; b++) {
            buttons.item(b).addEventListener("click", labelClicked);
        }
    }
}