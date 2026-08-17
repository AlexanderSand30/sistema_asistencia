document.getElementById("btnBuscarReporte").addEventListener("click", function () {
    const inicio = document.getElementById("fechaInicio").value;
    const fin = document.getElementById("fechaFin").value;
    const dni = document.getElementById("dniReporte").value.trim();
    const cuerpo = document.getElementById("cuerpoTablaReporte");
    const totalResultados = document.getElementById("totalResultados");

    if (!inicio || !fin) {
        alert("Selecciona la fecha de inicio y fecha fin");
        return;
    }

    let url = `/api/reportes?inicio=${inicio}&fin=${fin}`;
    if (dni) url += `&dni=${dni}`;

    cuerpo.innerHTML = `<tr><td colspan="9" class="text-center text-muted">Cargando...</td></tr>`;

    fetch(url)
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                cuerpo.innerHTML = `<tr><td colspan="9" class="text-center text-danger">${data.error}</td></tr>`;
                totalResultados.textContent = "";
                return;
            }

            if (data.length === 0) {
                cuerpo.innerHTML = `<tr><td colspan="9" class="text-center text-muted">Sin registros en este rango</td></tr>`;
                totalResultados.textContent = "";
                return;
            }

            cuerpo.innerHTML = "";
            data.forEach(r => {
                cuerpo.innerHTML += `
                    <tr>
                        <td>${r.dni}</td>
                        <td>${r.nombres}</td>
                        <td>${r.apellidos}</td>
                        <td>${r.obra ?? ""}</td>
                        <td>${r.cargo ?? ""}</td>
                        <td>${r.fecha}</td>
                        <td>${r.hora_entrada}</td>
                        <td>${r.hora_salida}</td>
                        <td>${r.estado}</td>
                    </tr>`;
            });

            totalResultados.textContent = `${data.length} registro(s) encontrado(s)`;
        })
        .catch(err => {
            cuerpo.innerHTML = `<tr><td colspan="9" class="text-center text-danger">Error al cargar los datos</td></tr>`;
            console.error(err);
        });
});