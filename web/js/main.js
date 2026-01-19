// web/js/main.js

// Fungsi Jam Digital yang aman
function updateClock() {
    const clockElement = document.getElementById('clock');
    if (clockElement) {
        const now = new Date();
        clockElement.innerText = now.toLocaleTimeString('id-ID');
    }
}

// Fungsi Statistik yang aman
async function refreshStats() {
    try {
        const stats = await eel.get_sys_info()();
        const cpuEl = document.getElementById('cpu');
        const ramEl = document.getElementById('ram');
        
        if (cpuEl) cpuEl.innerText = stats.cpu;
        if (ramEl) ramEl.innerText = stats.ram;
    } catch (e) {
        console.log("Eel belum siap atau error stats.");
    }
}

// Jalankan interval hanya jika fungsi tersedia
setInterval(updateClock, 1000);
setInterval(refreshStats, 3000);
