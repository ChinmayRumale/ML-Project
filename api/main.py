# This file defines FastAPI app with prediction, health check and frontend endpoints

from fastapi import FastAPI, HTTPException  # fastapi framework
from fastapi.staticfiles import StaticFiles  # serve static files
from fastapi.templating import Jinja2Templates  # serve html templates
from fastapi.requests import Request  # request object
from fastapi.responses import HTMLResponse  # html response
from pydantic import BaseModel  # request body validation
import sys  # system path manipulation
import os  # access env variables
from dotenv import load_dotenv  # load env variables

load_dotenv()  # load .env file

current_dir = os.path.dirname(os.path.abspath(__file__))

# add project root to path so ml package imports work
sys.path.append(os.path.abspath(os.path.join(current_dir, '..')))

from ml.predict import predict  # import predict function

app = FastAPI(
    title="Online Shoppers Intention API",
    description="Predicts if a shopper will purchase or not",
    version="1.0.0"
)

# mount static files directory
app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")

# setup jinja2 templates
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))

# define input schema
class ShopperInput(BaseModel):
    Administrative: int
    Administrative_Duration: float
    Informational: int
    Informational_Duration: float
    ProductRelated: int
    ProductRelated_Duration: float
    BounceRates: float
    ExitRates: float
    PageValues: float
    SpecialDay: float
    Month: int
    OperatingSystems: int
    Browser: int
    Region: int
    TrafficType: int
    VisitorType: int
    Weekend: int

# define output schema
class PredictionOutput(BaseModel):
    prediction: int
    probability: float
    message: str

@app.get("/", response_class=HTMLResponse)  # serve frontend
def frontend(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")  # health check endpoint
def health():
    return {"status": "healthy"}

@app.post("/predict", response_model=PredictionOutput)  # prediction endpoint
def predict_endpoint(data: ShopperInput):
    try:
        input_dict = data.model_dump()  # convert to dict
        result = predict(input_dict)    # run prediction
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))