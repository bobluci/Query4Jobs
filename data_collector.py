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
