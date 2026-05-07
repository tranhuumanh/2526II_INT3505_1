from fastapi import FastAPI, APIRouter, Header, Query, Response, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List, Union

app = FastAPI(
    title="API Versioning Demo - Buổi 9",
    description="Demo 3 chiến lược versioning phổ biến và quản lý vòng đời API",
    version="2.0.0"
)

# Giả lập database cho Idempotency
processed_keys = set()

# --- UTILS: Response Wrappers ---
def v2_wrapper(data: any, meta: dict = None):
    return {
        "data": data,
        "meta": meta or {"status": "success", "api_version": "v2"}
    }

# ==========================================
# STRATEGY 1: URL PATH (v1 vs v2)
# ==========================================
router_v1 = APIRouter(prefix="/api/v1", tags=["Strategy 1: URL Path (Legacy)"])
router_v2 = APIRouter(prefix="/api/v2", tags=["Strategy 1: URL Path (Current)"])

class PaymentV1(BaseModel):
    amount: str
    card_number: str
    description: str

class PaymentV2(BaseModel):
    amount: float
    currency: str
    card_last4: str
    description: str
    idempotency_key: str

@router_v1.post("/payments")
async def create_payment_v1(payment: PaymentV1, response: Response):
    # Thêm Deprecation Headers
    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = "2026-09-01"
    # Lỗi bảo mật: trả về nguyên card_number
    return {
        "message": "Payment created (v1)",
        "card_number": payment.card_number, 
        "warning": "SECURITY RISK: Full card number exposed!"
    }

@router_v2.post("/payments")
async def create_payment_v2(payment: PaymentV2):
    # Kiểm tra Idempotency
    if payment.idempotency_key in processed_keys:
        return {"duplicate": True, "message": "Request already processed", "key": payment.idempotency_key}
    
    processed_keys.add(payment.idempotency_key)
    
    # Masking card number
    masked_card = f"****-****-****-{payment.card_last4}"
    
    data = {
        "payment_id": "pay_999",
        "amount": payment.amount,
        "currency": payment.currency,
        "card": masked_card,
        "description": payment.description
    }
    return v2_wrapper(data)

# ==========================================
# STRATEGY 2: HEADER VERSIONING
# ==========================================
@app.get("/api/products", tags=["Strategy 2: Header"])
async def get_products(x_api_version: Optional[str] = Header(None)):
    products = [{"id": 1, "name": "Laptop"}, {"id": 2, "name": "Phone"}]
    
    if x_api_version == "2":
        return v2_wrapper(products, {"total": len(products), "version": "Header-based v2"})
    
    # Mặc định trả về v1 (mảng phẳng)
    return products

# ==========================================
# STRATEGY 3: QUERY PARAMETER
# ==========================================
@app.get("/api/orders", tags=["Strategy 3: Query Param"])
async def get_orders(version: str = Query("1")):
    order_data = {"id": 101, "total": 150000}
    
    if version == "2":
        order_data["total_formatted"] = f"{order_data['total']:,} VND"
        return v2_wrapper(order_data)
    
    return order_data

# ==========================================
# LIFECYCLE: MIGRATION GUIDE
# ==========================================
@app.get("/api/migration-guide", tags=["Lifecycle"])
async def get_migration_guide():
    return {
        "current_stable": "v2",
        "deprecation_notice": "v1 will be disabled on 2026-09-01",
        "breaking_changes": [
            "URL prefix changed from /v1 to /v2",
            "Card number replaced by card_last4 (Security)",
            "Amount changed from String to Float",
            "Response structure wrapped in {data, meta}"
        ],
        "timeline": {
            "Q1-2026": "Release v2 (Beta)",
            "Q2-2026": "Deprecation warning on v1",
            "Q3-2026": "Sunset v1"
        }
    }

app.include_router(router_v1)
app.include_router(router_v2)