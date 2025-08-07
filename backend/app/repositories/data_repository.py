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
    def get_analytics_for_user(self, user_id):
        # Здесь по user_id делаем фильтрацию в моделях
        user_analytics = UserAnalytics.query.filter_by(user_id=user_id).first()
        contract_analytics = ContractAnalytics.query.filter_by(user_id=user_id).first()
        deal_analytics = DealAnalytics.query.filter_by(user_id=user_id).first()
        top_employee = TopEmployee.query.filter_by(user_id=user_id).first()
        performance = PerformanceAnalytics.query.join(TopEmployee).filter(TopEmployee.user_id == user_id).first()
        metadata = AnalyticsMetadata.query.first()  # если нужно, можно сделать и по user_id

        return {
            "analytics": {
                "users": {
                    "total_visitors": getattr(user_analytics, "total_visitors", 0),
                    "new_visitors": getattr(user_analytics, "new_visitors", 0),
                    "returning_visitors": getattr(user_analytics, "returning_visitors", 0),
                },
                "contracts": {
                    "in_progress": getattr(contract_analytics, "in_progress", 0),
                    "signed": getattr(contract_analytics, "signed", 0),
                    "total": getattr(contract_analytics, "total", 0),
                    "rejected": getattr(contract_analytics, "rejected", 0),
                },
                "deals": {
                    "completed": getattr(deal_analytics, "completed", 0),
                    "in_progress": getattr(deal_analytics, "in_progress", 0),
                    "total": getattr(deal_analytics, "total", 0),
                    "avg_deal_size": getattr(deal_analytics, "avg_deal_size", 0),
                },
                "performance": {
                    "top_employee": {
                        "id": getattr(top_employee, "id", None),
                        "name": getattr(top_employee, "name", None),
                        "department": getattr(top_employee, "department", None),
                        "kpi": getattr(top_employee, "kpi", 0.0),
                        "deals_closed": getattr(top_employee, "deals_closed", 0),
                        "revenue_generated": getattr(top_employee, "revenue_generated", 0),
                    } if top_employee else None,
                    "team_average": getattr(performance, "team_average", 0.0) if performance else 0.0,
                }
            },
            "metadata": {
                "period": getattr(metadata, "period", ""),
                "generated_at": getattr(metadata, "generated_at", ""),
                "source": getattr(metadata, "source", ""),
            }
        }
