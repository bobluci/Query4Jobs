# 🔍 Query4Jobs

**Query4Jobs** es una aplicación web interactiva desarrollada para realizar un análisis comparativo de oportunidades laborales en **Estadística** y **Ciencia de Datos** a nivel internacional. El proyecto permite filtrar por puesto y país, visualizar métricas clave mediante gráficos dinámicos y explorar cursos recomendados en Coursera para fortalecer la formación profesional.

---

## 💡 Objetivos del proyecto

- Facilitar el análisis del mercado laboral en campos estadísticos y relacionados con ciencia de datos.
- Visualizar de manera intuitiva tendencias salariales, tecnologías demandadas y experiencia requerida.
- Recomendar formación especializada mediante cursos populares disponibles en Coursera.

---

## 🚀 Funcionalidades principales

### 🧭 Búsqueda personalizada
- Filtrado por **puesto de trabajo especializado** (más de 15 opciones) y **país extranjero**:
  - Estados Unidos 🇺🇸
  - España 🇪🇸
  - México 🇲🇽
  - Alemania 🇩🇪
  - Francia 🇫🇷

### 📊 Visualización de resultados
- Estadísticas generales:
  - Total de empleos encontrados
  - Salario promedio
  - Tecnología más mencionada

- Gráficos dinámicos generados con Chart.js:
  - 📉 Distribución salarial
  - 💻 Tecnologías más demandadas
  - 📈 Experiencia requerida
  - 🏢 Fuentes de publicación

### 📚 Panel Coursera
- Muestra cursos populares para potenciar el perfil en:
  - Python
  - SQL
  - R  
*Datos obtenidos mediante integración con SerpAPI.*

---

## 🖼️ Componentes visuales

- Formulario con validación
- Indicador de carga animado
- Panel de resultados ocultable
- Sección de errores personalizada
- Lista dinámica de empleos
- Panel de formación con categorías de cursos

---

## 🛠️ Tecnologías utilizadas

| Componente     | Tecnología                  |
|----------------|-----------------------------|
| Frontend       | HTML, CSS, JavaScript       |
| Visualización  | Chart.js                    |
| Backend        | Python                      |
| Datos externos | Jooble, Adzuna, SerpAPI     |

---


## 👥 Integrantes del equipo

- **Zavaleta Mamani Juan**
- **Carbajal Falcón Lucía**
- **Ojeda Machuca Laura**

---

## 📁 Salida de datos

Los reportes generados se almacenan en formato `.json`, organizados por puesto y país para su reutilización o análisis externo.

---

## 📌 Créditos de fuentes

- [Jooble](https://www.jooble.org/)
- [Adzuna](https://www.adzuna.com/)
- [Coursera](https://www.coursera.org/) (vía [SerpAPI](https://serpapi.com/))

---

> Hecho con dedicación por estudiantes de la carrera de Estadística Informática - Universidad Nacional Agraria La Molina ✨
