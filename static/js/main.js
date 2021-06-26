const currentPagePath = document.getElementById("currentPagePath")
const currentPageUrl = currentPagePath.getAttribute("value")

let addActiveClass = function(nav){
    document.addEventListener("DOMContentLoaded", function() {
        let navigationLinks = nav.getElementsByClassName("nav-link")
        for (var i=0; i < navigationLinks.length; i++){
            if (navigationLinks[i].getAttribute("href").includes(currentPageUrl)) {
                navigationLinks[i].classList.add("active");
                navigationLinks[i].classList.remove("text-white");
                navigationLinks[i].setAttribute("aria-current", "page");
            }
        }
    })
};

let addTextWhite = function(nav){
    document.addEventListener("DOMContentLoaded", function() {
        let navigationLinks = nav.getElementsByClassName("nav-link")
        for (var i=0; i < navigationLinks.length; i++){
            if (!navigationLinks[i].classList.contains("active")) {
                navigationLinks[i].classList.add("text-white")
            }
        }
    })
}

let mainNavigation = document.getElementById("mainNavigation");
let navTabs = document.getElementsByClassName("nav-tabs");
addActiveClass(mainNavigation);

for (i=0; i < navTabs.length; i++){
    addActiveClass(navTabs[i]);
    addTextWhite(navTabs[i]);
}
