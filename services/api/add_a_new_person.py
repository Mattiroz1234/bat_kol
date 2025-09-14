from typing import Literal, List
from fastapi import FastAPI
from pydantic import BaseModel, Field
from
from typing import Optional
import uvicorn

app = FastAPI()


class AddPerson(BaseModel):
    first_name: str = Field(..., description="שם פרטי של המשתמש")
    last_name: str = Field(..., description="שם משפחה של המשתמש")
    age: int = Field(..., ge=18, le=120, description="גיל המשתמש, חייב להיות בין 18 ל-120")
    location: str = Field(..., description="עיר מגורים")
    gender: Literal["Male", "Female"] = Field(..., description="מגדר של המשתמש")  # Male=זכר, Female=נקבה
    marital_status: Literal["Single", "Divorced", "Widower"] = Field(...,description="מצב משפחתי")  # Single=רווק, Divorced=גרוש, Widower=אלמן
    origin: Literal["ספרדי", "אשכנזי", "תימני"] = Field(..., description="מוצא אתני של המשתמש")
    sector: Literal["חסידי", "ליטאי", "ספרדי"] = Field(..., description="מגזר של המשתמש")
    occupation: Optional[str] = Field(None, description="עיסוק של המשתמש (אופציונלי)")
    favorites: Optional[List[str]] = Field(None, description="תחביבים או דברים אהובים (אופציונלי)")
    photo: Optional[str] = Field(None, description="קישור או נתיב לתמונה של המשתמש")
    height: Optional[int] = Field(None, description="גובה המשתמש ")
    free_text_self: str = Field(..., description="טקסט חופשי על המשתמש")
    free_text_for_search: str = Field(..., description="טקסט חופשי לשימוש בחיפוש/התאמה")



database = []

@app.post("/add_person")
def add_person(person: AddPerson):
    database.append(person)
    person_json = person.dict()

    return {"message": "Person added successfully", "person": person_json}


@app.get("/people")
def get_people():
    return database


if __name__ == "__main__":
    uvicorn.run("add_a_new_person:app", host="127.0.0.1", port=8000, reload=True)