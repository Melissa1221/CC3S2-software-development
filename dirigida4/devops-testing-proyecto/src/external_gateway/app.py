"""Microservicio HTTP local para simular pasarela de pagos."""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from decimal import Decimal
from typing import Optional
import random

app = FastAPI(title="Payment Gateway API")

class ChargeRequest(BaseModel):
    """Modelo de entrada para un cargo."""
    amount: Decimal
    currency: str
    user_id: str
    success_rate: Optional[float] = 1.0  # Tasa de éxito simulada (0.0-1.0)

class ChargeResponse(BaseModel):
    """Respuesta de la pasarela de pago."""
    success: bool
    transaction_id: Optional[str] = None
    error_message: Optional[str] = None

@app.post("/charge", response_model=ChargeResponse)
async def charge(request: ChargeRequest):
    """
    Simula un cargo en una pasarela de pagos externa.
    Usa success_rate para simular fallos aleatorios.
    """
    # Validaciones
    if request.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El monto debe ser positivo"
        )
    
    if request.currency not in ["USD", "EUR", "GBP"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Moneda no soportada: {request.currency}"
        )
    
    # Simular probabilidad de éxito
    if random.random() <= request.success_rate:
        # Cargo exitoso
        return ChargeResponse(
            success=True,
            transaction_id=f"txn_{random.randint(10000, 99999)}"
        )
    else:
        # Fallo del cargo
        return ChargeResponse(
            success=False,
            error_message="Fallo simulado en la pasarela de pagos"
        ) 