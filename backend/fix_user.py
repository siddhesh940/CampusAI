import os  
  
content = r'''""" >> fix_user.py && echo User model with role-based access control. >> fix_user.py && echo Users are always scoped to a university ^(multi-tenant^). >> fix_user.py && echo """ 
 
import enum 
import uuid 
from datetime import datetime 
 
from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, func 
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm import Mapped, mapped_column, relationship 
 
from app.database import Base
