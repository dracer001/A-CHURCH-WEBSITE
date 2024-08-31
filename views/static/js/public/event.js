const selectField = document.getElementById('query-field-select')
const target = document.getElementById('query-field')

function setFieldType(value) {
    switch (value) {
        case 'datetime':
            target.setAttribute('type', 'date')
            // target.type = 'datetime'
            break;
        case 'a-z':
        case 'most read':
            target.setAttribute('type', 'search')

            // target.type = 'text'
            break;
        default:
            target.type = 'search'
            break;
    }
}

setFieldType(selectField.value)


selectField.addEventListener('change', (event)=>{
    let value = event.target.value
    console.log("target", target)
    console.log("value", value)
    setFieldType(value)
})
