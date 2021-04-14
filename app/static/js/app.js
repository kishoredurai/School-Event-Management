const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const sign_up_btn2 = document.querySelector("#sign-up-btns");

const sign_up_btn1 = document.querySelector("#pass-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});


sign_up_btn2.addEventListener("click", () => {
  location.replace("http://127.0.0.1:5000/")
});


sign_up_btn1.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
  console.log('hi');
});



sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});
