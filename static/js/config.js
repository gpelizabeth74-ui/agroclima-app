const API_URL = window.location.origin;

const ESTACIONES = [
  { nombre:"CHICLAYO",  dpto:"LAMBAYEQUE", prov:"CHICLAYO",  dist:"CHICLAYO",  lat:-6.7714, lon:-79.8409 },
  { nombre:"FERRENAFE", dpto:"LAMBAYEQUE", prov:"FERRENAFE", dist:"FERRENAFE", lat:-6.6365, lon:-79.7936 },
  { nombre:"INCAHUASI", dpto:"LAMBAYEQUE", prov:"FERRENAFE", dist:"INCAHUASI", lat:-6.2333, lon:-79.3167 },
  { nombre:"PIURA",     dpto:"PIURA",      prov:"PIURA",     dist:"PIURA",     lat:-5.1945, lon:-80.6328 },
  { nombre:"CAJAMARCA", dpto:"CAJAMARCA",  prov:"CAJAMARCA", dist:"CAJAMARCA", lat:-7.1637, lon:-78.5001 },
];

const NOTAS_CLIMA = {
  temp_max: "Temperatura mas alta del dia. Por encima de 30C puede estressar los cultivos.",
  temp_min: "Temperatura mas baja del dia. Valores bajo 10C pueden dañar plantas sensibles al frio.",
  precipitacion: "Agua caida en milimetros. 1mm equivale a 1 litro por metro cuadrado de suelo.",
  humedad: "Porcentaje de humedad en el aire. Alta humedad favorece hongos y enfermedades foliares."
};
