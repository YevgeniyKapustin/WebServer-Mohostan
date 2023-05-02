from src.database import session
from src.commands_types.models import Type


async def get_type_by_name(name: str) -> Type:
    return (
        session.query(Type).where(
            Type.name == name
        ).first()
    )


async def create_type_by_name(name: str) -> bool:
    session.add(Type(name=name))
    session.commit()
    return True
