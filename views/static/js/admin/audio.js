const audioLists = document.querySelectorAll('.audio-player')
audioLists.forEach((item)=>{
    let playing = false
    let audio = new Audio()
    let playBtn = item.querySelector('.play-btn')
    let currTimeEL = item.querySelector('.curr-time')
    let fullTimeEL = item.querySelector('.full-time')
    let progressBar = item.querySelector('.audio-progress')
    // let progressBar = item.querySelector('.audio-progress-bar')
    // let progressHead = item.querySelector('.audio-progress-head')
    let file_id = item.querySelector('.audio-file_id').value;
    audio.src = '/admin/audio/download/'+file_id
    audio.ontimeupdate = ()=>{
        if (audio.duration) {
            // console.log(audio.currentTime)
            barWidth = (100/audio.duration) * audio.currentTime
            // progressBar.style.width = `${barWidth}%`
            // progressHead.style.setProperty("left", `${barWidth}%`)

            progressBar.value = barWidth
            let durmin = Math.floor(audio.duration/60)
            let dursec = Math.floor(audio.duration - durmin * 60)

            let curmin = Math.floor(audio.currentTime/60)
            let cursec = Math.floor(audio.currentTime - curmin*60)
            if(durmin < 10) durmin = "0" + durmin
            if(dursec < 10) dursec = "0" + dursec
            if(curmin < 10) curmin = "0" + curmin
            if(cursec < 10) cursec = "0" + cursec
            currTimeEL.innerText = curmin + ":" + cursec
            fullTimeEL.innerText = durmin + ":" + dursec
            
            if(audio.currentTime == audio.duration){
                playing = false
            }
        }
        if (playing){
            playBtn.classList.remove('bi-play-fill')
            playBtn.classList.add('bi-pause-fill')
        } else {
            playBtn.classList.remove('bi-pause-fill')
            playBtn.classList.add('bi-play-fill')         
        }
    }

    playBtn.addEventListener('click', ()=>{
        if (audio.paused) {
            audio.play()
            playing = true

        } else {
            audio.pause()
            playing = false
        }
    })

    progressBar.addEventListener('input', (event) => {
        percentage = event.target.value;
        console.log(percentage)
        let max_duration = audio.duration
        let present_time = (max_duration * percentage)/100
        console.log(present_time)
        audio.currentTime = present_time
    });




    // progressBarContainer.addEventListener('click', (x)=>{
    //     let max_duration = audio.duration
    //     let position = x.pageX - progressBarContainer.offsetLeft
    //     let percentage = (100 * position) / progressBarContainer.offsetWidth
    //     if(percentage > 100) percentage = 100
    //     if(percentage < 0 ) percentage = 0
    //     let present_time = (max_duration * percentage)/100
    //     console.log(present_time)
    //     audio.currentTime = present_time
    //     barWidth = percentage
    //     progressBar.style.width = `${barWidth}%`
    //     progressHead.style.setProperty("left", `${barWidth}%`)
    // })

    // let isDragging = false
    // let startX = 0
    // progressHead.addEventListener('mousedown', (x)=> {
    //     isDragging = true;
    //     startX = x.clientX - progressHead.offsetLeft;
    //     x.preventDefault(); // Prevent text selection
    //     console.log(startX)
    // });

    // progressHead.addEventListener('mousemove', function(x) {
    //     const x_pos = x.clientX - startX;
    //     console.log(x_pos)

    //     if (isDragging) {
    //         let max_duration = audio.duration
    //         let position = x.pageX - progressHead.offsetLeft
    //         let percentage = (100 * position) / progressHead.offsetWidth
    //         if(percentage > 100) percentage = 100
    //         if(percentage <0 ) percentage = 0
    
    //         // audio.currentTime = (max_duration * percentage)/100
    //         console.log((max_duration * percentage)/100)
    //         barWidth = percentage
    //         progressBar.style.width = `${barWidth}%`
    //         progressHead.style.setProperty("left", `${barWidth}%`)
    //     }
    // });

    // progressHead.addEventListener('mouseup', function() {
    //     if (isDragging) {
    //         isDragging = false;
    //     }
    // });
    
})





const audioFileInput = document.querySelector('.audio-file #audioFileInput');
const audioFileNameDisplay = document.querySelector('.audio-file .file-name');
const audioFileLabel = document.querySelector('.audio-file .custom-file-label');

// audioFileLabel.addEventListener('click', ()=> {
//     audioFileInput.click();
//     return false;
// });

audioFileInput.addEventListener('change', ()=> {
    if (audioFileInput.files[0]){
        audioFileNameDisplay.textContent = audioFileInput.files[0].name
        audioFileInput.name = 'audio-file'
    }
    // const fileName = fileInput.files[0] ? fileInput.files[0].name : 'No file selected';
    // fileNameDisplay.textContent = fileInput.files[0] ? `${fileName}` : 'No file selected';
});

const imageFileInput = document.querySelector('.audio-image #imageFileInput');
const imageFileNameDisplay = document.querySelector('.audio-image .file-name');
const imageFileLabel = document.querySelector('.audio-image .custom-file-label');

// imageFileLabel.addEventListener('click', ()=> {
//     imageFileInput.click();
//     return false;
// });

imageFileInput.addEventListener('change', ()=> {
    if (imageFileInput.files[0]){
        imageFileNameDisplay.textContent = imageFileInput.files[0].name
        imageFileInput.name = 'audio-image'
    }
    // const fileName = fileInput.files[0] ? fileInput.files[0].name : 'No file selected';
    // fileNameDisplay.textContent = fileInput.files[0] ? `${fileName}` : 'No file selected';
});
