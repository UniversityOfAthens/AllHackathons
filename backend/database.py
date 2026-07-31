from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, Boolean, DateTime, Enum, text, CheckConstraint
from sqlalchemy.sql import func
from datetime import datetime,timedelta
import enum
#from main import MAX_INTERESTCOUNT_VALUE

MAX_INTERESTCOUNT_VALUE = 10000

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
today = datetime.now().replace(microsecond=0)
tommorow = today + timedelta(days=1)

class StatusEnum(enum.Enum): # Python feature for creating a fixed set of named constants.
    draft = "draft" #name is draft and value is 'draft', they are seperate things but in our case they have the same name
    pending = "pending"
    published = "published"
    needs_changes = "needs-changes"
    
class ModeEnum(enum.Enum):
    in_person = "in_person"
    online = "online"
    hybrid = "hybrid"

class Hackathon(db.Model): #db has the model class=Base, we can add another base later for our next table
    __tablename__ = "hackathon"
    id: Mapped[str] = mapped_column(Integer,primary_key=True,autoincrement=True) #autoincrement increases id number by 1 each time a new hackathon gets added
    name: Mapped[str] = mapped_column(String,nullable=False) #name REQUIRED
    description: Mapped[str] = mapped_column(String,nullable=True)
    url: Mapped[str] = mapped_column(String,nullable=False) #official link REQUIRED
    startDate: Mapped[datetime] = mapped_column(DateTime, nullable=True) # ISO 8601 date (des to meta)
    endDate: Mapped[datetime] = mapped_column(DateTime,nullable=True) # ISO 8601 date (des to meta)
    location: Mapped[str] = mapped_column(String,nullable=True)
    mode: Mapped[ModeEnum] = mapped_column(Enum(ModeEnum),nullable=True) # sqlalchemy's Enum(ModeEnum) restricts this column to only those values: in-person,online,hybrid
    organizer: Mapped[str] = mapped_column(String,nullable=True)
    hasPrize: Mapped[bool] = mapped_column(Boolean,nullable=True)
    prizeDetails: Mapped[str] = mapped_column(String,nullable=True)
    tags: Mapped[str] = mapped_column(String,nullable=True)
    status: Mapped[StatusEnum] = mapped_column(Enum(StatusEnum),nullable=True) # sqlalchemy's Enum(StatusEnum) restricts this column to only those values: draft,pending,published,needs-change 
    submittedAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(),nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(),nullable=False)
    interestCount: Mapped[int] = mapped_column(Integer,nullable=True)
    __table_args__ = (CheckConstraint(f'interestCount >= 0 AND interestCount <= {MAX_INTERESTCOUNT_VALUE}', name='check_interest_count_range'),)
    
    
    def to_dict(self):
        return{
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "url": self.url,
            "startDate": self.startDate.isoformat() if self.startDate else None,
            "endDate": self.endDate.isoformat() if self.endDate else None,
            "location": self.location,
            "mode": self.mode.value if self.mode in (ModeEnum.in_person, ModeEnum.online, ModeEnum.hybrid) else None,
            "organizer": self.organizer,
            "hasPrize": self.hasPrize,
            "prizeDetails": self.prizeDetails,
            "tags": self.tags,
            "status": self.status.value if self.status in (StatusEnum.draft, StatusEnum.pending, StatusEnum.published, StatusEnum.needs_changes) else None,
            "submittedAt": self.submittedAt.isoformat() if self.submittedAt else None,
            "updatedAt": self.updatedAt.isoformat() if self.updatedAt else None,
            "interestCount": self.interestCount,
        }