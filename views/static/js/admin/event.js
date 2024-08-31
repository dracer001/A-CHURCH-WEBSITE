let formModel;
if (document.querySelector("#form-model")){
    formModel = document.getElementById("form-model").cloneNode(true)
}
function addForm(addBtn) {
    let form = addBtn.parentNode.parentNode
    form.insertAdjacentElement("afterend", formModel.cloneNode(true))
}


function rmvForm(rmvBtn) {
    if (document.querySelectorAll(".form-item").length == 1){
        console.log("last item")
        return false
    }
    console.log("removing")
    let form = rmvBtn.parentNode.parentNode
    form.remove()
    console.log("removed")
}


function chooseForm(formSelect) {
    const option = formSelect.value
    const fieldOptionContainer = formSelect.nextElementSibling
    console.log("option", option)
    switch (option) {
        case "text":
        case "textarea":
        case "email":
        case "number":
        case "time": 
        case "date":

            fieldOptionContainer.innerHTML=""
            break;
    
        case "checkbox":
        case "radio":
            fieldOptionContainer.innerHTML=""
            const selcectOption = new AddOptions(fieldOptionContainer)
            selcectOption.addOption()
            break

        default:
            formSelect.value = "text"
            fieldOptionContainer.innerHTML=""
            break;
    }
}

const setOptionDB = (el, options)=>{
    let container = el.parentNode
    console.log(container)
    console.log(options)
    options = options.split(",")
    optionTool = new AddOptions(container)
    options.forEach(option =>{
        optionTool.addOption(null, option)

    })
}

class AddOptions {
    constructor(optionContainer) {
        this.optionContainer = optionContainer;
        this.option_cnt = 0;
    }

    addOption(addEl, value) {
        const optionBox = document.createElement("div")
        optionBox.classList.add("option-box") 

        this.option_cnt++;
        let optionTag = document.createElement("input");
        optionTag.classList.add("select-option", "form-control")
        optionTag.setAttribute("placeholder", "option " + this.option_cnt);
        optionTag.required = true
        if(value) optionTag.value=value
        optionBox.appendChild(optionTag);
        this.createOptionBtn(optionBox)
        if (addEl) {
            addEl.insertAdjacentElement("afterend", optionBox)
            this.recountOptions();
        }else{
            this.optionContainer.appendChild(optionBox)
        }
    }

    removeOption(el) {
        if (this.recountOptions() == 1){
            return false
        } 
        this.option_cnt--;
        el.remove()
        this.recountOptions()
        
    }

    createOptionBtn(container) {
        const btn_container = document.createElement("div");
        btn_container.classList.add("option-add-rmv-btn", "d-flex", "justify-content-end");

        const add_option_btn = document.createElement("i");
        add_option_btn.classList.add("bi", "bi-plus-circle", "add");
        add_option_btn.addEventListener("click", (event) => this.addOption(event.target.parentNode.parentNode));

        const rmv_option_btn = document.createElement("i");
        rmv_option_btn.classList.add("bi", "bi-dash-circle", "rmv");
        rmv_option_btn.addEventListener("click", (event) => {
            let btn = event.target
            this.removeOption(btn.parentNode.parentNode);
        });

        btn_container.appendChild(rmv_option_btn);
        btn_container.appendChild(add_option_btn);
        container.appendChild(btn_container); // Append the buttons to the container
    }

    recountOptions(){
        const selectOptions = this.optionContainer.querySelectorAll(".select-option")
        console.log(selectOptions)
        selectOptions.forEach((element, index) => {
            element.setAttribute("placeholder", "option " + (index+1));
        });
        this.option_cnt = selectOptions.length
        return this.option_cnt
    }
}

function checkDuplicateElements(arr) {
    const set = new Set();
    for (let element of arr) {
      if (set.has(element)) {
        return true; // Found duplicate elements
      }
      set.add(element);
    }
    return false; // No duplicate elements found
  }
  

function ArrangeForm() {
    const form = []
    const formItems = document.querySelectorAll(".form-item")
    formItems.forEach(item =>{
        let formData = {}
        field_names = document.querySelectorAll(".field-name")
        if(checkDuplicateElements(field_names)) return false
        if(!item.querySelector(".field-name").value.trim()){
            return false

        } 
        formData.field_name = item.querySelector(".field-name").value
        formData.field_type =  item.querySelector(".form-select").value
        let options = item.querySelectorAll(".select-option")
        console.log("Options", options)
        if (options.length > 0){
            if (checkDuplicateElements(options)) return false
            formData.options = []
            options.forEach(option =>{
                if (!option.value.trim()) return false
                formData.options.push(option.value)
                
            })
        }
        form.push(formData)
        console.log(formData)
        const jsonString = JSON.stringify(form);
        console.log(jsonString)
        document.getElementById("reg-form").value = jsonString
        console.log(document.getElementById("reg-form"))
    })
}



