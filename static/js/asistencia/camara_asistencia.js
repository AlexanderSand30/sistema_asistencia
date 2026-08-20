let streamActivo = null;
let idActual = null;
let tipoActual = null;
let coordsActuales = null;
let fotoCapturada = null;

const modalCamara = new bootstrap.Modal(document.getElementById('modalCamara'));
const video = document.getElementById('videoCamara');
const canvas = document.getElementById('canvasCamara');
const estadoUbicacion = document.getElementById('estadoUbicacion');

function abrirModalMarcado(id, tipo) {
    idActual = id;
    tipoActual = tipo;
    fotoCapturada = null;
    coordsActuales = null;

    document.getElementById('tituloModalCamara').textContent =
        tipo === 'entrada' ? 'Marcar Entrada' : 'Marcar Salida';

    video.style.display = 'block';
    canvas.style.display = 'none';
    document.getElementById('botonesCamara').classList.remove('d-none');
    document.getElementById('botonesConfirmar').classList.add('d-none');
    estadoUbicacion.textContent = '📍 Obteniendo ubicación...';

    modalCamara.show();
    iniciarCamara();
    obtenerUbicacion();
}

function iniciarCamara() {
    navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } })
        .then(stream => { streamActivo = stream; video.srcObject = stream; })
        .catch(err => {
            mostrarToast('error', 'No se pudo acceder a la cámara: ' + err.message);
            modalCamara.hide();
        });
}

function detenerCamara() {
    if (streamActivo) {
        streamActivo.getTracks().forEach(track => track.stop());
        streamActivo = null;
    }
}

function obtenerUbicacion() {
    if (!navigator.geolocation) {
        estadoUbicacion.textContent = '⚠️ Este navegador no soporta geolocalización';
        return;
    }
    navigator.geolocation.getCurrentPosition(
        pos => {
            coordsActuales = { lat: pos.coords.latitude, lng: pos.coords.longitude };
            estadoUbicacion.textContent = `📍 Ubicación obtenida (±${Math.round(pos.coords.accuracy)}m)`;
        },
        err => { estadoUbicacion.textContent = '⚠️ No se pudo obtener la ubicación: ' + err.message; },
        { enableHighAccuracy: true, timeout: 10000 }
    );
}

document.getElementById('btnCapturar').addEventListener('click', () => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    fotoCapturada = canvas.toDataURL('image/jpeg', 0.8);

    video.style.display = 'none';
    canvas.style.display = 'block';
    document.getElementById('botonesCamara').classList.add('d-none');
    document.getElementById('botonesConfirmar').classList.remove('d-none');
});

document.getElementById('btnRetomar').addEventListener('click', () => {
    fotoCapturada = null;
    video.style.display = 'block';
    canvas.style.display = 'none';
    document.getElementById('botonesCamara').classList.remove('d-none');
    document.getElementById('botonesConfirmar').classList.add('d-none');
});

document.getElementById('btnConfirmarMarcado').addEventListener('click', () => {
    if (!fotoCapturada) { mostrarToast('warning', 'Primero toma la foto'); return; }
    if (!coordsActuales) { mostrarToast('warning', 'Esperando ubicación, intenta de nuevo en unos segundos'); return; }

    fetch(`/api/asistencias/${idActual}/${tipoActual}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ foto: fotoCapturada, lat: coordsActuales.lat, lng: coordsActuales.lng })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) { mostrarToast('error', data.error); return; }
        const mensaje = tipoActual === 'entrada'
            ? '✅ Entrada marcada: ' + data.hora_entrada
            : '✅ Salida marcada: ' + data.hora_salida;
        mostrarToast('success', mensaje);
        modalCamara.hide();
        cargarAsistencias();
    })
    .catch(err => { console.error(err); mostrarToast('error', 'Error al marcar asistencia'); });
});

document.getElementById('modalCamara').addEventListener('hidden.bs.modal', detenerCamara);
