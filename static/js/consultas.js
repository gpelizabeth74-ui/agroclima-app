function calcularDistanciaKm(lat1, lon1, lat2, lon2) {
  const R = 6371;
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
            Math.sin(dLon/2) * Math.sin(dLon/2);
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
}

function estacionMasCercana(lat, lon) {
  let menor = Infinity;
  let elegida = null;
  for (const e of ESTACIONES) {
    const dist = calcularDistanciaKm(lat, lon, e.lat, e.lon);
    if (dist < menor) {
      menor = dist;
      elegida = { ...e, distanciaKm: Math.round(dist) };
    }
  }
  return elegida;
}

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
    const lat = pos.coords.latitude;
    const lon = pos.coords.longitude;
    const cercana = estacionMasCercana(lat, lon);

    cargando(false);

    if (!cercana) {
      alert('No se encontro ninguna estacion en el sistema.');
      return;
    }

    if (cercana.distanciaKm > DISTANCIA_MAXIMA_KM) {
      const confirmar = confirm(
        `No hay una estacion cerca de tu ubicacion actual.\n\n` +
        `La estacion mas cercana es ${cercana.nombre} (${cercana.dpto}), ` +
        `a ${cercana.distanciaKm} km de distancia.\n\n` +
        `Deseas ver el informe de esa estacion?`
      );
      if (!confirmar) return;
    }

    await _consultar(cercana.dpto, cercana.prov, cercana.dist);

  }, () => {
    cargando(false);
    alert('No se pudo obtener tu ubicacion. Verifica los permisos del navegador.');
  });
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