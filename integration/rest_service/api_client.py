from typing import Dict, TypedDict, Optional


class CodeRequestResponse(TypedDict):
    obfuscated_device_identifier: Optional[str]
    error: Optional[str]


class BaseAPIClient:
    def get_membership_identifier(self, data: Dict) -> Dict:
        raise NotImplementedError

    def is_active(self, membership_identifier: str) -> bool:
        raise NotImplementedError

    def external_service_is_healthy(self) -> bool:
        raise NotImplementedError

    def request_verification_code(self, user_data: Dict) -> CodeRequestResponse:
        raise NotImplementedError
