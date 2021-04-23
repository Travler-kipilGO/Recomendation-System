const LoginView = {
  after_render: () => {
    document
      .querySelector(".login-form2")
      .addEventListener("submit", (event) => {
        event.preventDefault();

        let idInput = document.querySelector("input[name=email2]");
        function vaildation() {
          if (idInput.value) {
            console.log(idInput.value);
          } else {
            console.log("no data");
          }
        }
        vaildation();
      });
  },
  render: () => {
    return ` 
    <div class="login-form2" action="index.html">
    <form>
      <input
        type="text"
        name="email2"
        class="text-field"
        placeholder="아이디"
      />
      <input
        type="password"
        name="password2"
        class="text-field"
        placeholder="비밀번호"
      />
      <input type="submit" value="로그인" class="submit-btn" />
    </form>
    </div>
  </div>`;
  },
};

const router = () => {
  const main = document.getElementById("container");
  main.innerHTML = LoginView.render();
  if (LoginView.after_render) LoginView.after_render();
};

window.addEventListener("load", router);
