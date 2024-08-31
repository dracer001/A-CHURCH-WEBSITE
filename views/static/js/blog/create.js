const formModel = document.getElementById('form-model').cloneNode(true)
formModel.id=""

function disableLastBtn() {
    const contentItems = document.querySelectorAll(".content-item")
    if (contentItems.length <= 1){
        contentItems[0].querySelector('.rmv-btn').classList.add('btn-disabled')
    } else{
        contentItems[0].querySelector('.rmv-btn').classList.remove('btn-disabled')
    }
}

function addField(btn) {
    let fieldSibling = btn.parentNode.parentNode
    fieldSibling.insertAdjacentElement("afterend", formModel.cloneNode(true))
    disableLastBtn()
}



function rmvField(btn) {
    const contentItems = document.querySelectorAll(".content-item")
    if (contentItems.length <= 1){
        return false
    }
    let item = btn.parentNode.parentNode
    item.remove()
    disableLastBtn()
}

function displayTextarea(btn) {
    let contentItem = btn.parentNode.parentNode
    let current_value_input = contentItem.querySelector(".content-input").value
    let textareaItem = document.getElementById('text-area').cloneNode(true)
    textareaItem.id=""
    let textInput = textareaItem.querySelector('.content-input')
    textInput.classList.add("form-added")
    textInput.innerText = current_value_input
    textInput.required = true
    console.log(textareaItem)
    let fieldContainer = contentItem.querySelector('.field-container')
    let old_item = fieldContainer.querySelector('.field-item')
    fieldContainer.replaceChild(textareaItem, old_item)
}

function displayListul(btn) {
    let contentItem = btn.parentNode.parentNode
    let current_value_input = contentItem.querySelector(".content-input").value
    let ulItem = document.getElementById('ul').cloneNode(true)
    ulItem.id=""
    let ulInput = ulItem.querySelector('.content-input')
    ulInput.classList.add("form-added")
    ulInput.innerText = current_value_input
    ulInput.required = true
    updateLineNumbers(ulInput, 'ul')
    console.log(ulItem)
    let fieldContainer = contentItem.querySelector('.field-container')
    let old_item = fieldContainer.querySelector('.field-item')
    fieldContainer.replaceChild(ulItem, old_item)
}

function displayListol(btn) {
    let contentItem = btn.parentNode.parentNode
    let current_value_input = contentItem.querySelector(".content-input").value
    let olItem = document.getElementById('ol').cloneNode(true)
    olItem.id=""
    let olInput = olItem.querySelector('.content-input')
    olInput.classList.add("form-added")
    olInput.innerText = current_value_input
    olInput.required = true
    updateLineNumbers(olInput, 'ol')
    console.log(olItem)
    let fieldContainer = contentItem.querySelector('.field-container')
    let old_item = fieldContainer.querySelector('.field-item')
    fieldContainer.replaceChild(olItem, old_item)
}

function displaySubheader(btn) {
    let contentItem = btn.parentNode.parentNode
    let current_value_input = contentItem.querySelector(".content-input").value
    let headerItem = document.getElementById('sub-header').cloneNode(true)
    headerItem.id=""
    let headerInput = headerItem.querySelector('.content-input')
    headerInput.classList.add("form-added")
    headerInput.value = current_value_input
    headerInput.required = true
    let fieldContainer = contentItem.querySelector('.field-container')
    let old_item = fieldContainer.querySelector('.field-item')
    fieldContainer.replaceChild(headerItem, old_item)
}

function displayImageForm(btn) {
    let contentItem = btn.parentNode.parentNode
    let current_value_input = contentItem.querySelector(".content-input").value
    let imageItem = document.getElementById('image-form').cloneNode(true)
    imageItem.id=""
    let imageInput = imageItem.querySelector('.content-input')
    imageInput.classList.add("form-added")
    imageInput.required = true
    let fieldContainer = contentItem.querySelector('.field-container')
    let old_item = fieldContainer.querySelector('.field-item')
    fieldContainer.replaceChild(imageItem, old_item)
}


function updateLineNumbers(el, list_type) {
    const editor = el;
    const lineNumbers = editor.parentNode.querySelector('.line-numbers')
    const lines = editor.value.split('\n').length;
    let lineNumberHtml = '';
    
    if (list_type == 'ol') {
        for (let i = 1; i <= lines; i++) {
            lineNumberHtml += `<span>${i}</span>`;
        }
    } else if(list_type == 'ul') {
        for (let i = 1; i <= lines; i++) {
            lineNumberHtml += `<span><i class="bi bi-dot ol-dot"></i></span>`;
        }
    }
    lineNumbers.innerHTML = lineNumberHtml;
}

function syncScroll(el) {
    const editor = el;
    const lineNumbers = editor.parentNode.querySelector('.line-numbers')
    lineNumbers.scrollTop = editor.scrollTop;
}

function ArrangeForm() {
    const contentItems = document.querySelectorAll(".form-added")
    const form = []
    contentItems.forEach(content =>{
        const formData = {}
        if (content.classList.contains('text')){
            formData["field-type"] = "text"
            formData["content"] = content.value
        }else if(content.classList.contains('sub-header')){
            formData["field-type"] = "sub-header"
            formData["content"] = content.value
        }else if(content.classList.contains('image')){
            formData["field-type"] = "image"
            formData["content"] = content.files[0].name
            content.name=content.files[0].name
        }else if(content.classList.contains('ul')){
            formData["field-type"] = "ul"
            formData["content"] = content.value.split('\n')
        }else if(content.classList.contains('ol')){
            formData["field-type"] = "ol"
            formData["content"] = content.value.split('\n')
        }
        console.log(formData)
        form.push(formData)
        const jsonString = JSON.stringify(form);
        document.getElementById("blog-content").value = jsonString
        console.log(document.getElementById("blog-content").value)
    })
}
