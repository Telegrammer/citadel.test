from domain.entities.user import UserId


def connection_status_channel(user_id: UserId) -> str:
    return f"connection-status:{user_id.value}"
