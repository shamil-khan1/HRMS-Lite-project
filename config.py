import os
class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("postgresql://hrms_db_ibmt_user:OkUtBcxDTnaupZ8s2aapUtepywy28sXv@dpg-d661otfgi27c73djomcg-a/hrms_db_ibmt")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


