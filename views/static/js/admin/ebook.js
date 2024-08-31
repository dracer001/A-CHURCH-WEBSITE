const ebookFileInput = document.querySelector('.ebook-file #ebookFileInput');
const ebookFileNameDisplay = document.querySelector('.ebook-file .file-name');
const ebookFileLabel = document.querySelector('.ebook-file .custom-file-label');

ebookFileInput.addEventListener('change', ()=> {
    if (ebookFileInput.files[0]){
        ebookFileNameDisplay.textContent = ebookFileInput.files[0].name
        ebookFileInput.name = 'ebook-file'
    }
});

const imageFileInput = document.querySelector('.ebook-image #imageFileInput');
const imageFileNameDisplay = document.querySelector('.ebook-image .file-name');
const imageFileLabel = document.querySelector('.ebook-image .custom-file-label');


imageFileInput.addEventListener('change', ()=> {
    if (imageFileInput.files[0]){
        imageFileNameDisplay.textContent = imageFileInput.files[0].name
        imageFileInput.name = 'ebook-image'
    }
});
