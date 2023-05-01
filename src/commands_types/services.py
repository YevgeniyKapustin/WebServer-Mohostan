from src.database import session
from src.commands_types.models import Type as TypeModel


async def get_type_by_name(name: str):
    return (
        session.query(TypeModel).where(
            TypeModel.name == name
        ).first()
    )


async def create_type_by_name(name: str):
    session.add(TypeModel(name=name))
    session.commit()
    return True
