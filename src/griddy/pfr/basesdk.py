from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Type

from griddy.core.basesdk import BaseSDK as CoreBaseSDK

from . import errors, models
from .utils.browserless import Browserless


@dataclass
class EndpointConfig:
    """Configuration for a PFR HTML-scraping endpoint."""

    path_template: str
    operation_id: str
    wait_for_element: str
    parser: Callable[[str], Any]
    response_type: Type
    path_params: Dict[str, Any] = field(default_factory=dict)
    timeout_ms: Optional[int] = None


class BaseSDK(CoreBaseSDK):
    """PFR-specific BaseSDK with PFR error classes and security model."""

    def __init__(self, sdk_config: Any, parent_ref: Optional[object] = None):
        super().__init__(sdk_config=sdk_config, parent_ref=parent_ref)
        self.browserless = Browserless()

    @property
    def _default_error_cls(self) -> Type[Exception]:
        return errors.GriddyPFRDefaultError

    @property
    def _no_response_error_cls(self) -> Type[Exception]:
        return errors.NoResponseError

    @property
    def _security_model_cls(self) -> Any:
        return models.Security

    @property
    def _security_env_mapping(self) -> Optional[Dict[str, str]]:
        return {"pfr_auth": "GRIDDY_PFR_AUTH"}

    def _execute_endpoint(self, config: EndpointConfig) -> Any:
        """Execute a PFR scraping endpoint using its configuration.

        Resolves the base URL, templates path params, fetches HTML via
        Browserless, and runs the configured parser.
        """
        base_url, _ = self.sdk_configuration.get_server_details()
        path = config.path_template.format(**config.path_params)
        url = f"{base_url}{path}"

        html = self.browserless.get_page_content(
            url,
            wait_for_element=config.wait_for_element,
        )

        return config.parser(html)
