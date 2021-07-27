from typing import List, Dict, Optional

from integration.rest_service.api_client import (
    BaseAPIClient,
    CodeRequestResponse,
    PrivateIdentifier,
    PrivateIdentifierList,
)


class MembershipService:
    def __init__(self, api_client: BaseAPIClient):
        self.api_client = api_client

    def get_membership_identifier(self, data: Dict) -> Optional[Dict]:
        return self.api_client.get_membership_identifier(data)

    def is_active(self, membership_identifier: str) -> bool:
        return self.api_client.is_active(membership_identifier)

    def external_service_is_healthy(self) -> bool:
        return self.api_client.external_service_is_healthy()

    def request_verification_code(self, user_data: Dict) -> CodeRequestResponse:
        return self.api_client.request_verification_code(user_data)

    def get_private_identifier_value_list(
        self, uuids: List[str]
    ) -> PrivateIdentifierList:
        return self.api_client.get_private_identifier_value_list(uuids)

    def create_private_identifier(self, value: str) -> PrivateIdentifier:
        return self.api_client.create_private_identifier(value)

    def get_private_identifier_value(self, uuid: str) -> Optional[PrivateIdentifier]:
        return self.api_client.get_private_identifier_value(uuid)

    def delete_private_identifier(self, uuid: str) -> bool:
        return self.api_client.delete_private_identifier(uuid)
