window.addEventListener('load', function () {
    var usernameInput = document.getElementById('username');
    var passwordInput = document.getElementById('password');

    usernameInput.value = '';
    passwordInput.value = '';
});
function validateusername(username) {
  var regexp = /^[A-Za-z][A-Za-z0-9_]{2,14}/;
  return regexp.test(username);
}

function validatepassword(password) {
  var pattern = /^(?=.*[A-Za-z])(?=.*\d|\W).+/;
  return pattern.test(password);
}

function validatemail(email) {
  var emailpattern = /^[a-zA-Z0-9]\w*[.]?\w*@[a-z]{3,9}[.][a-z]{2,3}$/;
  return emailpattern.test(email);
}

function validateform() {
  var firstInput = document.getElementById('firstname')
  var lastInput = document.getElementById('lastname')
  var usernameInput = document.getElementById('username');
  var emailInput = document.getElementById('email');
  var passwordInput = document.getElementById('password');

  var firstname = firstInput.value.trim()
  var lastname = lastInput.value.trim()
  var name = usernameInput.value.trim();
  var email = emailInput.value.trim();
  var password = passwordInput.value.trim();


  if (firstname.length < 3) {
    firstInput.setAttribute("placeholder","Too short");
    firstInput.classList.add("firstname");
    firstInput.value = '';
  } else {
    firstInput.removeAttribute("placeholder");
    firstInput.classList.remove("firstname");
  }
  if (lastname.length < 3) {
    lastInput.setAttribute("placeholder","Too short");
    lastInput.classList.add("lastname");
    lastInput.value = '';
  } else {
    lastInput.removeAttribute("placeholder");
    lastInput.classList.remove("lastname");
  }


  if (!validateusername(name)) {
    usernameInput.setAttribute("placeholder","Should be 3 to 15 characters. Special character not allowed except '_'")
    usernameInput.classList.add("username")
    usernameInput.value = '';
    return false;
  } else {
    usernameInput.removeAttribute("placeholder")
    usernameInput.classList.remove("username")
  }

  if (!validatemail(email)) {
      emailInput.setAttribute("placeholder", "Invalid email format");
      emailInput.classList.add("email");
      emailInput.value = '';
      return false;
  } else {
      emailInput.removeAttribute("placeholder");
      emailInput.classList.remove("email");
  }

  if (!validatepassword(password)) {
      passwordInput.setAttribute("placeholder", "contains at least 1 letter and digit/special character");
      passwordInput.classList.add("password");
      passwordInput.value = '';
      return false;
  } else if (password.length < 8) {
      passwordInput.setAttribute("placeholder", "contains at least 1 letter and digit/special character");
      passwordInput.classList.add("password");
      passwordInput.value = '';
      return false;

  } else {
    passwordInput.removeAttribute("placeholder");
    passwordInput.classList.remove("password");
}

  return true;
}