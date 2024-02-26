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
    } else {
        element.classList.add("invalid");
        element.classList.remove("valid");
        messageSpan.innerHTML = "رقم موبايل غير صالح!";
    }
}

function validatePassword(element) {
    if ((element.value.length < 8) | !/\d/.test(element.value)) {
        element.classList.remove("valid");
        element.classList.add("invalid");
        messageSpan.innerHTML = "كلمة مرور ضعيفة!";
    } else {
        element.classList.add("valid");
        element.classList.remove("invalid");
        messageSpan.innerHTML = "";
    }
    checkSimilarity(confirmPassword)
}

function checkSimilarity(element) {
    if (!password.classList.contains("valid")) {
        messageSpan.innerHTML = "كلمة مرور ضعيفة!";
        element.classList.remove("valid");
        element.classList.add("invalid");
    } else {

        if (
            (element.value == password.value)
        ) {
            element.classList.add("valid");
            element.classList.remove("invalid");
            messageSpan.innerHTML = "";
        } else {
            element.classList.remove("valid");
            element.classList.add("invalid");
            messageSpan.innerHTML = "كلمات مرور غير متطابقة!";
        }
    }
}


form.addEventListener("submit", function (event) {
    event.preventDefault();
    if (!phone.classList.contains("valid")) {
        validatePhone(phone);
        console.log("submit1")
        return;
    }
    if (!password.classList.contains("valid")) {
        validatePassword(password);
        console.log("submit2")
        return;
    }
    if (!confirmPassword.classList.contains("valid")) {
        checkSimilarity(confirmPassword);
        console.log("submit3")
        return;
    }
    if (terms.checked) {
        console.log("submit")
        form.submit();
    }
})
