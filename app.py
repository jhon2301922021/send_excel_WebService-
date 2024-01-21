# Importamos las bibliotecas necesarias
import uvicorn 
from fastapi import FastAPI, File, UploadFile, Depends
import pandas as pd
from pydantic import BaseModel
import tempfile  # Biblioteca para crear archivos temporales
import shutil  # Biblioteca para copiar archivos

# Crear una instancia de la aplicación FastAPI
app = FastAPI()

class User(BaseModel):
    user_name: str

# Definir un endpoint para manejar la subida de archivos Excel
@app.post("/upload-excel")
def upload_excel(file: UploadFile = File(...), user: User = Depends()):
    try:
        # Crear un archivo temporal para manejar el archivo subido
        with tempfile.TemporaryFile() as temp_file:
            # Copiar el contenido del archivo subido al archivo temporal
            shutil.copyfileobj(file.file, temp_file)

            # Volver al principio del archivo temporal
            temp_file.seek(0)
            # Leer el archivo Excel usando pandas y lo almacenarlo en un DataFrame
            df = pd.read_excel(temp_file)

            # Imprimir el nombre del usuario que ha mandado el archivo
            print('User: ' + user.dict()['user_name'])

            # Imprimir las primeras filas del DataFrame como ejemplo
            print(df.head())  

            # Retornar un mensaje de éxito
            return {"message": "El archivo Excel se ha subido correctamente!"}
    except Exception as e:
        # Retornar un mensaje de error si ocurre alguna excepción
        return {"error": f"Ocurrió un error: {str(e)}"}

# Ejecutar la aplicación FastAPI
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
