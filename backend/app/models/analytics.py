from app.db.database import db

class UserAnalytics(db.Model):
    __tablename__ = "user_analytics"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    total_visitors = db.Column(db.Integer)
    new_visitors = db.Column(db.Integer)
    returning_visitors = db.Column(db.Integer)

    user = db.relationship("User", backref=db.backref("user_analytics", uselist=False))



class ContractAnalytics(db.Model):
    __tablename__ = "contract_analytics"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    in_progress = db.Column(db.Integer)
    signed = db.Column(db.Integer)
    total = db.Column(db.Integer)
    rejected = db.Column(db.Integer)

    user = db.relationship("User", backref=db.backref("contract_analytics", uselist=False))



class DealAnalytics(db.Model):
    __tablename__ = "deal_analytics"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    deals_count = db.Column(db.Integer)
    revenue = db.Column(db.Float)

    user = db.relationship("User", backref="deal_analytics")

class TopEmployee(db.Model):
    __tablename__ = "top_employee"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  
    name = db.Column(db.String(100))
    department = db.Column(db.String(50))
    kpi = db.Column(db.Float)
    deals_closed = db.Column(db.Integer)
    revenue_generated = db.Column(db.Integer)

    user = db.relationship("User", backref="top_employees") 



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
