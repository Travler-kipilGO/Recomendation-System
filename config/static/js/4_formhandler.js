(function () {
  var App = window.App || {};

  function FormHandler(selector) {
    this.$formElement = document.querySelector(selector);
  }

  FormHandler.prototype.addSubmitHandler = function (fn) {
    this.$formElement.addEventListener("submit", function (event) {
      event.preventDefault();
      fn.bind(this)();
    });
  };

  App.FormHandler = FormHandler;
  window.App = App;
})(window);
