from __future__ import annotations
import logging

from typing import Any, Optional

import ckan.plugins.toolkit as tk
from ckan.plugins.interfaces import Interface

log = logging.getLogger(__name__)


class IFpx(Interface):
    """Extension point for FPX plugin."""

    def fpx_url_from_resource(self, resource: dict[str, Any]) -> Optional[str]:
        """Extract URL from the resource dictionary.

        Args:
            resource: standard resource dictionary from package/resource show
        Returns:
            String with the download URL or `None` if resource cannot be downloaded
        """
        return resource["url"]

    def fpx_normalize_items_and_type(
        self, items: list[Any], type_: str
    ) -> tuple[list[dict[str, Any]], str]:
        """Transfrom list of items into valid payload for FPX ticket ordering process.

        Args:
            items: list of strings/dictionaries/etc representing ordered items
            type_: type hint for item processing
        Returns:
            List of items accepted by FPX ticket ordering endpoint and, possibly, changed type.
        """

        if type_ == "package":
            items, type_ = self._fpx_package_normalizer(items)

        elif type_ == "resource":
            items, type_ = self._fpx_resource_normalizer(items)

        items = [
            item if isinstance(item, dict) else dict(url=item)
            for item in items
        ]

        return items, type_

    def _fpx_package_normalizer(
        self, items: list[Any]
    ) -> tuple[list[dict[str, Any]], str]:
        """Normalize items when initial type is "package" """
        if not isinstance(items, list):
            log.warning(
                "Passing items as scalar value when type set to 'package' is "
                "deprecated. Use list instead."
            )
            items = [items]

        fq_list = [
            "{!q.op=OR}id:(%s)"
            % " ".join(['"{}"'.format(item) for item in items])
        ]
        result = tk.get_action("package_search")(
            None, {"fq_list": fq_list, "include_private": True}
        )

        items = [
            {"url": self.fpx_url_from_resource(r), "path": pkg["name"]}
            for pkg in result["results"]
            for r in pkg["resources"]
        ]

        return items, "zip"

    def _fpx_resource_normalizer(
        self, items: list[Any]
    ) -> tuple[list[dict[str, Any]], str]:
        """Normalize items when initial type is "resource" """
        items = [
            {
                "url": self.fpx_url_from_resource(
                    tk.get_action("resource_show")(None, {"id": r["id"]})
                )
            }
            for r in items
        ]
        return items, "zip"
