from sqlalchemy.ext.asyncio import AsyncSession
from apps.finance.services import FinanceService

class DashboardService:
    @staticmethod
    async def get_summary(db: AsyncSession):
        return await FinanceService.get_dashboard_summary(db)

    @staticmethod
    async def get_charts(db: AsyncSession):
        return await FinanceService.get_dashboard_charts(db)
