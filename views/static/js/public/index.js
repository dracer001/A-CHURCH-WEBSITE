// import WaveSurfer from 'https://cdn.jsdelivr.net/npm/wavesurfer.js@7/dist/wavesurfer.esm.js'
const file_id = document.getElementById("audio-file-id").value
const wavesurfer = WaveSurfer.create({
  container: '#wavesurfer',
  waveColor: '#0dcaf0',
  progressColor: '#0e6d80',
  barWidth: 2,
  barGap: 2,
  barRadius: 5,
  height: 95,
  responsive: true,
  normalize: true,
  fillParent: true,
  dragToSeek: true,
//   url: '/admin/audio/download/'+file_id,
})
wavesurfer.load('/admin/audio/download/'+file_id)
document.querySelector('.play-btn').addEventListener('click', (e)=>{
    wavesurfer.playPause();
    let btn = e.target
    if (btn.classList.contains('bi-play-fill')){
        btn.classList.remove('bi-play-fill')
        btn.classList.add('bi-pause-fill')
    }
    else  if (btn.classList.contains('bi-pause-fill')){
        btn.classList.remove('bi-pause-fill')
        btn.classList.add('bi-play-fill')
    }
})
