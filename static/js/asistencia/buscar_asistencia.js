document.getElementById("btnBuscar").addEventListener("click", function () {
    const dni = document.getElementById("dniBuscar").value.trim();

    if (!dni) {
        alert("Ingrese un DNI");
        return;
    }

    fetch(`/api/asistencias/buscar/${dni}`)
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert("Error: " + data.error);
                document.getElementById("datosTrabajador").classList.add("d-none");
                return;
            }

            document.getElementById("infoTrabajadorId").value = data.id;
            document.getElementById("infoDni").value = data.dni;
            document.getElementById("infoNombres").value = data.nombres;
            document.getElementById("infoApellidos").value = data.apellidos;
            document.getElementById("infoCargo").value = data.cargo ?? "";
            document.getElementById("infoObra").value = "";

            document.getElementById("datosTrabajador").classList.remove("d-none");
        })
        .catch(err => console.error("Error al buscar:", err));
});