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

// Las funciones displayResults, createCharts, createSalaryChart, createTechChart,
// createExperienceChart, createSourceChart, displayJobsList, showLoading,
// hideLoading, showResults, hideResults, showError, hideError, debugSearch
// permanecen sin cambios.

// Visualización de resultados
function displayResults(data) {
  currentData = data

  // Actualizar resumen
  document.getElementById("resultsTitle").textContent = `Análisis: ${data.job_title} en ${data.country}`

  // Mostrar el total de empleos
  document.getElementById("totalJobs").textContent = data.total_jobs

  // Mostrar el salario promedio con símbolo y código de moneda
  if (data.salary_stats.count > 0) {
    document.getElementById("avgSalary").textContent =
      `${data.currency_symbol}${data.salary_stats.mean.toLocaleString()} ${data.currency_code}`
  } else {
    document.getElementById("avgSalary").textContent = "N/A"
  }

  const topTech = Object.keys(data.top_technologies)[0] || "N/A"
  document.getElementById("topTech").textContent = topTech

  // Crear gráficos
  createCharts(data)

  // Mostrar lista de empleos
  displayJobsList(data.jobs_sample, data.currency_symbol, data.currency_code)

  showResults()
}
