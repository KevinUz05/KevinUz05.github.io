# Proyecto Integrador 2026A: Predicción de Rendimiento Académico

## Descripción del Proyecto
Este repositorio contiene el desarrollo completo del Proyecto Integrador del semestre 2026A para la carrera de Inteligencia Artificial y Ciencia de Datos. El objetivo principal es analizar y predecir el rendimiento académico de estudiantes universitarios (Promedio General y Calificaciones Internas) a partir de sus hábitos de vida y comportamiento diario (horas de estudio, sueño, tiempo en pantalla, nivel de estrés, asistencia, entre otros).

## Equipo de Desarrollo
* Fátima Sofía García de León Torres
* Miguel Angel Magaña Solís
* Sophia Díaz de León Gleason
* Kevin Uziel García Márquez

## Tecnologías y Herramientas
* **Lenguaje:** Python 3
* **Machine Learning:** Scikit-Learn, Pandas, NumPy
* **Backend y API:** FastAPI, Uvicorn y Render
* **Base de Datos:** MongoDB Atlas (NoSQL)
* **Entorno de Trabajo:** Jupyter Notebooks

## Modelos de Machine Learning Implementados
Se entrenaron y compararon cuatro algoritmos principales para abordar el problema desde diferentes perspectivas:
1. **Regresión Lineal Múltiple:** Utilizada para la predicción continua de calificaciones y establecer las relaciones lineales entre hábitos y desempeño.
2. **Regresión Logística:** Adaptada para la tarea de clasificación de riesgo académico, determinando la probabilidad de que un alumno apruebe o repruebe.
3. **Support Vector Machine (SVR):** Implementada para capturar fronteras de decisión complejas y fuertemente no lineales (ej. picos de estrés vs rendimiento), siendo muy robusta ante valores atípicos.
4. **Árboles de Decisión:** Empleados por su alta interpretabilidad para extraer reglas jerárquicas claras sobre el comportamiento de los datos.

## Análisis Estadístico y Fundamentos Matemáticos
El proyecto no se limita a la ejecución de código, sino que justifica matemáticamente cada decisión:
* **Probabilidad y Estadística:** Uso de pruebas de inferencia clásica, como la prueba T-Student pareada (para evaluar el desbalance entre horas de estudio y tiempo en pantalla) y Análisis de Varianza (ANOVA) para medir el impacto real del estrés.
* **Complejidad Computacional:** Análisis profundo del costo algorítmico ($O(nd^2)$) de la Ecuación Normal frente a métodos numéricamente más estables como la Descomposición de Valores Singulares (SVD) y Factorización QR utilizados internamente por Scikit-Learn, previniendo el colapso del sistema con grandes volúmenes de datos.
* **Matemáticas Aplicadas:** Evaluación de las funciones de costo (MSE para regresión y Entropía Cruzada para clasificación), así como la vigilancia estricta de la multicolinealidad mediante el Factor de Inflación de Varianza (VIF).

## Arquitectura del Sistema y Base de Datos
El modelo predictivo ganador fue integrado en un pipeline estandarizado de Scikit-Learn (incluyendo `OneHotEncoder` para el manejo de variables categóricas) y serializado en el archivo `model_pipeline.pkl`. 

Para su puesta en producción, se construyó una **API REST asíncrona con FastAPI** que consume este modelo. Las interacciones de los usuarios y el historial de predicciones se almacenan de manera dinámica y escalable en una base de datos en la nube utilizando **MongoDB Atlas**.

## Archivos Principales
* `main.py`: Código fuente del backend (FastAPI) que expone las rutas de la API.
* `model_pipeline.pkl`: Modelo de Machine Learning pre-entrenado y listo para inferencia.
* `*_students.ipynb`: Notebooks detallados con la limpieza de datos y el entrenamiento de los distintos modelos (Lineal, Logística, SVR).
* `Proyecto_*.ipynb`: Notebooks dedicados a los reportes teóricos de las materias transversales (Probabilidad, Complejidad Computacional y Matemáticas Aplicadas).
* `PROYECTO INTEGRADOR_Bases de datos.docx`: Documentación de la arquitectura NoSQL y el diagrama de flujo de datos.

## Instrucciones de Instalación y Uso Local

1. **Clonar el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd <nombre-del-directorio>
