const editBtns = document.querySelectorAll(".edit")
const submitBtn = document.getElementById("submit")
const inputs = document.querySelectorAll('input')

const zoomImage = document.querySelector('.profile-img img');

zoomImage.addEventListener('click', function() {
    this.classList.toggle('full-width');
});

inputs.forEach(input=>{
    input.addEventListener('change', ()=>{
        submitBtn.disabled = false
        if (input.id == 'dp') input.name = 'blogger-image'

    })
})

editBtns.forEach(btn =>{
    btn.addEventListener("click", (event)=>{
        let el = event.target
        console.log(el)
        let input  = el.previousSibling.previousSibling
        console.log(input)
        // input.setAttribute('readonly', false)
        input.readOnly = false
        el.disabled = true
    })
})

document.getElementById("reset").addEventListener('click', ()=>{

    editBtns.forEach(btn =>{
            let input  = btn.previousSibling.previousSibling
            console.log(input)
            // input.setAttribute('readonly', false)
            input.readOnly = true
            btn.disabled = false
    })
    submitBtn.disabled = true
})

document.querySelector('.pwd-box').addEventListener('submit', (event)=>{
    const newP = document.getElementById('new-p')
    const cnewP = document.getElementById('c-new-p')
    if(newP.value !== cnewP.value){
        cnewP.classList.add('is-invalid')
        event.preventDefault()
        event.stopPropagation()
    }
    
})

const confirmPassword = (event) =>{
    console.log("confirming password")
    let password1 = document.getElementById("new-p")
    let password2 = document.getElementById("c-new-p")
    if (password1.value != password2.value){
        password2.classList.add('is-invalid')
        console.log("invalid password")
        // document.getElementById("invalid-feedback-password").style.display="block"
        event.preventDefault()
        event.stopPropagation()
        return false
    }
}