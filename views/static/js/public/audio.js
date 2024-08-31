const audioLists = document.querySelectorAll('.audio-item');
const nowplaying = document.getElementById('now-playing')
const NOWPLAYING = {
    audio: null,
    src: '',
    playing: false,
    btn: null,
    display: 'none',
    img: '',
    title: '',
    artist: '',
};

audioLists.forEach((item) => {
    let audio = new Audio();
    let playBtn = item.querySelector('.play-btn');
    let progressBar = item.querySelector('.audio-progress');
    let title = item.querySelector('.audio-title').getAttribute('data-title');
    let artist = item.querySelector('.audio-artist').getAttribute('data-name');
    let image_id = item.querySelector('img').getAttribute('data-file');
    let file_id = playBtn.getAttribute('data-file');
    audio.src = '/admin/audio/download/' + file_id;

    audio.ontimeupdate = () => {
        if (audio.duration) {
            let barWidth = (100 / audio.duration) * audio.currentTime;
            progressBar.value = barWidth;
            updateProgress();
            if (audio.currentTime == audio.duration) {
                playing = false;
                NOWPLAYING.playing = false;
                playBtn.classList.remove('bi-pause-fill');
                playBtn.classList.add('bi-play-fill');
            }
        }

        if (NOWPLAYING.src === file_id) {
            if (NOWPLAYING.playing) {
                playBtn.classList.remove('bi-play-fill');
                playBtn.classList.add('bi-pause-fill');
            } else {
                playBtn.classList.remove('bi-pause-fill');
                playBtn.classList.add('bi-play-fill');
            }
        }
    };

    playBtn.addEventListener('click', () => {
        if(NOWPLAYING.display === 'none'){
            NOWPLAYING.display = 'block';
            displayNowPlaying(NOWPLAYING.display, nowplaying);
        } 

        if (NOWPLAYING.src === file_id) {
            if (audio.paused) {
                audio.play();
                NOWPLAYING.playing = true;
            } else {
                audio.pause();
                NOWPLAYING.playing = false;
            }
        } else {
            if (NOWPLAYING.playing) {
                NOWPLAYING.audio.pause();
                NOWPLAYING.btn.classList.remove('bi-pause-fill');
                NOWPLAYING.btn.classList.add('bi-play-fill');
            }
            audio.play();
            NOWPLAYING.audio = audio;
            NOWPLAYING.src = file_id;
            NOWPLAYING.btn = playBtn;
            NOWPLAYING.playing = true;
            NOWPLAYING.img = image_id;
            NOWPLAYING.title = title;
            NOWPLAYING.artist = artist;
        }

        setNowPlaying();
        console.log('origin', NOWPLAYING.playing)
    });
})


document.querySelector('#now-playing .cancel-btn').addEventListener('click', ()=>{
    NOWPLAYING.audio.pause();
    NOWPLAYING.display = 'none';
    displayNowPlaying(NOWPLAYING.display, nowplaying)
    NOWPLAYING.btn.classList.remove('bi-pause-fill');
    NOWPLAYING.btn.classList.add('bi-play-fill');
    NOWPLAYING.playing = false;
    document.querySelector('#now-playing .hide-btn').classList.replace('bi-chevron-up', 'bi-chevron-down')
})

document.querySelector('#now-playing .hide-btn').addEventListener('click', (event)=>{
    if (event.target.classList.contains('bi-chevron-down')) {
         event.target.classList.replace('bi-chevron-down', 'bi-chevron-up')

        NOWPLAYING.display = 'hidden';
    }else if(event.target.classList.contains('bi-chevron-up')){
        event.target.classList.replace('bi-chevron-up', 'bi-chevron-down')
        NOWPLAYING.display = 'block';
    }
    console.log(event.target)

    displayNowPlaying(NOWPLAYING.display, nowplaying)

})

// document.querySelector('#now-playing .bi-chevron-up').addEventListener('click', (event)=>{
//     NOWPLAYING.display = 'block';
//     displayNowPlaying(NOWPLAYING.display, nowplaying)
//     event.target.classList.replace('bi-chevron-up', 'bi-chevron-down')
// })


function displayNowPlaying(style, nowplaying) {
    switch (style) {
        case 'block':
            nowplaying.style.transform = 'translateY(0%)';
            break;
            
        case 'hidden':
            nowplaying.style.transform = 'translateY(80%)';
            break;

        case 'none':
            nowplaying.style.transform = 'translateY(100%)';
            
            break;
    
        default:
            break;
    }
}

function setNowPlaying(){
    const audioImg = document.querySelector('#now-playing .audio-img')
    const playBtn = document.querySelector('#now-playing .play-pause-btn')
    const title_dis = document.querySelector('#now-playing .title')
    const artist_dis = document.querySelector('#now-playing .artist')
    audioImg.src = `http://127.0.0.1:5000/admin/audio/download/${NOWPLAYING.img}`;
    if(NOWPLAYING.playing){
        playBtn.classList.replace('bi-play-circle', 'bi-pause-circle')
    }else{
        playBtn.classList.replace('bi-pause-circle', 'bi-play-circle')
    }
    console.log('heck nouber of time nowplayinf')
    title_dis.innerText = NOWPLAYING.title
    artist_dis.innerText = NOWPLAYING.artist


}


const playBtn = document.querySelector('#now-playing .play-pause-btn')
playBtn.addEventListener('click', ()=>{
    console.log('FROM NOWPLAYING', NOWPLAYING.playing)
    if(NOWPLAYING.playing){
        NOWPLAYING.audio.pause()
        NOWPLAYING.playing = false
        playBtn.classList.replace('bi-pause-circle', 'bi-play-circle')

    }else{
        NOWPLAYING.audio.play()
        NOWPLAYING.playing = true
        playBtn.classList.replace('bi-play-circle', 'bi-pause-circle')
    }
}) 

    const progressBarContainer = document.querySelector('#now-playing .audio-progress')
    const progressHead = document.querySelector('#now-playing .audio-progress-head')
    const progressBar = document.querySelector('#now-playing .audio-progress-bar')
    

    function updateProgress() {
        let barWidth = (100/NOWPLAYING.audio.duration) * NOWPLAYING.audio.currentTime
        progressBar.style.width = `${barWidth}%`
        progressHead.style.setProperty("left", `${barWidth}%`)
    }

    progressBarContainer.addEventListener('click', (x)=>{
        let max_duration = NOWPLAYING.audio.duration
        let position = x.pageX - progressBarContainer.offsetLeft
        let percentage = (100 * position) / progressBarContainer.offsetWidth
        if(percentage > 100) percentage = 100
        if(percentage < 0 ) percentage = 0
        let present_time = (max_duration * percentage)/100
        console.log(present_time)
        NOWPLAYING.audio.currentTime = present_time
        let barWidth = percentage
        progressBar.style.width = `${barWidth}%`
        progressHead.style.setProperty("left", `${barWidth}%`)
    })

    let isDragging = false
    let startX = 0
    progressHead.addEventListener('mousedown', (x)=> {
        isDragging = true;
        startX = x.clientX - progressHead.offsetLeft;
        x.preventDefault(); // Prevent text selection
        console.log(startX)
    });

    progressHead.addEventListener('mousemove', function(x) {
        const x_pos = x.clientX - startX;
        console.log(x_pos)

        if (isDragging) {
            let max_duration = audio.duration
            let position = x.pageX - progressHead.offsetLeft
            let percentage = (100 * position) / progressHead.offsetWidth
            if(percentage > 100) percentage = 100
            if(percentage <0 ) percentage = 0
    
            // audio.currentTime = (max_duration * percentage)/100
            console.log((max_duration * percentage)/100)
            barWidth = percentage
            progressBar.style.width = `${barWidth}%`
            progressHead.style.setProperty("left", `${barWidth}%`)
        }
    });

    progressHead.addEventListener('mouseup', function() {
        if (isDragging) {
            isDragging = false;
        }
    });
    

