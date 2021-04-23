let loginForm = document.querySelector(".login-form");
let idInput = document.querySelector("input[name=email]");
let pwdInput = document.querySelector("input[name=password]");

function vaildation() {
  if (idInput.value) {
    console.log(idInput.value);
  } else {
    console.log("no data");
  }
}

loginForm.addEventListener("submit", function (event) {
  event.preventDefault();
  vaildation();
});
