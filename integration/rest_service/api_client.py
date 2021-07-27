from typing import Dict, List, Optional, TypedDict


class CodeRequestResponse(TypedDict):
    obfuscated_device_identifier: Optional[str]
    error: Optional[str]


class PrivateIdentifier(TypedDict):
    identifier: str
    value: str


class PrivateIdentifierList(TypedDict):
    data: List[PrivateIdentifier]


class BaseAPIClient:
    def get_membership_identifier(self, data: Dict) -> Dict:
        raise NotImplementedError

    def is_active(self, membership_identifier: str) -> bool:
        raise NotImplementedError

    def external_service_is_healthy(self) -> bool:
        raise NotImplementedError

    def request_verification_code(self, user_data: Dict) -> CodeRequestResponse:
        raise NotImplementedError

    def search_private_identifiers_values(
        self, uuids: List[str]
    ) -> PrivateIdentifierList:
        return NotImplementedError

    def create_private_identifier(self, value: str) -> PrivateIdentifier:
        raise NotImplementedError

    def get_private_identifier_value(self, uuid: str) -> Optional[PrivateIdentifier]:
        raise NotImplementedError

    def delete_private_identifier(self, uuid: str) -> bool:
        raise NotImplementedError
