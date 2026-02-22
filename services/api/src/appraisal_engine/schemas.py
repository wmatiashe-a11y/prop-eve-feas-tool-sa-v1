from pydantic import BaseModel, Field
from typing import Literal

class RevenueInputs(BaseModel):
    sellable_area_m2: float = Field(gt=0)
    exit_price_per_m2: float = Field(gt=0)

class CostInputs(BaseModel):
    build_cost_per_m2: float = Field(gt=0)
    contingency_rate: float = Field(ge=0, le=0.5, default=0.1)
    professional_fees_rate: float = Field(ge=0, le=0.5, default=0.1)
    marketing_rate_on_gdv: float = Field(ge=0, le=0.2, default=0.03)

class ProfitTarget(BaseModel):
    basis: Literal["gdv", "cost"] = "gdv"
    target_rate: float = Field(ge=0, le=0.5, default=0.2)

class Assumptions(BaseModel):
    revenue: RevenueInputs
    costs: CostInputs
    profit_target: ProfitTarget

class AuditLine(BaseModel):
    section: str
    key: str
    label: str
    value: float
    formula: str

class Outputs(BaseModel):
    gdv: float
    tdc: float
    profit: float
    profit_margin: float
    residual_land_value: float
    audit: list[AuditLine]
