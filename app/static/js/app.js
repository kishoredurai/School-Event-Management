const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const sign_up_btn1 = document.querySelector("#pass-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});


sign_up_btn1.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
  console.log('hi');
});



sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});