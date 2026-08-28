/** @format */

function cargarAsistencias(fechaInicio, fechaFin, pagina = 1) {
  if (fechaInicio === undefined) {
    fechaInicio = document.getElementById("filtroFechaInicio")?.value || "";
    fechaFin = document.getElementById("filtroFechaFin")?.value || "";
  }

  let url = "/api/asistencias";
  const params = [];

  if (fechaInicio) {
    params.push(`fecha_inicio=${encodeURIComponent(fechaInicio)}`);
  }

  if (fechaFin) {
    params.push(`fecha_fin=${encodeURIComponent(fechaFin)}`);
  }

  params.push(`page=${pagina}`);
  params.push("per_page=10");

  if (params.length) {
    url += "?" + params.join("&");
  }

  fetch(url)
    .then((res) => {
      if (!res.ok) {
        throw new Error(`HTTP error: ${res.status}`);
      }
      return res.json();
    })
    .then((data) => {
      const cuerpo = document.getElementById("cuerpoTablaAsistencia");

      if (!cuerpo) {
        console.error("No se encontró #cuerpoTablaAsistencia");
        return;
      }

      cuerpo.innerHTML = "";

      // SIN REGISTROS
      if (!data || !data.items || data.items.length === 0) {
        renderizarPaginacionAsistencia(data, fechaInicio, fechaFin);

        cuerpo.innerHTML = `
            <tr>
                <td colspan="11" class="text-center py-5">
                    <div class="text-muted">
                        <i class="bi bi-calendar-x fs-2 d-block mb-2"></i>
                        <strong>No hay registros</strong>
                        <div class="small mt-1">
                            No existen asistencias en este rango de fechas.
                        </div>
                    </div>
                </td>
            </tr>
        `;
        return;
      }

      // FECHA ACTUAL
      const fechaActual = obtenerFechaActual();

      // RECORRER ASISTENCIAS
      data.items.forEach((a) => {
        // ESTADO DE LA ACCIÓN
        const estadoAccion = obtenerEstadoAccion(a, fechaActual);
        // ACCIONES
        let acciones = "";

        switch (estadoAccion) {
          // PUEDE MARCAR ENTRADA
          case "PUEDE_ENTRAR":
            acciones = `
                <div class="d-flex gap-1 justify-content-center">
                    <button
                        class="btn btn-sm btn-primary text-nowrap"
                        onclick="marcarEntrada(${a.id})"
                        title="Registrar entrada"
                    >
                        <i class="bi bi-box-arrow-in-right me-1"></i>
                        Entrada
                    </button>
                </div>
            `;
            break;

          // PUEDE MARCAR SALIDA
          case "PUEDE_SALIR":
            acciones = `
                <div class="d-flex gap-1 justify-content-center">
                    <button
                        class="btn btn-sm btn-warning text-nowrap"
                        onclick="marcarSalida(${a.id})"
                        title="Registrar salida"
                    >
                        <i class="bi bi-box-arrow-right me-1"></i>
                        Salida
                    </button>
                </div>
            `;
            break;

          // COMPLETA
          case "COMPLETA":
            acciones = `
                <span class="badge bg-success-subtle text-success">
                    <i class="bi bi-check-circle me-1"></i>
                    Completa
                </span>
            `;
            break;

          // FECHA ANTERIOR SIN SALIDA
          case "SIN_SALIDA":
            acciones = `
                <span
                    class="badge bg-danger-subtle text-danger"
                    title="La fecha de esta asistencia ya pasó"
                >
                    <i class="bi bi-clock-history me-1"></i>
                    Sin salida
                </span>
            `;
            break;

          // FECHA ANTERIOR SIN ENTRADA
          case "CERRADA":
            acciones = `
                <span
                    class="badge bg-secondary-subtle text-secondary"
                    title="La fecha de esta asistencia ya pasó"
                >
                    <i class="bi bi-lock me-1"></i>
                    Cerrada
                </span>
            `;
            break;

          // FECHA FUTURA
          case "FUTURA":
            acciones = `
                <span
                    class="badge bg-info-subtle text-info"
                    title="La fecha de esta asistencia aún no llega"
                >
                    <i class="bi bi-calendar-event me-1"></i>
                    Pendiente
                </span>
            `;
            break;

          // ESTADO DESCONOCIDO
          default:
            acciones = `
                <span class="badge bg-secondary-subtle text-secondary">
                    <i class="bi bi-question-circle me-1"></i>
                    Sin acción
                </span>
            `;
            break;
        }

        // FOTOS
        const fotoEntradaBtn = a.foto_entrada
          ? `
            <button
                class="btn btn-sm btn-outline-primary"
                onclick="verMarcado(
                    'Entrada',
                    '/static/${a.foto_entrada}',
                    ${a.lat_entrada ?? null},
                    ${a.lng_entrada ?? null}
                )"
                title="Ver foto de entrada"
            >
                <i class="bi bi-camera"></i>
            </button>
        `
          : `<span class="text-muted">—</span>`;

        const fotoSalidaBtn = a.foto_salida
          ? `
            <button
                class="btn btn-sm btn-outline-primary"
                onclick="verMarcado(
                    'Salida',
                    '/static/${a.foto_salida}',
                    ${a.lat_salida ?? null},
                    ${a.lng_salida ?? null}
                )"
                title="Ver foto de salida"
            >
                <i class="bi bi-camera"></i>
            </button>
        `
          : `<span class="text-muted">—</span>`;

        // UBICACIÓN DE ENTRADA
        const mapaEntrada =
          a.lat_entrada != null && a.lng_entrada != null
            ? `
                <a
                    href="https://www.google.com/maps?q=${a.lat_entrada},${a.lng_entrada}"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="text-primary"
                    title="Ver ubicación de entrada"
                >
                    <i class="bi bi-geo-alt-fill"></i>
                    Entrada
                </a>
            `
            : "";

        // UBICACIÓN DE SALIDA
        const mapaSalida =
          a.lat_salida != null && a.lng_salida != null
            ? `
                <a
                    href="https://www.google.com/maps?q=${a.lat_salida},${a.lng_salida}"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="text-success"
                    title="Ver ubicación de salida"
                >
                    <i class="bi bi-geo-alt-fill"></i>
                    Salida
                </a>
            `
            : "";

        const ubicaciones =
          mapaEntrada || mapaSalida
            ? `
                <div class="d-flex flex-column gap-1">
                    ${mapaEntrada}
                    ${mapaSalida}
                </div>
            `
            : `<span class="text-muted">—</span>`;

        // ESTADO DE ASISTENCIA
        let estadoHtml;
        if (a.estado === "Presente") {
          estadoHtml = `
                <span class="badge bg-success-subtle text-success">
                    <i class="bi bi-check-circle me-1"></i>
                    Presente
                </span>
            `;
        } else if (a.estado === "Tarde") {
          estadoHtml = `
                <span class="badge bg-warning-subtle text-warning-emphasis">
                    <i class="bi bi-clock me-1"></i>
                    Tarde
                </span>
            `;
        } else {
          estadoHtml = `
                <span class="badge bg-secondary-subtle text-secondary">
                    ${a.estado || "Pendiente"}
                </span>
            `;
        }

        // FILA
        cuerpo.innerHTML += `
            <tr>
                <td>
                    <span class="fw-semibold">${a.dni || "—"}</span>
                </td>
                <td>
                    ${a.apellidos || ""}
                    ${a.nombres || ""}
                </td>
                <td>
                    ${a.obra || '<span class="text-muted">—</span>'}
                </td>
                <td>
                    ${a.cargo || '<span class="text-muted">—</span>'}
                </td>
                <td class="text-nowrap">
                    ${formatearFecha(a.fecha)}
                </td>
                <td>
                    ${
                      a.hora_entrada
                        ? `
                            <span class="text-success fw-semibold text-nowrap">
                                <i class="bi bi-box-arrow-in-right me-1"></i>
                                ${a.hora_entrada}
                            </span>
                        `
                        : `<span class="text-muted"> — </span>`
                    }
                </td>
                <td>
                    ${
                      a.hora_salida
                        ? `
                            <span class="text-danger fw-semibold text-nowrap">
                                <i class="bi bi-box-arrow-right me-1"></i>
                                ${a.hora_salida}
                            </span>
                        `
                        : `<span class="text-muted">—</span>`
                    }
                </td>
                <td>${estadoHtml}</td>
                <td>
                    <div class="d-flex gap-1 justify-content-center">
                        ${fotoEntradaBtn}
                        ${fotoSalidaBtn}
                    </div>
                </td>
                <td>${ubicaciones}</td>
                <td>${acciones}</td>
            </tr>
        `;
      });

      // ----------------------------------------
      // PAGINACIÓN
      // ----------------------------------------

      renderizarPaginacionAsistencia(data, fechaInicio, fechaFin);
    })

    .catch((error) => {
      console.error("Error cargando asistencias:", error);

      const cuerpo = document.getElementById("cuerpoTablaAsistencia");

      if (cuerpo) {
        cuerpo.innerHTML = `
            <tr>
                <td colspan="11" class="text-center py-5">
                    <div class="text-danger">
                        <i class="bi bi-exclamation-triangle fs-2 d-block mb-2"></i>
                        <strong>
                            No se pudieron cargar las asistencias
                        </strong>
                        <div class="small text-muted mt-1">
                            Intente nuevamente.
                        </div>
                   </div>
                </td>
            </tr>
        `;
      }
    });
}

/**
 * =====================================================
 * OBTENER FECHA ACTUAL
 * =====================================================
 */
function obtenerFechaActual() {
  const hoy = new Date();
  const anio = hoy.getFullYear();
  const mes = String(hoy.getMonth() + 1).padStart(2, "0");
  const dia = String(hoy.getDate()).padStart(2, "0");
  return `${anio}-${mes}-${dia}`;
}

/**
 * =====================================================
 * OBTENER ESTADO DE LA ACCIÓN
 * =====================================================
 */
function obtenerEstadoAccion(asistencia, fechaActual) {
  const fechaRegistro = asistencia.fecha;
  if (!fechaRegistro) {
    return "CERRADA";
  }

  // FECHA FUTURA
  if (fechaRegistro > fechaActual) {
    return "FUTURA";
  }

  // FECHA ANTERIOR
  if (fechaRegistro < fechaActual) {
    // Tiene entrada pero no salida
    if (asistencia.hora_entrada && !asistencia.hora_salida) {
      return "SIN_SALIDA";
    }

    // No tiene entrada
    if (!asistencia.hora_entrada) {
      return "CERRADA";
    }

    // Tiene entrada y salida
    return "COMPLETA";
  }

  // -----------------------------------------
  // HOY
  // -----------------------------------------

  // Sin entrada

  if (!asistencia.hora_entrada) {
    return "PUEDE_ENTRAR";
  }

  // Tiene entrada pero no salida
  if (asistencia.hora_entrada && !asistencia.hora_salida) {
    return "PUEDE_SALIR";
  }

  // Tiene entrada y salida
  return "COMPLETA";
}

/**
 * =====================================================
 * PAGINACIÓN
 * =====================================================
 */

function renderizarPaginacionAsistencia(data, fechaInicio, fechaFin) {
  const paginacion = document.getElementById("paginacionAsistencia");
  const resumen = document.getElementById("resumenPaginacionAsistencia");
  if (!paginacion || !resumen) {
    return;
  }

  paginacion.innerHTML = "";
  // SIN REGISTROS
  if (!data || !data.total) {
    resumen.textContent = "0 registros";
    return;
  }

  // -----------------------------------------
  // RESUMEN
  // -----------------------------------------

  const inicio = (data.pagina - 1) * data.por_pagina + 1;
  const fin = Math.min(data.pagina * data.por_pagina, data.total);
  resumen.textContent = `Mostrando ${inicio}-${fin} de ${data.total} registros`;

  // CREAR PÁGINA
  const agregarPagina = (pagina, texto, activa = false, deshabilitada = false) => {
    const item = document.createElement("li");
    item.className = `page-item` + `${activa ? " active" : ""}` + `${deshabilitada ? " disabled" : ""}`;
    item.innerHTML = `<button class="page-link" type="button">${texto}</button>`;

    if (!deshabilitada) {
      item.querySelector("button").addEventListener("click", () => cargarAsistencias(fechaInicio, fechaFin, pagina));
    }

    paginacion.appendChild(item);
  };

  // ANTERIOR
  agregarPagina(data.pagina - 1, "Anterior", false, data.pagina === 1);

  // NÚMEROS
  for (let pagina = 1; pagina <= data.total_paginas; pagina += 1) {
    agregarPagina(pagina, pagina, pagina === data.pagina);
  }

  // SIGUIENTE
  agregarPagina(data.pagina + 1, "Siguiente", false, data.pagina === data.total_paginas);
}

//FORMATEAR FECHA
function formatearFecha(fecha) {
  if (!fecha) {
    return "--/--/--";
  }

  const partes = fecha.split("-");

  if (partes.length !== 3) {
    return fecha;
  }

  const [anio, mes, dia] = partes;
  return `${dia}/${mes}/${anio}`;
}

/**
 * =====================================================
 * INICIALIZAR RANGO DEL MES ACTUAL
 * =====================================================
 */

function inicializarRangoMesActual() {
  const hoy = new Date();
  const anio = hoy.getFullYear();
  const mes = hoy.getMonth();
  const formato = (fecha) => {
    const mesTexto = String(fecha.getMonth() + 1).padStart(2, "0");
    const diaTexto = String(fecha.getDate()).padStart(2, "0");
    return `
            ${fecha.getFullYear()}-
            ${mesTexto}-
            ${diaTexto}
        `.replace(/\s/g, "");
  };

  const inicio = new Date(anio, mes, 1);
  const fin = new Date(anio, mes + 1, 0);
  const fechaInicio = formato(inicio);
  const fechaFin = formato(fin);
  const inputInicio = document.getElementById("filtroFechaInicio");
  const inputFin = document.getElementById("filtroFechaFin");

  if (inputInicio) {
    inputInicio.value = fechaInicio;
  }

  if (inputFin) {
    inputFin.value = fechaFin;
  }

  cargarAsistencias(fechaInicio, fechaFin);
}

// =====================================================
// INICIAR
// =====================================================

inicializarRangoMesActual();
