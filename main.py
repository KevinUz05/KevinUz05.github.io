from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
import joblib
import pandas as pd
import traceback
import os
from dotenv import load_dotenv  # <-- Importamos esto

app = FastAPI(title="Predicción de Notas Internas (Internal Marks)")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite que tu archivo HTML se conecte
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ... (tus importaciones) ...

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
# Leemos los nombres del .env. Si por alguna razón no los encuentra, 
# usa "school_project" y "students" como plan de respaldo por defecto.
DB_NAME = os.getenv("MONGODB_DB", "school_project")
COLLECTION_NAME = os.getenv("MONGODB_COLLECTION", "students")

# --- CONEXIÓN A BASE DE DATOS ---
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Para comprobar que sí se conectó a Atlas al iniciar el servidor
try:
    client.admin.command('ping')
    print("✅ ¡Conectado exitosamente a MongoDB Atlas!")
except Exception as e:
    print(f"❌ Error al conectar a MongoDB Atlas: {e}")

# ... (Aquí sigue el resto de tu código igual: CARGAR EL MODELO, FEATURES_ORDER, etc.) ...
# --- 2. CARGAR EL MODELO ---
try:
    model = joblib.load('model_pipeline.pkl')
except Exception as e:
    model = None
    print(f"Error crítico al cargar el modelo: {e}")

# --- 3. ORDEN EXACTO DE LAS CARACTERÍSTICAS (X) ---
# NOTA: Aquí debes poner EXACTAMENTE las mismas columnas que usaste en tu X_train.
# Si en tu notebook también eliminaste "CGPA", quítala de esta lista.
FEATURES_ORDER = [
    "Age", 
    "Branch", 
    "Study_Hours_per_Day", 
    "Sleep_Hours", 
    "Screen_Time_Hours", 
    "Gym_Hours_per_Week", 
    "Diet_Type", 
    "Attendance_Percentage", 
    "Stress_Level_1_to_10", 
    "Residence",
    "CGPA"  # Déjala aquí solo si la usaste como característica en tu X_train
]

# --- 4. ESQUEMA DE VALIDACIÓN (Sin Internal_Marks) ---
class StudentInput(BaseModel):
    Age: int
    Branch: str
    Study_Hours_per_Day: float
    Sleep_Hours: float
    Screen_Time_Hours: float
    Gym_Hours_per_Week: float
    Diet_Type: str
    Attendance_Percentage: float
    Stress_Level_1_to_10: int
    Residence: str
    CGPA: float  # El usuario ingresa su CGPA actual para predecir su Internal Mark

# --- 5. RUTA POST ---
@app.post("/students/")
def create_and_predict(student: StudentInput):
    if model is None:
        raise HTTPException(status_code=500, detail="El modelo no está disponible en el servidor.")
    
    try:
        # Convertir datos de la petición a diccionario
        student_data = student.model_dump()
        
        # Crear el DataFrame con los datos de entrada
        df_input = pd.DataFrame([student_data])
        
        # Forzar el orden y las columnas exactas que el modelo espera (Excluye Internal_Marks)
        df_input = df_input[FEATURES_ORDER]
        
        # Hacer la predicción de Internal_Marks
        prediction = model.predict(df_input)[0]
        
        # Guardar la predicción en el diccionario que irá a la base de datos
        student_data["Predicted_Internal_Marks"] = round(float(prediction), 2)
        
        # Guardar el registro completo en MongoDB
        new_student = collection.insert_one(student_data)
        
        return {
            "status": "success",
            "student_id": str(new_student.inserted_id),
            "predicted_internal_marks": student_data["Predicted_Internal_Marks"]
        }
        
    except Exception as e:
        print("--- ERROR EN EL PROCESAMIENTO DEL POST ---")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error en el modelo/backend: {str(e)}")
    
    # --- HELPER PARA FORMATEAR EL ID DE MONGO ---
def format_student(student) -> dict:
    student["_id"] = str(student["_id"])
    return student

# --- RUTA PARA OBTENER EL HISTORIAL (GET) ---
@app.get("/students/")
def get_students():
    try:
        students = []
        # Buscamos todos los registros en Atlas
        for student in collection.find():
            students.append(format_student(student))
        return students
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer la base de datos: {str(e)}")

# --- RUTA PARA BORRAR UN ALUMNO (DELETE) ---
@app.delete("/students/{id}")
def delete_student(id: str):
    # Verificamos que el ID tenga el formato correcto de MongoDB
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
        
    try:
        delete_result = collection.delete_one({"_id": ObjectId(id)})
        if delete_result.deleted_count == 1:
            return {"message": "Estudiante borrado exitosamente"}
        raise HTTPException(status_code=404, detail="Estudiante no encontrado en Atlas")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al intentar borrar: {str(e)}")