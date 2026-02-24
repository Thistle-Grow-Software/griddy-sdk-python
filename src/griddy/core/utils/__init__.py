import builtins
import sys
from importlib import import_module
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .annotations import get_discriminator
    from .converters import clean_text, safe_float, safe_int, safe_numberify
    from .cookies import (
        Cookie,
        cookies_to_dict,
        cookies_to_header,
        extract_cookies_as_dict,
        extract_cookies_as_header,
        extract_cookies_for_url,
        parse_cookies_txt,
    )
    from .datetimes import parse_date, parse_datetime
    from .enums import OpenEnumMeta
    from .har import (
        HarEntryPathManager,
        consolidate_minified_entries,
        extract_minified_har_entry,
        html_template,
        minify_har,
        write_consolidated_to_files,
    )
    from .headers import get_headers, get_response_headers
    from .logger import Logger, get_body_content, get_default_logger
    from .metadata import (
        FieldMetadata,
        FormMetadata,
        HeaderMetadata,
        MultipartFormMetadata,
        PathParamMetadata,
        QueryParamMetadata,
        RequestMetadata,
        SecurityMetadata,
        find_metadata,
    )
    from .queryparams import get_query_params
    from .requestbodies import SerializedRequestBody, serialize_request_body
    from .retries import (
        BackoffStrategy,
        Retries,
        RetryConfig,
        retry,
        retry_async,
        retry_on_rate_limit,
    )
    from .security import get_security, get_security_from_env
    from .serializers import (
        get_pydantic_model,
        marshal_json,
        serialize_decimal,
        serialize_float,
        serialize_int,
        stream_to_bytes,
        stream_to_bytes_async,
        stream_to_text,
        stream_to_text_async,
        unmarshal,
        unmarshal_json,
        validate_const,
        validate_decimal,
        validate_float,
        validate_int,
        validate_open_enum,
    )
    from .url import build_url, generate_url, remove_suffix, template_url
    from .values import (
        cast_partial,
        get_global_from_env,
        match_content_type,
        match_response,
        match_status_codes,
    )
    from .yaml_consolidator import YAMLConsolidator

__all__ = [
    "BackoffStrategy",
    "build_url",
    "cast_partial",
    "clean_text",
    "consolidate_minified_entries",
    "Cookie",
    "cookies_to_dict",
    "cookies_to_header",
    "extract_cookies_as_dict",
    "extract_cookies_as_header",
    "extract_cookies_for_url",
    "extract_minified_har_entry",
    "FieldMetadata",
    "find_metadata",
    "FormMetadata",
    "generate_url",
    "get_body_content",
    "get_default_logger",
    "get_discriminator",
    "get_global_from_env",
    "get_headers",
    "get_pydantic_model",
    "get_query_params",
    "get_response_headers",
    "get_security",
    "get_security_from_env",
    "HarEntryPathManager",
    "HeaderMetadata",
    "html_template",
    "Logger",
    "marshal_json",
    "match_content_type",
    "match_response",
    "match_status_codes",
    "minify_har",
    "MultipartFormMetadata",
    "OpenEnumMeta",
    "parse_cookies_txt",
    "parse_date",
    "parse_datetime",
    "PathParamMetadata",
    "QueryParamMetadata",
    "remove_suffix",
    "RequestMetadata",
    "Retries",
    "retry",
    "retry_async",
    "retry_on_rate_limit",
    "RetryConfig",
    "safe_float",
    "safe_int",
    "safe_numberify",
    "SecurityMetadata",
    "serialize_decimal",
    "serialize_float",
    "serialize_int",
    "serialize_request_body",
    "SerializedRequestBody",
    "stream_to_bytes",
    "stream_to_bytes_async",
    "stream_to_text",
    "stream_to_text_async",
    "template_url",
    "unmarshal",
    "unmarshal_json",
    "validate_const",
    "validate_decimal",
    "validate_float",
    "validate_int",
    "validate_open_enum",
    "write_consolidated_to_files",
    "YAMLConsolidator",
]

_dynamic_imports: dict[str, str] = {
    "BackoffStrategy": ".retries",
    "build_url": ".url",
    "cast_partial": ".values",
    "clean_text": ".converters",
    "consolidate_minified_entries": ".har",
    "Cookie": ".cookies",
    "cookies_to_dict": ".cookies",
    "cookies_to_header": ".cookies",
    "extract_cookies_as_dict": ".cookies",
    "extract_cookies_as_header": ".cookies",
    "extract_cookies_for_url": ".cookies",
    "extract_minified_har_entry": ".har",
    "FieldMetadata": ".metadata",
    "find_metadata": ".metadata",
    "FormMetadata": ".metadata",
    "generate_url": ".url",
    "get_body_content": ".logger",
    "get_default_logger": ".logger",
    "get_discriminator": ".annotations",
    "get_global_from_env": ".values",
    "get_headers": ".headers",
    "get_pydantic_model": ".serializers",
    "get_query_params": ".queryparams",
    "get_response_headers": ".headers",
    "get_security": ".security",
    "get_security_from_env": ".security",
    "HarEntryPathManager": ".har",
    "HeaderMetadata": ".metadata",
    "html_template": ".har",
    "Logger": ".logger",
    "marshal_json": ".serializers",
    "match_content_type": ".values",
    "match_response": ".values",
    "match_status_codes": ".values",
    "minify_har": ".har",
    "MultipartFormMetadata": ".metadata",
    "OpenEnumMeta": ".enums",
    "parse_cookies_txt": ".cookies",
    "parse_date": ".datetimes",
    "parse_datetime": ".datetimes",
    "PathParamMetadata": ".metadata",
    "QueryParamMetadata": ".metadata",
    "remove_suffix": ".url",
    "RequestMetadata": ".metadata",
    "Retries": ".retries",
    "retry": ".retries",
    "retry_async": ".retries",
    "retry_on_rate_limit": ".retries",
    "RetryConfig": ".retries",
    "safe_float": ".converters",
    "safe_int": ".converters",
    "safe_numberify": ".converters",
    "SecurityMetadata": ".metadata",
    "serialize_decimal": ".serializers",
    "serialize_float": ".serializers",
    "serialize_int": ".serializers",
    "serialize_request_body": ".requestbodies",
    "SerializedRequestBody": ".requestbodies",
    "stream_to_bytes": ".serializers",
    "stream_to_bytes_async": ".serializers",
    "stream_to_text": ".serializers",
    "stream_to_text_async": ".serializers",
    "template_url": ".url",
    "unmarshal": ".serializers",
    "unmarshal_json": ".serializers",
    "validate_const": ".serializers",
    "validate_decimal": ".serializers",
    "validate_float": ".serializers",
    "validate_int": ".serializers",
    "validate_open_enum": ".serializers",
    "write_consolidated_to_files": ".har",
    "YAMLConsolidator": ".yaml_consolidator",
}


def dynamic_import(modname, retries=3):
    for attempt in range(retries):
        try:
            return import_module(modname, __package__)
        except KeyError:
            # Clear any half-initialized module and retry
            sys.modules.pop(modname, None)
            if attempt == retries - 1:
                break
    raise KeyError(f"Failed to import module '{modname}' after {retries} attempts")


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    if module_name is None:
        raise AttributeError(
            f"no {attr_name} found in _dynamic_imports, module name -> {__name__} "
        )

    try:
        module = dynamic_import(module_name)
        return getattr(module, attr_name)
    except ImportError as e:
        raise ImportError(
            f"Failed to import {attr_name} from {module_name}: {e}"
        ) from e
    except AttributeError as e:
        raise AttributeError(
            f"Failed to get {attr_name} from {module_name}: {e}"
        ) from e


def __dir__():
    lazy_attrs = builtins.list(_dynamic_imports.keys())
    return builtins.sorted(lazy_attrs)
