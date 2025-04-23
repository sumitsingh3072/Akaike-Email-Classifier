from fastapi import FastAPI, Request
from pydantic import BaseModel
from utils import mask_pii, restore_pii
from models import load_model, predict_category
from logger import logger
import uvicorn

app = FastAPI()

model = load_model()
logger.info("Loaded email classification model.")

class EmailRequest(BaseModel):
    email_body: str

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

@app.post("/classify/")
def classify_email(request: EmailRequest) -> dict:
    original_email = request.email_body
    logger.info("Received email for classification.")

    # Mask PII
    masked_email, entities = mask_pii(original_email)
    logger.debug(f"Masked email: {masked_email}")
    logger.debug(f"Masked entities: {entities}")

    # category with local model
    category = predict_category(model, masked_email)
    logger.info(f"Predicted category: {category}")

    #Restore PII in masked email
    demasked_email = restore_pii(masked_email, entities)

    return {
        "input_email_body": original_email,
        "list_of_masked_entities": entities,
        "masked_email": masked_email,
        "category_of_the_email": category
    }