from typing import List, Optional
from pydantic import BaseModel

class DashboardSummaryData(BaseModel):
    monthly_revenue: float
    revenue_growth_percent: float
    active_orders_count: int
    completed_boilers_count: int
    low_stock_alerts_count: int

class DashboardSummaryResponse(BaseModel):
    success: bool = True
    data: DashboardSummaryData

class ChartDataPoint(BaseModel):
    label: str
    sales: float
    production: int

class DashboardChartsData(BaseModel):
    trends: List[ChartDataPoint]

class DashboardChartsResponse(BaseModel):
    success: bool = True
    data: DashboardChartsData
