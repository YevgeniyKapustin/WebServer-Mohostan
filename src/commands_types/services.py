from src.database import session
from src.commands_types.models import Type


async def get_type_by_name(name: str) -> Type:
    return (
        session.query(Type).
        where(Type.name == name).
        first()
    )


async def add_type_by_name(name: str) -> bool:
    session.add(Type(name=name))
    session.commit()
    return True


async def edit_type_name(original_type: Type, new_name: str) -> bool:
    original_type.name = new_name
    session.commit()
    return True
