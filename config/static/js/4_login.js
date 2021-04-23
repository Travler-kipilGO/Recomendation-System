(function () {
  const LOGIN_SELECTOR = ".login-form";
  const ID_SELECTOR = "input[name=email]";
  const PWD_SELECTOR = "input[name=password]";

  let App = window.App;
  let FormHandler = App.FormHandler;

  function vaildation() {
    console.log(this.querySelector(ID_SELECTOR).value);
  }

  formHandler = new FormHandler(LOGIN_SELECTOR);
  formHandler.addSubmitHandler(vaildation);
})(window);
