from datetime import datetime

from config.extensions import db

from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Text


class LoginLog(db.Model):

    __tablename__ = "login_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("usuario.id"))
    login_at = Column(DateTime, default=datetime.utcnow)

    username = Column(String(45))
    ip_address = Column(String(45))
    user_agent = Column(Text)

    browser = Column(String(100))
    operating_system = Column(String(100))
    device = Column(String(100))

    success = Column(Boolean, default=True)
