window.addEventListener("DOMContentLoaded", function () {
  let navBtn = document.querySelector(".fa-bars");
  let navClasses = navBtn.classList;
  let navbarClasses = document.querySelector(".navbar").classList;
  let headerClasses = document.querySelector("header").classList;
  let navbarMenuClasses = document.querySelector(".navbar ul li a").classList;

  navBtn.addEventListener("click", () => {
    navClasses.toggle("fa-times");
    navbarClasses.toggle("nav-toggle");
  });

  document.addEventListener("scroll", function () {
    navClasses.remove("fa-times");
    navbarClasses.remove("nav-toggle");

    if (window.scrollY > 30) {
      headerClasses.add("header-active");
    } else {
      headerClasses.remove("header-active");
    }
  });
});
