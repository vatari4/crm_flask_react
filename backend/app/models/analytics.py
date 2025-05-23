from app.db.database import db

class UserAnalytics(db.Model):
    __tablename__ = "user_analytics"

    id = db.Column(db.Integer, primary_key=True)
    total_visitors = db.Column(db.Integer)
    new_visitors = db.Column(db.Integer)
    returning_visitors = db.Column(db.Integer)


class ContractAnalytics(db.Model):
    __tablename__ = "contract_analytics"

    id = db.Column(db.Integer, primary_key=True)
    in_progress = db.Column(db.Integer)
    signed = db.Column(db.Integer)
    total = db.Column(db.Integer)
    rejected = db.Column(db.Integer)


class DealAnalytics(db.Model):
    __tablename__ = "deal_analytics"

    id = db.Column(db.Integer, primary_key=True)
    completed = db.Column(db.Integer)
    in_progress = db.Column(db.Integer)
    total = db.Column(db.Integer)
    avg_deal_size = db.Column(db.Integer)


class TopEmployee(db.Model):
    __tablename__ = "top_employee"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    department = db.Column(db.String(50))
    kpi = db.Column(db.Float)
    deals_closed = db.Column(db.Integer)
    revenue_generated = db.Column(db.Integer)


class PerformanceAnalytics(db.Model):
    __tablename__ = "performance_analytics"

    id = db.Column(db.Integer, primary_key=True)
    top_employee_id = db.Column(db.Integer, db.ForeignKey("top_employee.id"))
    team_average = db.Column(db.Float)

    top_employee = db.relationship("TopEmployee", backref="performance")


class AnalyticsMetadata(db.Model):
    __tablename__ = "analytics_metadata"

    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String(50))
    generated_at = db.Column(db.String(50))
    source = db.Column(db.String(100))
