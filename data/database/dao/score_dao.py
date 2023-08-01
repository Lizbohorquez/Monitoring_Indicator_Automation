from ..declarative_base import Base, Session, engine
from ..entities.score import Score

session = Session()


def add_score(infra, proactive, realtime, total):
    """
    Adds a new score entry to the "Score" table in the database.
    Param infra: The infrastructure monitoring score (0-100).
    Param proactive: The proactive monitoring score (0-100).
    Param realtime: The real-time monitoring score (0-100).
    Param total: The total score (optional).
    Return: The result of the database operation (usually None if successful).
    """
    session.add(Score(infrastructure=infra, proactive=proactive, realtime=realtime, total=total))
    res = session.commit()
    return res
