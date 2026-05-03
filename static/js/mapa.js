const mapaObj = L.map('mapa', { center: [-7.0, -78.5], zoom: 6 });

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors',
  maxZoom: 18
}).addTo(mapaObj);

const icono = L.divIcon({
  className: '',
  html: `<div style="
    width:30px;height:30px;
    background:#2d6a2d;
    border:3px solid white;
    border-radius:50% 50% 50% 0;
    transform:rotate(-45deg);
    box-shadow:0 3px 10px rgba(0,0,0,0.22);
    cursor:pointer;
  "></div>`,
  iconSize: [30, 30],
  iconAnchor: [15, 30],
  popupAnchor: [0, -34]
});

let estacionesConDatos = [];

async function cargarMarcadores() {
  try {
    const res = await fetch(API_URL + '/estaciones');
    const data = await res.json();
    estacionesConDatos = data;

    data.forEach(e => {
      L.marker([e.latitud, e.longitud], { icon: icono })
        .addTo(mapaObj)
        .bindPopup(`
          <div class="popup-inner">
            <h3>${e.distrito}</h3>
            <p>${e.departamento}</p>
            <button class="popup-btn" onclick="consultarDesdePopup('${e.departamento}','${e.provincia}','${e.distrito}')">
              Ver informe agroclimatico
            </button>
          </div>
        `);
    });
  } catch {
    console.error('No se pudieron cargar los marcadores.');
  }
}

cargarMarcadores();