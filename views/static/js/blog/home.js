console.log("active")

const selectField = document.getElementById('query-field-select')
const target = document.getElementById('query-field')

// document.getElementById('search-btn').addEventListener('click', ()=>{
//     console.log('clicked')
//     searchQuery(target.value)
//     console.log('finished search')
//     return false
// })

// selectField.addEventListener('change', (event)=>{
//     let value = event.target.value
//     console.log("target", target)
//     console.log("value", value)
//     switch (value) {
//         case 'post-date':
//             target.setAttribute('type', 'date')
//             // target.type = 'datetime'
//             break;
//         case 'a-z':
//         case 'most read':
//             target.setAttribute('type', 'search')

//             // target.type = 'text'
//             break;
//         default:
//             target.type = 'search'
//             break;
//     }
// })


function searchQuery(query) {
    xhttp = new XMLHttpRequest
    const field = selectField.value
    if(query.length >0 ){
        xhttp.open('GET', `/blog/blog-query?value=${query}&field=${field}`, false)
        xhttp.send()

        console.log(xhttp.responseText)
    }
}