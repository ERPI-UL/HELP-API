
from app.models.statement import ObjectOut, Statement


def find_object(statement_db: Statement):
    """ find the object of a statement"""
    if statement_db.object_activity_id is not None:
        return ObjectOut(id=statement_db.object_activity_id, objectType="activity")
    elif statement_db.object_action_id is not None:
        return ObjectOut(id=statement_db.object_action_id, objectType="action")
    elif statement_db.object_agent_id is not None:
        return ObjectOut(id=statement_db.object_agent_id, objectType="agent")
    elif statement_db.object_target_id is not None:
        return ObjectOut(id=statement_db.object_target_id, objectType="target")
    else:
        return None
