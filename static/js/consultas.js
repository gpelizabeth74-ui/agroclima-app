function estacionMasCercanaPorNombre(dpto, prov, dist) {
  if (estacionesConDatos.length === 0) return null;
  const mismoDepto = estacionesConDatos.filter(e => e.departamento === dpto);
  if (mismoDepto.length > 0) return {
    nombre: mismoDepto[0].distrito,
    dpto: mismoDepto[0].departamento,
    prov: mismoDepto[0].provincia,
    dist: mismoDepto[0].distrito
  };
  return {
    nombre: estacionesConDatos[0].distrito,
    dpto: estacionesConDatos[0].departamento,
    prov: estacionesConDatos[0].provincia,
    dist: estacionesConDatos[0].distrito
  };
}