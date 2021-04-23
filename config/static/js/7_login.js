class Model {
  constructor() {}
}

class View {
  constructor() {
    this.app = this.getElement("#container");
    this.form = this.createElement("form");

    this.inputId = this.createElement("input");
    this.inputId.type = "text";
    this.inputId.name = "email";

    this.inputPwd = this.createElement("input");
    this.inputPwd.type = "password";
    this.inputPwd.name = "password";

    this.submitButton = this.createElement("button");
    this.submitButton.textContent = "Submit";

    this.form.append(this.inputId, this.inputPwd, this.submitButton);
    this.app.append(this.form);

    this._initLocalListeners();
  }

  createElement(tag, className) {
    const element = document.createElement(tag);
    if (className) element.classList.add(className);

    return element;
  }

  getElement(selector) {
    const element = document.querySelector(selector);

    return element;
  }

  _initLocalListeners() {
    this.form.addEventListener("submit", (event) => {
      event.preventDefault();
      console.log("event");
    });
  }
}

class Controller {
  constructor(model, view) {
    this.model = model;
    this.view = view;
  }
}

new Controller(new Model(), new View());
