from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from api.persistence.core import Base


class LassoModelPredictions(Base):
    __tablename__ = "regression_model_predictions"
    id = Column(Integer, primary_key=True)
    user_id = Column(String(36), nullable=False)
    datetime_captured = Column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )
    model_version = Column(String(36), nullable=False)
    inputs = Column(JSONB)
    outputs = Column(JSONB)


class GradientBoostingModelPredictions(Base):
    __tablename__ = "gradient_boosting_model_predictions"
    id = Column(Integer, primary_key=True)
    user_id = Column(String(36), nullable=False)
    datetime_captured = Column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )
    model_version = Column(String(36), nullable=False)
    inputs = Column(JSONB)
    outputs = Column(JSONB)
