function irAResultado() {
  document.getElementById('pantalla-inicio').style.display = 'none';
  const p = document.getElementById('pantalla-resultado');
  p.style.display = 'flex';
}

function volverAlMapa() {
  document.getElementById('pantalla-resultado').style.display = 'none';
  document.getElementById('pantalla-inicio').style.display = 'flex';
  setTimeout(() => mapa.invalidateSize(), 100);
}

function cargando(v) {
  document.getElementById('overlay').style.display = v ? 'flex' : 'none';
}
