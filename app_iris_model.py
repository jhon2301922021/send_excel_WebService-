# Importamos las bibliotecas necesarias
import uvicorn
from fastapi import FastAPI, File, UploadFile, Depends #`fastapi` es una biblioteca para construir APIs rápidas en Python
import pandas as pd
from pydantic import BaseModel #`pydantic` es una biblioteca que permite la validación de datos en Python
import tempfile  # Biblioteca para crear archivos temporales
import shutil  # Biblioteca para copiar archivos
import joblib

# Crear una instancia de la aplicación FastAPI
app = FastAPI()

# Definir un endpoint para manejar la subida de archivos Excel
@app.post("/upload-excel")
def upload_excel(file: UploadFile = File(...)):
    try:
        # Crear un archivo temporal para manejar el archivo subido
        with tempfile.TemporaryFile() as temp_file:
            # Copiar el contenido del archivo subido al archivo temporal
            shutil.copyfileobj(file.file, temp_file)

            # Volver al principio del archivo temporal
            temp_file.seek(0)

            # Leer el archivo Excel usando pandas y almacenarlo en un DataFrame
            df = pd.read_excel(temp_file)

            # Cargar el modelo
            loaded_model = joblib.load('iris_model.joblib')

            # Realizar predicciones con el modelo cargado
            new_predictions = loaded_model.predict(df.values)

            # Retornar las predicciones
            return {"predictions": new_predictions.tolist()}
    except Exception as e:
        # Retornar un mensaje de error si ocurre alguna excepción
        return {"error": f"Ocurrió un error: {str(e)}"}

# Ejecutar la aplicación FastAPI
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
