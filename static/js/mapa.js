const mapa = L.map('mapa', { center: [-7.0, -78.5], zoom: 6 });

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors',
  maxZoom: 18
}).addTo(mapa);

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

ESTACIONES.forEach(e => {
  L.marker([e.lat, e.lon], { icon: icono }).addTo(mapa).bindPopup(`
    <div class="popup-inner">
      <h3>${e.nombre}</h3>
      <p>${e.dpto}</p>
      <button class="popup-btn" onclick="consultarDesdePopup('${e.dpto}','${e.prov}','${e.dist}')">
        Ver informe agroclimatico
      </button>
    </div>
  `);
});
