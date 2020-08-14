from typing import Dict


class BaseAPIClient:
    def get_membership_identifier(self, data: Dict) -> Dict:
        raise NotImplementedError

    def is_active(self, membership_identifier: str) -> bool:
        raise NotImplementedError

    def external_service_is_healthy(self) -> bool:
        raise NotImplementedError
