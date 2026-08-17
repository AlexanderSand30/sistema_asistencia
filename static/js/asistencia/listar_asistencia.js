function cargarAsistencias(fechaInicio, fechaFin) {

    let url = "/api/asistencias";
    const params = [];

    if (fechaInicio) {
        params.push(`fecha_inicio=${encodeURIComponent(fechaInicio)}`);
    }

    if (fechaFin) {
        params.push(`fecha_fin=${encodeURIComponent(fechaFin)}`);
    }

    if (params.length) {
        url += "?" + params.join("&");
    }

    fetch(url)
        .then(res => res.json())
        .then(data => {
            const cuerpo = document.getElementById("cuerpoTablaAsistencia");
            cuerpo.innerHTML = "";

            if (!data || data.length === 0) {
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

            data.forEach(a => {

                // -----------------------------
                // ACCIONES
                // ----------------------------

                const botonEntrada = !a.hora_entrada
                    ? `
                        <button
                            class="btn btn-sm btn-primary text-nowrap"
                            onclick="marcarEntrada(${a.id})"
                            title="Registrar entrada"
                        >
                            <i class="bi bi-box-arrow-in-right me-1"></i>
                            Entrada
                        </button>
                    `
                    : "";

                const botonSalida =
                    a.hora_entrada && !a.hora_salida
                        ? `
                            <button
                                class="btn btn-sm btn-warning text-nowrap"
                                onclick="marcarSalida(${a.id})"
                                title="Registrar salida"
                            >
                                <i class="bi bi-box-arrow-right me-1"></i>
                                Salida
                            </button>
                        `
                        : "";

                const acciones = (botonEntrada || botonSalida)
                    ? `
                        <div class="d-flex gap-1 justify-content-center">
                            ${botonEntrada}
                            ${botonSalida}
                        </div>
                    `
                    : `
                        <span class="badge bg-success-subtle text-success">
                            <i class="bi bi-check-circle me-1"></i>
                            Completa
                        </span>
                    `;

                // -----------------------------
                // FOTOS
                // -----------------------------

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
                    : `
                        <span class="text-muted">—</span>
                    `;

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
                    : `
                        <span class="text-muted">—</span>
                    `;


                // -----------------------------
                // UBICACIÓN
                // -----------------------------
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

                const ubicaciones = (mapaEntrada || mapaSalida)
                    ? `
                        <div class="d-flex flex-column gap-1">
                            ${mapaEntrada}
                            ${mapaSalida}
                        </div>
                    `
                    : `<span class="text-muted">—</span>`;


                // -----------------------------
                // ESTADO
                // -----------------------------
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

                // -----------------------------
                // FILA
                // -----------------------------
                cuerpo.innerHTML += `
                    <tr>
                        <td>
                            <span class="fw-semibold">${a.dni || "—"}</span>
                        </td>
                        <td>${a.apellidos || ""} ${a.nombres || ""}</td>
                        <td>${a.obra || '<span class="text-muted">—</span>'}</td>
                        <td>${a.cargo || '<span class="text-muted">—</span>'}</td>
                        <td class="text-nowrap"> ${formatearFecha(a.fecha)}</td>
                        <td>
                            ${a.hora_entrada ? `
                                <span class="text-success fw-semibold text-nowrap">
                                    <i class="bi bi-box-arrow-in-right me-1"></i>
                                    ${a.hora_entrada}
                                </span>
                            ` : `<span class="text-muted">—</span>`}
                        </td>
                        <td>
                            ${a.hora_salida ? `
                                <span class="text-danger fw-semibold">
                                    <i class="bi bi-box-arrow-right me-1"></i>
                                    ${a.hora_salida}
                                </span>
                            ` : `<span class="text-muted">—</span>`}
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

        })
        .catch(error => {

            console.error("Error cargando asistencias:", error);

            document.getElementById("cuerpoTablaAsistencia").innerHTML = `
                <tr>
                    <td colspan="11" class="text-center py-5">
                        <div class="text-danger">
                            <i class="bi bi-exclamation-triangle fs-2 d-block mb-2"></i>
                            <strong>No se pudieron cargar las asistencias</strong>
                            <div class="small text-muted mt-1">
                                Intente nuevamente.
                            </div>
                        </div>
                    </td>
                </tr>
            `;
        });
}


function formatearFecha(fecha) {

    if (!fecha) {
        return "--/--/--";
    }

    const [anio, mes, dia] = fecha.split("-");

    return `${dia}/${mes}/${anio}`;
}


cargarAsistencias();
