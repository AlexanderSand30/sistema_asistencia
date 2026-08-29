document.getElementById("btnExportarPDF").addEventListener("click", function () {
  const inicio = document.getElementById("fechaInicio").value;
  const fin = document.getElementById("fechaFin").value;
  const dni = document.getElementById("dniReporte").value.trim();

  if (!inicio || !fin) {
    mostrarToast("warning", "Selecciona la fecha de inicio y fecha fin");
    return;
  }

  let url = `/reportes/pdf?inicio=${inicio}&fin=${fin}`;
  if (dni) url += `&dni=${dni}`;

  window.open(url, "_blank");
});

document.getElementById("btnExportarExcel").addEventListener("click", function () {
  const inicio = document.getElementById("fechaInicio").value;
  const fin = document.getElementById("fechaFin").value;
  const dni = document.getElementById("dniReporte").value.trim();

  if (!inicio || !fin) {
    mostrarToast("warning", "Selecciona la fecha de inicio y fecha fin");
    return;
  }

  let url = `/reportes/excel?inicio=${inicio}&fin=${fin}`;
  if (dni) url += `&dni=${dni}`;

  window.open(url, "_blank");
});
