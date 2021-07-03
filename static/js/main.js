const currentPagePath = document.getElementById("currentPagePath");
const currentPageUrl = currentPagePath.getAttribute("value");

let navLinkAddActiveClass = function(navLink){
    navLink.classList.add("active");
    navLink.classList.remove("text-white");
    navLink.setAttribute("aria-current", "page");
};

let navigationAddActiveClass = function(nav){
    document.addEventListener("DOMContentLoaded", function() {
        let navigationLinks = nav.getElementsByClassName("nav-link")
        for (var i=0; i < navigationLinks.length; i++){
            let navLink = navigationLinks[i];
            if (navLink.classList.contains("dropdown-toggle")) {
                let navDropDownLinks = navLink.getElementsByClassName("dropdown-item");
                for (var j=0; j < navDropDownLinks.length; j++){
                    if (currentPageUrl.includes(navDropDownLinks[j].getAttribute("href"))){
                        navLinkAddActiveClass(navLink);
                    }
                };
            } else {
                if (currentPageUrl.includes(navLink.getAttribute("href"))) {
                    navLinkAddActiveClass(navLink);
                };
            };
        };
    });
};

let mainNavigation = document.getElementById("mainNavigation");
navigationAddActiveClass(mainNavigation);
