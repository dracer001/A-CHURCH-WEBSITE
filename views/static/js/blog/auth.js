regForm = document.getElementById("registration-form")
regForm.addEventListener("submit", (event)=>confirmPassword(event))

const confirmPassword = (event) =>{
    console.log("confirming password")
    let password1 = document.getElementById("password")
    let password2 = document.getElementById("c-password")
    if (password1.value != password2.value){
        password2.classList.add('is-invalid')
        console.log("invalid password")
        document.getElementById("invalid-feedback-password").style.display="block"
        event.preventDefault()
        event.stopPropagation()
        return false
    }
}
