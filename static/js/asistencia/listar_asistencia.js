function cargarAsistencias(fechaInicio, fechaFin) {
    let url = "/api/asistencias";
    const params = [];
    if (fechaInicio) params.push(`fecha_inicio=${fechaInicio}`);
    if (fechaFin) params.push(`fecha_fin=${fechaFin}`);
    if (params.length) url += "?" + params.join("&");

    fetch(url)
        .then(res => res.json())
        .then(data => {
            const cuerpo = document.getElementById("cuerpoTablaAsistencia");
            cuerpo.innerHTML = "";

            if (data.length === 0) {
                cuerpo.innerHTML = `<tr><td colspan="12" class="text-center text-muted">Sin registros en este rango de fechas</td></tr>`;
                return;
            }

            data.forEach(a => {
                const botonEntrada = !a.hora_entrada
                    ? `<button class="btn btn-sm btn-primary" onclick="marcarEntrada(${a.id})">Entrada</button>`
                    : "";

                const botonSalida = (a.hora_entrada && !a.hora_salida)
                    ? `<button class="btn btn-sm btn-warning" onclick="marcarSalida(${a.id})">Salida</button>`
                    : "";

                const acciones = (botonEntrada || botonSalida)
                    ? `${botonEntrada} ${botonSalida}`
                    : `<span class="badge bg-success">✅ Jornada completa</span>`;

                const fotoEntradaBtn = a.foto_entrada
                    ? `<button class="btn btn-sm btn-outline-secondary" onclick="verMarcado('Entrada', '/static/${a.foto_entrada}', ${a.lat_entrada}, ${a.lng_entrada})">📷</button>`
                    : "—";
                const fotoSalidaBtn = a.foto_salida
                    ? `<button class="btn btn-sm btn-outline-secondary" onclick="verMarcado('Salida', '/static/${a.foto_salida}', ${a.lat_salida}, ${a.lng_salida})">📷</button>`
                    : "—";

                const mapaEntrada = (a.lat_entrada && a.lng_entrada)
                    ? `<a href="https://www.google.com/maps?q=${a.lat_entrada},${a.lng_entrada}" target="_blank">Entrada</a>`
                    : "—";
                const mapaSalida = (a.lat_salida && a.lng_salida)
                    ? `<a href="https://www.google.com/maps?q=${a.lat_salida},${a.lng_salida}" target="_blank">Salida</a>`
                    : "—";

                cuerpo.innerHTML += `
                    <tr>
                        <td>${a.dni}</td>
                        <td>${a.nombres}</td>
                        <td>${a.apellidos}</td>
                        <td>${a.obra ?? ""}</td>
                        <td>${a.cargo ?? ""}</td>
                        <td>${a.fecha}</td>
                        <td>${a.hora_entrada || "—"}</td>
                        <td>${a.hora_salida || "—"}</td>
                        <td>${a.estado}</td>
                        <td>${fotoEntradaBtn} ${fotoSalidaBtn}</td>
                        <td>${mapaEntrada} / ${mapaSalida}</td>
                        <td>${acciones}</td>
                    </tr>`;
            });
        });
}

cargarAsistencias();