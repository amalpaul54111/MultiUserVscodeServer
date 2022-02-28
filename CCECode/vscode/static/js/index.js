const signUpButton = document.getElementById("signUp");
const signInButton = document.getElementById("signIn");
const container = document.getElementById("container");
let context = document.getElementById("context")

if(context.innerHTML === ""){
    context.style.display= "none"
}

signUpButton.addEventListener("click", () => {
    container.classList.add("right-panel-active");
});

signInButton.addEventListener("click", () => {
    container.classList.remove("right-panel-active");
});
