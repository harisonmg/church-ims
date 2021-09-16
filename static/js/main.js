let formGroups = document.getElementsByClassName("form-group");

let updateFormElements = function(formElements){
    for (let index = 0; index < formElements.length; index++) {
        // get the label and immediate child div
        const formElement = formElements[index];
        const label = formElement.getElementsByTagName("label")[0];
        const childDiv = formElement.getElementsByTagName("div")[0];

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
