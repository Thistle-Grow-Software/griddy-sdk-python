"""Schools endpoint for Pro Football Reference.

Provides ``list()`` and ``high_schools()`` to fetch and parse PFR school pages.
"""

from typing import Optional

from griddy.pfr.parsers.schools import SchoolsParser

from ..basesdk import BaseSDK, EndpointConfig
from ..models import CollegeList, HighSchoolList

_parser = SchoolsParser()


class Schools(BaseSDK):
    """Sub-SDK for PFR Schools & Colleges pages."""

    def _get_list_config(
        self,
        *,
        timeout_ms: Optional[int] = None,
    ) -> EndpointConfig:
        return EndpointConfig(
            path_template="/schools/",
            operation_id="getCollegeList",
            wait_for_element="#college_stats_table",
            parser=lambda html: _parser.parse_colleges(html),
            response_type=CollegeList,
            path_params={},
            timeout_ms=timeout_ms,
        )

    def list(
        self,
        *,
        timeout_ms: Optional[int] = None,
    ) -> CollegeList:
        """Fetch and parse the All Player Colleges page from Pro Football Reference.

        Scrapes
        ``https://www.pro-football-reference.com/schools/``
        and returns structured data for every college/university.

        Args:
            timeout_ms: Optional timeout in milliseconds for the page
                selector.

        Returns:
            A :class:`~griddy.pfr.models.CollegeList` instance containing
            all college entries.
        """
        config = self._get_list_config(timeout_ms=timeout_ms)
        data = self._execute_endpoint(config)
        return CollegeList.model_validate(data)

    def _get_high_schools_config(
        self,
        *,
        timeout_ms: Optional[int] = None,
    ) -> EndpointConfig:
        return EndpointConfig(
            path_template="/schools/high_schools.cgi",
            operation_id="getHighSchoolList",
            wait_for_element="#high_schools",
            parser=lambda html: _parser.parse_high_schools(html),
            response_type=HighSchoolList,
            path_params={},
            timeout_ms=timeout_ms,
        )

    def high_schools(
        self,
        *,
        timeout_ms: Optional[int] = None,
    ) -> HighSchoolList:
        """Fetch and parse the High Schools page from Pro Football Reference.

        Scrapes
        ``https://www.pro-football-reference.com/schools/high_schools.cgi``
        and returns structured data for the top high schools by NFL player count.

        Args:
            timeout_ms: Optional timeout in milliseconds for the page
                selector.

        Returns:
            A :class:`~griddy.pfr.models.HighSchoolList` instance containing
            all high school entries.
        """
        config = self._get_high_schools_config(timeout_ms=timeout_ms)
        data = self._execute_endpoint(config)
        return HighSchoolList.model_validate(data)
