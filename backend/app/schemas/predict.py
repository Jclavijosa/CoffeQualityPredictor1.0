from pydantic import BaseModel, Field

class PredictionInput(BaseModel):
    aroma: float = Field(..., gt=0, lt=10)
    flavor: float = Field(..., gt=0, lt=10)
    aftertaste: float = Field(..., gt=0, lt=10)
    acidity: float = Field(..., gt=0, lt=10)
    body: float = Field(..., gt=0, lt=10)
    balance: float = Field(..., gt=0, lt=10)
    uniformity: float = Field(..., gt=0, lt=10)

class PredictionOutput(BaseModel):
    calidad: str
