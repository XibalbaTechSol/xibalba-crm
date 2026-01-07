from sqlalchemy import Column, String, ForeignKey, Table, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.user import User
from app.models.acl_entities import entity_team, Team

class Meeting(Base):
    __tablename__ = "meeting"

    id = Column(String(24), primary_key=True, index=True)
    name = Column(String(255))
    status = Column(String(100))
    date_start = Column("dateStart", DateTime)
    date_end = Column("dateEnd", DateTime)
    description = Column(String)

    deleted = Column(Boolean, default=False)

    assigned_user_id = Column("assignedUserId", String(24), ForeignKey("user.id"))
    assigned_user = relationship("User")

    teams = relationship("Team", secondary=entity_team,
                         primaryjoin="and_(Meeting.id==entity_team.c.entity_id, entity_team.c.entity_type=='Meeting')",
                         secondaryjoin="Team.id==entity_team.c.team_id",
                         viewonly=True)

class Stream(Base):
    __tablename__ = "stream"

    id = Column(String(24), primary_key=True, index=True)
    post = Column(String)
    created_by_name = Column("createdByName", String(255))
    created_at = Column("createdAt", DateTime)

    deleted = Column(Boolean, default=False)
