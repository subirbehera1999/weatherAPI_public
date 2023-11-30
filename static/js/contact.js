function validatemail(email) {
    var emailpattern = /^[a-zA-Z0-9]\w*[.]?\w*@[a-z]{3,9}[.][a-z]{2,3}$/;
    return emailpattern.test(email);
}
function validateform(){
    var nameInput = document.getElementById('name');
    var emailInput = document.getElementById('email');
    var msgInput = document.getElementById('msg');

    var name = nameInput.value.trim();
    var email = emailInput.value.trim();
    var msg = msgInput.value.trim();

    if (!validatemail(email)) {
        emailInput.setAttribute("placeholder", "Invalid email format");
        emailInput.classList.add("email");
        emailInput.value = '';
        return false;
    } else {
        emailInput.removeAttribute("placeholder");
        emailInput.classList.remove("email");
    }
    if (name==="") {
        nameInput.setAttribute("placeholder", "Please fill up Name");
        nameInput.classList.add("name");
        nameInput.value = '';
        return false;
    } else if (name.length < 3){
        nameInput.setAttribute("placeholder", "It should be more than 2 character");
        nameInput.classList.add("name");
        nameInput.value = '';
        return false;
    } else {
        nameInput.removeAttribute("placeholder");
        nameInput.classList.remove("name");
    }
    if (msg==="") {
        msgInput.setAttribute("placeholder", "Give some message");
        msgInput.classList.add("msg");
        msgInput.value = '';
        return false;
    } else {
        msgInput.removeAttribute("placeholder");
        msgInput.classList.remove("msg");
    }
    return true;


}