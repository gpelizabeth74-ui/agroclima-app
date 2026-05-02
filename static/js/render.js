let cultivoActivo = null;
let todosLosCultivos = [];

function renderResultado(data) {
  document.getElementById('res-titulo').textContent = data.distrito;
  document.getElementById('res-subtitulo').textContent = 'Estacion: ' + data.estacion_referencia + ' · ' + data.fecha_consulta;

  const card = document.getElementById('card-semaforo');
  card.className = 'card-semaforo ' + data.semaforo;

  const svgPaths = {
    VERDE:    '<polyline points="20 6 9 17 4 12"/>',
    AMARILLO: '<line x1="12" y1="8" x2="12" y2="13"/><circle cx="12" cy="17" r="0.5" fill="white" stroke="white"/>',
    ROJO:     '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>'
  };
  document.getElementById('semaforo-svg').innerHTML = svgPaths[data.semaforo] || '';
  document.getElementById('res-distrito').textContent = data.distrito;
  document.getElementById('res-estacion').textContent = 'Estacion de referencia: ' + data.estacion_referencia;
  document.getElementById('semaforo-badge').textContent = data.semaforo;

  // Clima con notas
  renderFila('res-tmax', data.clima_hoy.temp_max + ' °C', NOTAS_CLIMA.temp_max);
  renderFila('res-tmin', data.clima_hoy.temp_min + ' °C', NOTAS_CLIMA.temp_min);
  renderFila('res-prec', data.clima_hoy.precipitacion_mm + ' mm', NOTAS_CLIMA.precipitacion);
  renderFila('res-hum',  data.clima_hoy.humedad_relativa + '%', NOTAS_CLIMA.humedad);

  // Historico
  document.getElementById('res-tmax-hist').textContent = data.contexto_historico.temp_max_promedio_historico + ' °C';
  document.getElementById('res-prec-hist').textContent = data.contexto_historico.precipitacion_promedio_historico + ' mm';
  document.getElementById('res-comparacion').textContent = data.contexto_historico.comparacion;

  // Cultivos
  todosLosCultivos = data.realidad_agricola;
  cultivoActivo = null;
  renderFiltros();
  renderCultivos();

  // Consejo
  document.getElementById('res-consejo').textContent = data.consejo;
}

function renderFila(id, valor, nota) {
  const el = document.getElementById(id);
  el.innerHTML = '';

  const izq = document.createElement('div');
  izq.className = 'fila-izq';

  const label = document.createElement('span');
  label.className = 'fila-label';
  label.textContent = el.dataset.label || '';

  const notaEl = document.createElement('span');
  notaEl.className = 'fila-nota';
  notaEl.textContent = nota;

  izq.appendChild(label);
  izq.appendChild(notaEl);

  const val = document.createElement('span');
  val.className = 'fila-valor';
  val.textContent = valor;

  el.appendChild(izq);
  el.appendChild(val);
}

function renderFiltros() {
  const div = document.getElementById('filtros');
  div.innerHTML = '';

  const todos = document.createElement('button');
  todos.className = 'chip' + (cultivoActivo === null ? ' activo' : '');
  todos.textContent = 'Todos';
  todos.onclick = () => { cultivoActivo = null; renderFiltros(); renderCultivos(); };
  div.appendChild(todos);

  todosLosCultivos.forEach(c => {
    const chip = document.createElement('button');
    chip.className = 'chip' + (cultivoActivo === c.cultivo ? ' activo' : '');
    chip.textContent = c.cultivo;
    chip.onclick = () => { cultivoActivo = c.cultivo; renderFiltros(); renderCultivos(); };
    div.appendChild(chip);
  });
}

function renderCultivos() {
  const lista = cultivoActivo
    ? todosLosCultivos.filter(c => c.cultivo === cultivoActivo)
    : todosLosCultivos;

  document.getElementById('lista-cultivos').innerHTML = lista.map(c => `
    <div class="cultivo-item">
      <div class="cultivo-nombre">${c.cultivo}</div>
      <div class="cultivo-datos">
        <span class="cultivo-tag">Produccion: <strong>${c.produccion_t} t</strong></span>
        <span class="cultivo-tag">Cosecha: <strong>${c.cosecha_ha} ha</strong></span>
        <span class="cultivo-tag">Precio: <strong>S/ ${c.precio_soles_kg}/kg</strong></span>
      </div>
    </div>
  `).join('');
}
