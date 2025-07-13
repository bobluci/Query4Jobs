// Variables globales
let currentData = null
const charts = {}

// Event Listeners
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("jobSearchForm")
  form.addEventListener("submit", handleFormSubmit)
  loadCourseraCourses() // Cargar cursos de Coursera al cargar la página
})

function handleFormSubmit(event) {
  event.preventDefault()

  const jobPosition = document.getElementById("jobPosition").value
  const country = document.getElementById("country").value

  if (!jobPosition || !country) {
    showError("Por favor selecciona un puesto y un país.")
    return
  }

  searchJobData(jobPosition, country)
}

function searchJobData(jobPosition, country) {
  showLoading()
  hideError()
  hideResults()

  loadRealData(jobPosition, country)
    .then((data) => {
      if (data) {
        displayResults(data)
      } else {
        showError(
          `No se encontraron datos para "${jobPosition}" en "${country}". Por favor, asegúrate de:
          1. Haber ejecutado 'python data_collector.py' para generar los archivos JSON.
          2. Estar ejecutando la aplicación a través de un servidor web local (ej. http://localhost:8000), no directamente desde el archivo.`,
        )
      }
    })
    .catch((error) => {
      console.error("Error al obtener los datos:", error)
      showError(
        `Error al cargar los datos. Esto puede deberse a la política de seguridad del navegador (CORS) al abrir el archivo directamente.
        Por favor, asegúrate de:
        1. Haber ejecutado 'python data_collector.py' para generar los archivos JSON.
        2. Estar ejecutando la aplicación a través de un servidor web local (ej. http://localhost:8000), no directamente desde el archivo.
        (Detalles técnicos en la consola del navegador)`,
      )
    })
    .finally(() => {
      hideLoading()
    })
}

async function loadRealData(jobPosition, country) {
  const filename = `data/data_${jobPosition.replace(/\s+/g, "_")}_${country.replace(/\s+/g, "_")}.json`
  try {
    const response = await fetch(filename)

    if (response.ok) {
      return await response.json()
    }
    // Si la respuesta no es OK (ej. 404 Not Found), retorna null
    console.warn(`Archivo no encontrado o error HTTP para ${filename}: ${response.status} ${response.statusText}`)
    return null
  } catch (error) {
    // Esto captura errores de red o CORS
    console.error(`Error al cargar el archivo ${filename}:`, error)
    return null
  }
}
