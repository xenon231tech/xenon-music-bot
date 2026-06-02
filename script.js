const songs = [
    {title: 'Summer Vibes', artist: 'Artist 1'},
    {title: 'Night Drive', artist: 'Artist 2'},
    {title: 'Morning Coffee', artist: 'Artist 3'},
    {title: 'Evening Chill', artist: 'Artist 4'}
];

let currentSong = 0;
let isPlaying = false;

function updateDisplay() {
    document.getElementById('song-title').textContent = songs[currentSong].title;
    document.getElementById('song-artist').textContent = songs[currentSong].artist;
    document.getElementById('play-btn').textContent = isPlaying ? '⏸' : '▶';
}

function togglePlay() {
    isPlaying = !isPlaying;
    updateDisplay();
}

function nextSong() {
    currentSong = (currentSong + 1) % songs.length;
    updateDisplay();
}

function previousSong() {
    currentSong = (currentSong - 1 + songs.length) % songs.length;
    updateDisplay();
}

document.getElementById('volume').addEventListener('change', (e) => {
    console.log('Volume: ' + e.target.value + '%');
});

document.getElementById('playlist-items').innerHTML = songs.map((s, i) => `
    <div onclick="currentSong=${i}; updateDisplay()" style="padding:10px; cursor:pointer; background:#f0f0f0; margin:5px 0; border-radius:5px;">
        ${s.title} - ${s.artist}
    </div>
`).join('');

updateDisplay();