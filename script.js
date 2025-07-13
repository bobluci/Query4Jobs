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

// Generación de gráficos
function createCharts(data) {
  // Destruir gráficos existentes
  Object.values(charts).forEach((chart) => {
    if (chart) chart.destroy()
  })

  // Gráfico de salarios
  if (data.salary_stats.count > 0) {
    createSalaryChart(data.salary_stats, data.currency_symbol, data.currency_code)
  }

  // Gráfico de tecnologías
  createTechChart(data.top_technologies)

  // Gráfico de experiencia
  if (data.experience_stats.count > 0) {
    createExperienceChart(data.experience_stats)
  }

  // Gráfico de fuentes
  createSourceChart(data.jobs_sample)
}

function createSalaryChart(salaryStats, currencySymbol, currencyCode) {
  const ctx = document.getElementById("salaryChart").getContext("2d")

  charts.salary = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Mínimo", "Promedio", "Mediana", "Máximo"],
      datasets: [
        {
          label: `Salario (${currencyCode})`,
          data: [salaryStats.min, salaryStats.mean, salaryStats.median, salaryStats.max],
          backgroundColor: [
            "rgba(255, 99, 132, 0.8)",
            "rgba(54, 162, 235, 0.8)",
            "rgba(255, 205, 86, 0.8)",
            "rgba(75, 192, 192, 0.8)",
          ],
          borderColor: [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(255, 205, 86, 1)",
            "rgba(75, 192, 192, 1)",
          ],
          borderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: (value) => `${currencySymbol}${value.toLocaleString()}`,
          },
        },
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: (context) => `${context.dataset.label}: ${currencySymbol}${context.parsed.y.toLocaleString()}`,
          },
        },
      },
    },
  })
}

function createTechChart(technologies) {
  const ctx = document.getElementById("techChart").getContext("2d")

  const labels = Object.keys(technologies).slice(0, 8)
  const data = Object.values(technologies).slice(0, 8)

  charts.tech = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Menciones",
          data: data,
          backgroundColor: "rgba(102, 126, 234, 0.8)",
          borderColor: "rgba(102, 126, 234, 1)",
          borderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: "y", // Esto hace que sea horizontal
      scales: {
        x: {
          beginAtZero: true,
        },
      },
    },
  })
}

function createExperienceChart(experienceStats) {
  const ctx = document.getElementById("experienceChart").getContext("2d")

  const labels = Object.keys(experienceStats.distribution).map((year) => `${year} años`)
  const data = Object.values(experienceStats.distribution)

  charts.experience = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: labels,
      datasets: [
        {
          data: data,
          backgroundColor: [
            "rgba(255, 99, 132, 0.8)",
            "rgba(54, 162, 235, 0.8)",
            "rgba(255, 205, 86, 0.8)",
            "rgba(75, 192, 192, 0.8)",
            "rgba(153, 102, 255, 0.8)",
            "rgba(255, 159, 64, 0.8)",
          ],
          borderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "bottom",
        },
      },
    },
  })
}

function createSourceChart(jobsSample) {
  const ctx = document.getElementById("sourceChart").getContext("2d")

  const sources = {}
  jobsSample.forEach((job) => {
    sources[job.source] = (sources[job.source] || 0) + 1
  })

  charts.source = new Chart(ctx, {
    type: "pie",
    data: {
      labels: Object.keys(sources),
      datasets: [
        {
          data: Object.values(sources),
          backgroundColor: ["rgba(102, 126, 234, 0.8)", "rgba(118, 75, 162, 0.8)", "rgba(255, 99, 132, 0.8)"],
          borderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "bottom",
        },
      },
    },
  })
}
