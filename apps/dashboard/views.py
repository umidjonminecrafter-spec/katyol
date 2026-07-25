from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.dependencies import get_current_user
from apps.accounts.models import User
from apps.dashboard.services import DashboardService
from apps.dashboard.schemas import DashboardSummaryResponse, DashboardChartsResponse, DashboardSummaryData, DashboardChartsData

async def get_summary_view(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    summary_data = await DashboardService.get_summary(db)
    return DashboardSummaryResponse(
        success=True,
        data=DashboardSummaryData(**summary_data)
    )

async def get_charts_view(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    charts_data = await DashboardService.get_charts(db)
    return DashboardChartsResponse(
        success=True,
        data=DashboardChartsData(trends=charts_data)
    )
