async function consultarDesdePopup(d, p, dist) {
  await _consultar(d, p, dist);
}

async function buscarPorDistrito() {
  const d    = document.getElementById('inp-dpto').value.trim().toUpperCase();
  const p    = document.getElementById('inp-prov').value.trim().toUpperCase();
  const dist = document.getElementById('inp-dist').value.trim().toUpperCase();
  if (!d || !p || !dist) return alert('Completa los tres campos.');
  await _consultar(d, p, dist);
}

async function buscarPorGPS() {
  if (!navigator.geolocation) return alert('Tu navegador no soporta geolocalizacion.');
  cargando(true);
  navigator.geolocation.getCurrentPosition(async pos => {
    try {
      const res = await fetch(API_URL + '/consulta/por-coordenadas', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ latitud: pos.coords.latitude, longitud: pos.coords.longitude })
      });
      cargando(false);
      if (!res.ok) return alert('No se encontro estacion cercana.');
      renderResultado(await res.json());
      irAResultado();
    } catch {
      cargando(false);
      alert('No se pudo conectar con el servidor.');
    }
  }, () => { cargando(false); alert('No se pudo obtener tu ubicacion.'); });
}

async function _consultar(d, p, dist) {
  cargando(true);
  try {
    const res = await fetch(API_URL + '/consulta/por-distrito', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ departamento: d, provincia: p, distrito: dist })
    });
    cargando(false);
    if (!res.ok) return alert('Distrito no encontrado. Verifica los datos.');
    renderResultado(await res.json());
    irAResultado();
  } catch {
    cargando(false);
    alert('No se pudo conectar con el servidor.');
  }
}
