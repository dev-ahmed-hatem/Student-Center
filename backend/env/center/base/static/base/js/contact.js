function sendData(e, form, url) {
    e.preventDefault();

    // Serialize form data
    var formData = new FormData(form);

    // Send AJAX request
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                // Handle success response
                console.log(xhr.responseText);
                alert(JSON.parse(xhr.responseText)["message"]);
            } else {
                // Handle error response
                console.error(xhr.responseText);
                alert(JSON.parse(xhr.responseText)["message"]);
            }
        }
    };
    xhr.send(formData);
}
