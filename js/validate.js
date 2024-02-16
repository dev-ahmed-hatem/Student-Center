let form = document.getElementById("register"),
    phone = document.getElementById("phone"),
    password = document.getElementById("password"),
    confirmPassword = document.getElementById("confirm-password"),
    messageSpan = document.getElementById("message"),
    submitBtn = document.getElementById("submit-btn"),
    terms = document.getElementById("terms");

function validatePhone(element) {
    if (/^\d{11}$/.test(element.value)) {
        element.classList.add("valid");
        element.classList.remove("invalid");
        messageSpan.innerHTML = "";
        return true;
    } else {
        element.classList.add("invalid");
        element.classList.remove("valid");
        messageSpan.innerHTML = "Phone number is not valid!";
        return false;
    }
}

function validatePassword(element) {
    if ((element.value.length < 8) | !/\d/.test(element.value)) {
        element.classList.remove("valid");
        element.classList.add("invalid");
        messageSpan.innerHTML = "Password is not valid!";
    } else {
        element.classList.add("valid");
        element.classList.remove("invalid");
        messageSpan.innerHTML = "";
    }
    checkSimilarity(confirmPassword);
}

function checkSimilarity(element) {
    if (!password.classList.contains("valid")) {
        messageSpan.innerHTML = "Password is not valid!";
        element.classList.remove("valid");
        element.classList.add("invalid");
    } else {
        if (element.value == password.value) {
            element.classList.add("valid");
            element.classList.remove("invalid");
            messageSpan.innerHTML = "";
        } else {
            element.classList.remove("valid");
            element.classList.add("invalid");
            messageSpan.innerHTML = "Passwords are not identical!";
        }
    }
}

form.addEventListener("input", function (event) {
    if (
        phone.classList.contains("valid") &
        password.classList.contains("valid") &
        confirmPassword.classList.contains("valid") &
        terms.checked
    ) {
        submitBtn.removeAttribute("disabled");
    } else {
        submitBtn.setAttribute("disabled", "");
    }
});
