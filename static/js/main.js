// set active class on sidebar links
let updateSidebarLinks = function(){
    const currentPath = window.location.pathname;
    const sidebar = document.getElementById("sidebarMenu");

    if (sidebar !== null) {
        let sidebarLinks = sidebar.getElementsByTagName("a");
        for (let index = 0; index < sidebarLinks.length; index++) {
            let link = sidebarLinks[index];
            let linkPath = link.getAttribute("href");

            // add `active` class to the current page's link
            if (linkPath === currentPath) {
                link.classList.add("active");
            };
        };
    };
};

updateSidebarLinks();


// update parent element's classes
let updateParentClass = function(){
    // get all elements with `parent-class` attribute
    let elements = document.querySelectorAll("[parent-class]");
    for (let index = 0; index < elements.length; index++) {
        let element = elements[index];
        let parent_classes = element.getAttribute("parent-class").split(" ");
        element.parentElement.classList.add(...parent_classes);
    };
};

updateParentClass();


// update forms to have floating labels and modify checkbox classes
const formGroups = document.getElementsByClassName("form-group");

let updateFormElements = function(formElements){
    for (let index = 0; index < formElements.length; index++) {
        // get the label and immediate child div
        let formElement = formElements[index];
        let label = formElement.getElementsByTagName("label")[0];
        let childDiv = formElement.getElementsByTagName("div")[0];

        // add margin to the form element
        formElement.classList.add("mb-3");

        // update checkbox classes
        if (childDiv.classList.contains("form-check")) {
            childDiv.classList.add("text-start");
        };

        // update other inputs
        if (childDiv.classList.length === 0) {
            childDiv.classList.add("form-floating");
            childDiv.appendChild(label);
        };
    };
};

updateFormElements(formGroups);
