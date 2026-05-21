from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Base de datos en memoria
tareas = []
contador = 1

# Modelo de tarea
class Tarea(BaseModel):
    titulo: str
    descripcion: Optional[str] = ""
    completada: bool = False

# GET — ver todas las tareas
@app.get("/tareas")
def obtener_tareas():
    return tareas

# GET — ver una tarea por ID
@app.get("/tareas/{id}")
def obtener_tarea(id: int):
    for tarea in tareas:
        if tarea["id"] == id:
            return tarea
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

# POST — crear una tarea nueva
@app.post("/tareas")
def crear_tarea(tarea: Tarea):
    global contador
    nueva = {"id": contador, **tarea.dict()}
    tareas.append(nueva)
    contador += 1
    return nueva

# PUT — actualizar una tarea completa
@app.put("/tareas/{id}")
def actualizar_tarea(id: int, tarea: Tarea):
    for i, t in enumerate(tareas):
        if t["id"] == id:
            tareas[i] = {"id": id, **tarea.dict()}
            return tareas[i]
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

# PATCH — marcar como completada
@app.patch("/tareas/{id}")
def completar_tarea(id: int):
    for tarea in tareas:
        if tarea["id"] == id:
            tarea["completada"] = True
            return tarea
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

# DELETE — borrar una tarea
@app.delete("/tareas/{id}")
def borrar_tarea(id: int):
    for i, t in enumerate(tareas):
        if t["id"] == id:
            tareas.pop(i)
            return {"mensaje": "Tarea borrada"}
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

