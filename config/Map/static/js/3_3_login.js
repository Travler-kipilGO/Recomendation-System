window.addEventListener("DOMContentLoaded", function () {
  let loginForm = document.querySelector(".login-form");
  let idInput = loginForm.querySelector("input[name=email]");
  let pwdInput = loginForm.querySelector("input[name=password]");

  function vaildation() {
    if (idInput.value) {
      console.log(idInput.value);
    } else {
      console.log("no data");
    }
  }

  loginForm.addEventListener("submit", (event) => {
    event.preventDefault();
    vaildation();
  });
});
