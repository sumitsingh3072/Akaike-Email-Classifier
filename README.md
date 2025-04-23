# Akaike Email Classifier (FastAPI + ML)

This project implements and deploys a machine-learning-based backend service that classifies customer support emails into one of four categories — Incident, Request, Problem, or Change — based on the content of the email body.

It uses:
- FastAPI to serve a REST API
- Scikit-learn (TF-IDF + Logistic Regression) for classification
- PII masking and restoration utilities
- Uvicorn as the ASGI server
- Hugging Face Spaces (Docker SDK) for deployment

---

## API Deployment (Hugging Face Spaces)

### Requirements
- Dockerfile in root
- `app.py` as FastAPI entrypoint
- `requirements.txt` with all Python dependencies
- Pre-trained model `email_classifier.pkl`

### Deployment Steps

1. Create a new Space: [Hugging Face Spaces](https://huggingface.co/spaces) → choose SDK: Docker
2. Clone repo & push your project
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/email-classifier
   cd email-classifier
   # Copy your code into this folder
   git add .
   git commit -m "Initial commit"
   git push
   ```
3. Hugging Face will build & deploy your API automatically

---

## API Usage

### Endpoint
```
POST /classify/
```

### Example Request
```json
{
  "email_body": "Hi, I need access to the internal finance dashboard."
}
```

### Example Response
```json
{
  "input_email_body": "Hi, I need access to the internal finance dashboard.",
  "list_of_masked_entities": [
    { "position": [20, 26], "classification": "resource", "entity": "finance" }
  ],
  "masked_email": "Hi, I need access to the internal [resource] dashboard.",
  "category_of_the_email": "Request"
}
```

---

## Project Structure

```bash
.
├── app.py              # Entrypoint for Uvicorn (FastAPI app)
├── api.py              # All routes, classification, PII masking logic
├── models.py           # ML training, prediction, and model loader
├── utils.py            # PII masking and demasking helpers
├── logger.py           # Centralized logging config
├── train.py            # Script to train and export model
├── requirements.txt    # All required Python dependencies
├── email_classifier.pkl# Saved trained classifier
└── README.md           # Project overview
```

---

## Module Documentation

### `api.py`
- `POST /classify/`: Accepts raw email and returns classification and masking metadata
- `GET /`: Returns welcome message with usage guide (optional)
- Middleware logs every request/response

### `models.py`
- `train_email_classifier()`: Trains a Logistic Regression model using TF-IDF vectors
- `predict_category(model, text)`: Predicts category for a given input
- `load_model()`: Loads the trained `.pkl` model

### `utils.py`
- `mask_pii(email_body)`: Identifies and masks sensitive info (names, dates, orgs)
- `restore_pii(masked_email, entities)`: Replaces masked tokens with original PII

### `logger.py`
- Unified logging setup — logs to terminal (and file if `ENV=local`)

### `train.py`
- CLI script to train the classifier and save `email_classifier.pkl`

---

## Local Development

```bash
# Start FastAPI server
uvicorn app:app --reload

# Send test request via curl
curl -X POST http://127.0.0.1:8000/classify/ \
  -H "Content-Type: application/json" \
  -d '{"email_body": "Please help reset my VPN login."}'
```

---

## Deployment-Ready
- Tested on Hugging Face Spaces (Docker-based)
- Compatible with automated API tests (assignment-ready)
- Lightweight and modular design

---

## Author
Sumit Singh — B.Tech CSE, AI/ML Enthusiast & FastAPI Builder

---

