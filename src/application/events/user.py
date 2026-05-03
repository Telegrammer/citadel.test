from dataclasses import dataclass


@dataclass(frozen=True)
class UserActivationKeyGenerated:
    user_email: str
    activation_key: str
