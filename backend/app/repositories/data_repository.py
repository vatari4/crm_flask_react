from app.models.analytics import (
    UserAnalytics,
    ContractAnalytics,
    DealAnalytics,
    TopEmployee,
    PerformanceAnalytics,
    AnalyticsMetadata,
)
from app.db.database import db

class DataRepository:
    @staticmethod
    def get_analytics():
        user_analytics = UserAnalytics.query.first()
        contract_analytics = ContractAnalytics.query.first()
        deal_analytics = DealAnalytics.query.first()
        top_employee = TopEmployee.query.first()
        performance = PerformanceAnalytics.query.first()
        metadata = AnalyticsMetadata.query.first()

        return {
            "analytics": {
                "users": {
                    "total_visitors": user_analytics.total_visitors,
                    "new_visitors": user_analytics.new_visitors,
                    "returning_visitors": user_analytics.returning_visitors,
                },
                "contracts": {
                    "in_progress": contract_analytics.in_progress,
                    "signed": contract_analytics.signed,
                    "total": contract_analytics.total,
                    "rejected": contract_analytics.rejected,
                },
                "deals": {
                    "completed": deal_analytics.completed,
                    "in_progress": deal_analytics.in_progress,
                    "total": deal_analytics.total,
                    "avg_deal_size": deal_analytics.avg_deal_size,
                },
                "performance": {
                    "top_employee": {
                        "id": top_employee.id,
                        "name": top_employee.name,
                        "department": top_employee.department,
                        "kpi": top_employee.kpi,
                        "deals_closed": top_employee.deals_closed,
                        "revenue_generated": top_employee.revenue_generated,
                    },
                    "team_average": performance.team_average,
                }
            },
            "metadata": {
                "period": metadata.period,
                "generated_at": metadata.generated_at,
                "source": metadata.source,
            }
        }
