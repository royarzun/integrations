from typing import Dict, Optional

from integration.rest_service.api_client import BaseAPIClient


class MembershipService:
    def __init__(self, api_client: BaseAPIClient):
        self.api_client = api_client

    def get_membership_identifier(self, data: Dict) -> Optional[Dict]:
        return self.api_client.get_membership_identifier(data)

    def is_active(self, membership_identifier: str) -> bool:
        return self.api_client.is_active(membership_identifier)

    def external_service_is_healthy(self) -> bool:
        return self.api_client.external_service_is_healthy()
