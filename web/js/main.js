// Update Jam Digital
function updateClock() {
    const now = new Date();
    document.getElementById('clock').innerText = now.toLocaleTimeString();
}
setInterval(updateClock, 1000);

// Ambil data sistem dari Python (Eel)
async function refreshStats() {
    let stats = await eel.get_sys_info()();
    document.getElementById('cpu').innerText = "CPU: " + stats.cpu;
    document.getElementById('ram').innerText = "RAM: " + stats.ram;
}
setInterval(refreshStats, 2000);
