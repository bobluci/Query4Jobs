import requests
import json
import time
from collections import Counter
import statistics
import re
from serpapi import GoogleSearch # Importar SerpAPI
import os # Importar el módulo os para manejar directorios

class JobDataCollector:
    def __init__(self):
        # Estas serán reemplazadas por las keys del usuario
        self.adzuna_app_id = "dee26963"
        self.adzuna_api_key = "35151c1fa3ff894e91e7b31d23b94e8f"
        self.jooble_api_key = "62bbe709-afe6-4ea1-b045-1be6ef5182a4"
        self.serpapi_api_key = "6213895854758679f17705210a17960c30d7d2430c57c5bd1e0b667e66a192aa" # Tu API Key de SerpAPI
        
        # Directorio donde se guardarán los archivos JSON
        self.data_output_dir = "data"
        # Crear el directorio si no existe
        os.makedirs(self.data_output_dir, exist_ok=True)

        # Mapeo de países para las APIs (código de país)
        self.countries = {
            "EEUU": {"adzuna": "us", "jooble": "us"},
            "España": {"adzuna": "es", "jooble": "es"},
            "México": {"adzuna": "mx", "jooble": "mx"},
            "Alemania": {"adzuna": "de", "jooble": "de"},
            "Francia": {"adzuna": "fr", "jooble": "fr"}
        }
        
        # Mapeo de idiomas para cada país
        self.language_map = {
            "EEUU": "en",
            "España": "es",
            "México": "es",
            "Alemania": "de",
            "Francia": "fr"
        }

        # Mapeo de monedas para cada país
        self.currency_map = {
            "EEUU": {"symbol": "$", "code": "USD"},
            "España": {"symbol": "€", "code": "EUR"},
            "México": {"symbol": "$", "code": "MXN"},
            "Alemania": {"symbol": "€", "code": "EUR"},
            "Francia": {"symbol": "€", "code": "EUR"}
        }
        
        # Puestos de trabajo relacionados con estadística (en español)
        self.job_positions = [
            "Analista de datos",
            "Científico de datos",
            "Ingeniero estadístico",
            "Especialista en inteligencia de negocios",
            "Analista de riesgos",
            "Especialista en bioestadística",
            "Ingeniero de machine learning",
            "Analista actuarial",
            "Especialista en analítica predictiva",
            "Ingeniero en calidad estadística",
            "Consultor estadístico",
            "Data engineer",
            "Especialista en visualización de datos",
            "Analista de investigación de mercado",
            "Especialista en estadística computacional"
        ]

        # Traducciones de puestos de trabajo (simple, para los idiomas soportados)
        self.job_title_translations = {
            "Analista de datos": {"en": "Data Analyst", "de": "Datenanalyst", "fr": "Analyste de données"},
            "Científico de datos": {"en": "Data Scientist", "de": "Datenwissenschaftler", "fr": "Scientifique de données"},
            "Ingeniero estadístico": {"en": "Statistical Engineer", "de": "Statistiker Ingenieur", "fr": "Ingénieur statisticien"},
            "Especialista en inteligencia de negocios": {"en": "Business Intelligence Specialist", "de": "Business Intelligence Spezialist", "fr": "Spécialiste en Business Intelligence"},
            "Analista de riesgos": {"en": "Risk Analyst", "de": "Risikoanalyst", "fr": "Analyste de risques"},
            "Especialista en bioestadística": {"en": "Biostatistics Specialist", "de": "Biostatistik Spezialist", "fr": "Spécialiste en biostatistique"},
            "Ingeniero de machine learning": {"en": "Machine Learning Engineer", "de": "Maschinelles Lernen Ingenieur", "fr": "Ingénieur en Machine Learning"},
            "Analista actuarial": {"en": "Actuarial Analyst", "de": "Aktuarischer Analyst", "fr": "Analyste actuariel"},
            "Especialista en analítica predictiva": {"en": "Predictive Analytics Specialist", "de": "Predictive Analytics Spezialist", "fr": "Spécialiste en analyse prédictive"},
            "Ingeniero en calidad estadística": {"en": "Statistical Quality Engineer", "de": "Statistischer Qualitätsingenieur", "fr": "Ingénieur qualité statistique"},
            "Consultor estadístico": {"en": "Statistical Consultant", "de": "Statistischer Berater", "fr": "Consultant statisticien"},
            "Data engineer": {"en": "Data Engineer", "de": "Dateningenieur", "fr": "Ingénieur de données"},
            "Especialista en visualización de datos": {"en": "Data Visualization Specialist", "de": "Datenvisualisierung Spezialist", "fr": "Spécialiste en visualisation de datos"},
            "Analista de investigación de mercado": {"en": "Market Research Analyst", "de": "Marktforschungsanalyst", "fr": "Analyste d'études de marché"},
            "Especialista en estadística computacional": {"en": "Computational Statistics Specialist", "de": "Computergestützte Statistik Spezialist", "fr": "Spécialiste en statistique computationnelle"}
        }
        
        # Tecnologías y herramientas comunes
        self.technologies = [
            "Python", "R", "SQL", "Excel", "Tableau", "Power BI", 
            "SAS", "SPSS", "Hadoop", "Spark", "TensorFlow", "Pandas",
            "NumPy", "Scikit-learn", "Matplotlib", "Seaborn", "Jupyter",
            "Git", "Docker", "AWS", "Azure", "GCP", "MongoDB", "PostgreSQL"
        ]

        # Palabras clave para buscar cursos de Coursera
        self.coursera_keywords = ["Python", "SQL", "R"]

    def _translate_job_title(self, job_title_es, target_lang):
        """Traduce el título del puesto si es necesario."""
        if target_lang == "es":
            return job_title_es
        return self.job_title_translations.get(job_title_es, {}).get(target_lang, job_title_es)

    def search_adzuna_jobs(self, job_title, country_code, max_results=50):
        """Buscar empleos en Adzuna API"""
        url = f"https://api.adzuna.com/v1/api/jobs/{country_code}/search/1"
        
        params = {
            'app_id': self.adzuna_app_id,
            'app_key': self.adzuna_api_key,
            'what': job_title,
            'results_per_page': min(max_results, 50),
            'sort_by': 'relevance'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error Adzuna ({country_code}): {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error conectando a Adzuna ({country_code}): {e}")
            return None

    def search_jooble_jobs(self, job_title, country_code, max_results=50):
        """Buscar empleos en Jooble API"""
        url = "https://jooble.org/api/" + self.jooble_api_key
        
        payload = {
            "keywords": job_title,
            "location": country_code,
            "page": "1"
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error Jooble ({country_code}): {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error conectando a Jooble ({country_code}): {e}")
            return None
# Búsqueda de cursos de Coursera--------------------------------
    def search_coursera_courses(self, keyword, num_results=5):
        """Buscar cursos de Coursera usando SerpAPI"""
        print(f"Buscando cursos de Coursera para: {keyword}")
        params = {
            "api_key": self.serpapi_api_key,
            "engine": "google",
            "q": f"{keyword} courses site:coursera.org", # Buscar en Coursera.org
            "num": num_results, # Número de resultados por página
            "hl": "es", # Idioma de los resultados (español)
            "gl": "us" # Ubicación geográfica para la búsqueda (genérico)
        }
        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            courses = []
            if "organic_results" in results:
                for result in results["organic_results"]:
                    # Filtrar para asegurar que sean enlaces de cursos de Coursera
                    if "coursera.org/learn/" in result.get("link", "") or "coursera.org/specializations/" in result.get("link", ""):
                        courses.append({
                            "title": result.get("title"),
                            "link": result.get("link"),
                            "snippet": result.get("snippet"),
                            "source": "Coursera"
                        })
            return courses
        except Exception as e:
            print(f"Error buscando cursos de Coursera para {keyword}: {e}")
            return []
    """
    Extrae posibles valores salariales desde un texto dado.
    Busca patrones numéricos que representen montos de dinero y los filtra
    dentro de un rango razonable (entre 1,000 y 500,000).
    """

    def extract_salary_from_text(self, text):
        """Extraer información salarial del texto (simplificado para números)"""
        if not text:
            return None
            
        # Patrones para extraer números que parecen salarios
        salaries = []
        matches = re.findall(r'(\d{1,3}(?:[.,]\d{3})*(?:\.\d{2})?|\d+)', text.lower())
        
        for match in matches:
            try:
                cleaned_match = match.replace('.', '').replace(',', '') 
                salary = float(cleaned_match)
                
                if 1000 <= salary <= 500000: # Rango razonable para salarios
                    salaries.append(salary)
            except ValueError:
                continue
                    
        return salaries if salaries else None

    """
    Extrae tecnologías mencionadas en el texto.
    Compara palabras clave de tecnologías conocidas con el contenido del texto.
    """

    def extract_technologies_from_text(self, text):
        """Extraer tecnologías mencionadas en el texto"""
        if not text:
            return []
            
        found_techs = []
        text_lower = text.lower()
        
        for tech in self.technologies:
            if re.search(r'\b' + re.escape(tech.lower()) + r'\b', text_lower):
                found_techs.append(tech)
                
        return found_techs
    """
    Extrae los años de experiencia mencionados en el texto.
    Busca patrones comunes como 'X años de experiencia' o 'mínimo X años'.
    """

    def extract_experience_from_text(self, text):
        """Extraer años de experiencia del texto"""
        if not text:
            return None
            
        patterns = [
            r'(\d+)\s*(?:años?|years?)\s*(?:de\s*)?(?:experiencia|experience)',
            r'(\d+)\+\s*(?:años?|years?)',
            r'mínimo\s*(\d+)\s*(?:años?|years?)',
            r'minimum\s*(\d+)\s*(?:años?|years?)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                try:
                    years = int(matches[0])
                    if 0 <= years <= 20:
                        return years
                except:
                    continue
                    
        return None
# Análisis de datos de empleo ADZUNA------------------------------------
    def analyze_job_data(self, job_title_es, country):
        """Analizar datos de trabajo para un puesto y país específico"""
        print(f"Analizando: {job_title_es} en {country}")
        
        country_codes = self.countries.get(country, {})
        target_lang = self.language_map.get(country, "es")
        currency_info = self.currency_map.get(country, {"symbol": "$", "code": "USD"})

        if not country_codes:
            print(f"País no soportado: {country}")
            return None
            
        translated_job_title = self._translate_job_title(job_title_es, target_lang)
        print(f"Buscando '{translated_job_title}' en {country} ({target_lang})")

        all_jobs = []
        salaries = []
        technologies = []
        experience_years = []
        
        # Buscar en Adzuna
        adzuna_data = self.search_adzuna_jobs(translated_job_title, country_codes["adzuna"])
        if adzuna_data and "results" in adzuna_data:
            for job in adzuna_data["results"]:
                job_info = {
                    "title": job.get("title", ""),
                    "description": job.get("description", ""),
                    "salary_min": job.get("salary_min"),
                    "salary_max": job.get("salary_max"),
                    "company": job.get("company", {}).get("display_name", ""),
                    "location": job.get("location", {}).get("display_name", ""),
                    "source": "Adzuna"
                }
                all_jobs.append(job_info)
                
                if job_info["salary_min"]:
                    salaries.append(job_info["salary_min"])
                if job_info["salary_max"]:
                    salaries.append(job_info["salary_max"])
                    
                full_text = f"{job_info['title']} {job_info['description']}"
                technologies.extend(self.extract_technologies_from_text(full_text))
                
                exp = self.extract_experience_from_text(full_text)
                if exp:
                    experience_years.append(exp)
        
        time.sleep(1)
# Análisis de datos de empleo JOOBLE------------------------------------        
        # Buscar en Jooble
        jooble_data = self.search_jooble_jobs(translated_job_title, country_codes["jooble"])
        if jooble_data and "jobs" in jooble_data:
            for job in jooble_data["jobs"]:
                job_info = {
                    "title": job.get("title", ""),
                    "description": job.get("snippet", ""),
                    "salary_min": None,
                    "salary_max": None,
                    "company": job.get("company", ""),
                    "location": job.get("location", ""),
                    "source": "Jooble"
                }
                all_jobs.append(job_info)
                
                full_text = f"{job_info['title']} {job_info['description']}"
                text_salaries = self.extract_salary_from_text(full_text)
                if text_salaries:
                    salaries.extend(text_salaries)
                
                technologies.extend(self.extract_technologies_from_text(full_text))
                
                exp = self.extract_experience_from_text(full_text)
                if exp:
                    experience_years.append(exp)
        
        tech_counter = Counter(technologies)
        
        analysis = {
            "job_title": job_title_es,
            "country": country,
            "currency_symbol": currency_info["symbol"],
            "currency_code": currency_info["code"],
            "total_jobs": len(all_jobs),
            "salary_stats": self.calculate_salary_stats(salaries),
            "top_technologies": dict(tech_counter.most_common(10)),
            "experience_stats": self.calculate_experience_stats(experience_years),
            "jobs_sample": all_jobs[:10]
        }
        
        return analysis

# Estadísticas salariales ---------------------------------------
    def calculate_salary_stats(self, salaries):
        """Calcular estadísticas salariales"""
        if not salaries:
            return {"count": 0, "min": 0, "max": 0, "mean": 0, "median": 0, "std_dev": 0, "message": "No hay datos salariales disponibles"}
            
        return {
            "count": len(salaries),
            "min": min(salaries),
            "max": max(salaries),
            "mean": statistics.mean(salaries),
            "median": statistics.median(salaries),
            "std_dev": statistics.stdev(salaries) if len(salaries) > 1 else 0
        }
    
# Estadísticas de experiencia-----------------------------------
    def calculate_experience_stats(self, experience_years):
        """Calcular estadísticas de experiencia"""
        if not experience_years:
            return {"count": 0, "min": 0, "max": 0, "mean": 0, "median": 0, "distribution": {}, "message": "No hay datos de experiencia disponibles"}
            
        exp_counter = Counter(experience_years)
        return {
            "count": len(experience_years),
            "min": min(experience_years),
            "max": max(experience_years),
            "mean": statistics.mean(experience_years),
            "median": statistics.median(experience_years),
            "distribution": dict(exp_counter)
        }

    def generate_report(self, job_title_es, country):
        """Generar reporte completo para un puesto y país"""
        analysis = self.analyze_job_data(job_title_es, country)
        
        if analysis:
            # Guardar en archivo JSON dentro del directorio de salida
            filename = os.path.join(self.data_output_dir, f"data_{job_title_es.replace(' ', '_')}_{country.replace(' ', '_')}.json")
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(analysis, f, ensure_ascii=False, indent=2)
                print(f"✅ Reporte de empleo guardado en: {filename}")
                return analysis
            except Exception as e:
                print(f"❌ Error al guardar el reporte de empleo en {filename}: {e}")
                return None
        else:
            print(f"⚠️ No se pudo generar el reporte para {job_title_es} en {country}")
            return None
