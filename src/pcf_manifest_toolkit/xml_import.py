"""Import ControlManifest.Input.xml into manifest data."""

from __future__ import annotations

import xml.etree.ElementTree as ET
import sys
from typing import Any, Callable


def parse_manifest_xml_path(path: str) -> dict[str, Any]:
    """Parse a manifest XML file into a dict suitable for Manifest model validation."""
    if path == "-":
        xml_text = sys.stdin.read()
        return parse_manifest_xml_text(xml_text)
    tree = ET.parse(path)
    return parse_manifest_xml_element(tree.getroot())


def parse_manifest_xml_text(xml_text: str) -> dict[str, Any]:
    """Parse a manifest XML string into a dict suitable for Manifest model validation."""
    root = ET.fromstring(xml_text)
    return parse_manifest_xml_element(root)


def parse_manifest_xml_element(root: ET.Element) -> dict[str, Any]:
    """Parse the manifest XML root element into a dict."""
    if _strip_ns(root.tag) != "manifest":
        raise ValueError("Root element must be <manifest>.")

    control_el = _first_child(root, "control")
    if control_el is None:
        raise ValueError("Manifest must contain a <control> element.")

    control = _parse_control(control_el)
    return {"control": control}


def _parse_control(control_el: ET.Element) -> dict[str, Any]:
    data: dict[str, Any] = {}
    _set_attr(data, control_el, "namespace")
    _set_attr(data, control_el, "constructor")
    _set_attr(data, control_el, "version")
    _set_attr(data, control_el, "display-name-key")
    _set_attr(data, control_el, "description-key")
    _set_attr(data, control_el, "control-type")
    _set_attr(data, control_el, "preview-image")

    data["property"] = [_parse_property(el) for el in _children(control_el, "property")]
    data["event"] = [_parse_event(el) for el in _children(control_el, "event")]
    data["data-set"] = [_parse_dataset(el) for el in _children(control_el, "data-set")]
    data["type-group"] = [
        _parse_type_group(el) for el in _children(control_el, "type-group")
    ]

    prop_deps = _first_child(control_el, "property-dependencies")
    if prop_deps is not None:
        data["property-dependencies"] = _parse_property_dependencies(prop_deps)

    feature_usage = _first_child(control_el, "feature-usage")
    if feature_usage is not None:
        data["feature-usage"] = _parse_feature_usage(feature_usage)

    external_usage = _first_child(control_el, "external-service-usage")
    if external_usage is not None:
        data["external-service-usage"] = _parse_external_service_usage(external_usage)

    platform_action = _first_child(control_el, "platform-action")
    if platform_action is not None:
        data["platform-action"] = _parse_platform_action(platform_action)

    resources = _first_child(control_el, "resources")
    if resources is not None:
        data["resources"] = _parse_resources(resources)

    return data


def _parse_property(property_el: ET.Element) -> dict[str, Any]:
    data: dict[str, Any] = {}
    for attr in (
        "name",
        "display-name-key",
        "description-key",
        "of-type",
        "of-type-group",
        "usage",
        "default-value",
        "pfx-default-value",
    ):
        _set_attr(data, property_el, attr)
    _set_bool_attr(data, property_el, "required")

    types_el = _first_child(property_el, "types")
    if types_el is not None:
        data["types"] = _parse_types(types_el)

    values = [_parse_value(el) for el in _children(property_el, "value")]
    if values:
        data["value"] = values

    return data


def _parse_value(value_el: ET.Element) -> dict[str, Any]:
    data: dict[str, Any] = {}
    _set_attr(data, value_el, "name")
    _set_attr(data, value_el, "display-name-key")
    text = (value_el.text or "").strip()
    if text:
        try:
            data["value"] = int(text)
        except ValueError:
            data["value"] = text
    return data


def _parse_event(event_el: ET.Element) -> dict[str, Any]:
    data: dict[str, Any] = {}
    for attr in (
        "name",
        "display-name-key",
        "description-key",
        "pfx-default-value",
    ):
        _set_attr(data, event_el, attr)
    return data


def _parse_dataset(dataset_el: ET.Element) -> dict[str, Any]:
    data: dict[str, Any] = {}
    for attr in (
        "name",
        "display-name-key",
        "description-key",
        "cds-data-set-options",
    ):
        _set_attr(data, dataset_el, attr)
    data["property-set"] = [
        _parse_property_set(el) for el in _children(dataset_el, "property-set")
    ]
    return data


def _parse_property_set(prop_set_el: ET.Element) -> dict[str, Any]:
    data: dict[str, Any] = {}
    for attr in (
        "name",
        "display-name-key",
        "description-key",
        "of-type",
        "of-type-group",
        "usage",
    ):
        _set_attr(data, prop_set_el, attr)
    _set_bool_attr(data, prop_set_el, "required")
    types_el = _first_child(prop_set_el, "types")
    if types_el is not None:
        data["types"] = _parse_types(types_el)
    return data


def _parse_types(types_el: ET.Element) -> dict[str, Any]:
    types = []
    for type_el in _children(types_el, "type"):
        value = (type_el.text or "").strip()
        if value:
            types.append({"value": value})
    return {"type": types}


def _parse_type_group(type_group_el: ET.Element) -> dict[str, Any]:
    data: dict[str, Any] = {}
    _set_attr(data, type_group_el, "name")
    types = []
    for type_el in _children(type_group_el, "type"):
        value = (type_el.text or "").strip()
        if value:
            types.append({"value": value})
    data["type"] = types
    return data


def _parse_property_dependencies(deps_el: ET.Element) -> dict[str, Any]:
    deps = []
    for dep_el in _children(deps_el, "property-dependency"):
        item: dict[str, Any] = {}
        for attr in ("input", "output", "required-for"):
            _set_attr(item, dep_el, attr)
        deps.append(item)
    return {"property-dependency": deps}


def _parse_feature_usage(feature_el: ET.Element) -> dict[str, Any]:
    uses_features = []
    for use_el in _children(feature_el, "uses-feature"):
        item: dict[str, Any] = {}
        _set_attr(item, use_el, "name")
        _set_bool_attr(item, use_el, "required")
        uses_features.append(item)
    return {"uses-feature": uses_features}


def _parse_external_service_usage(usage_el: ET.Element) -> dict[str, Any]:
    data: dict[str, Any] = {}
    _set_bool_attr(data, usage_el, "enabled")
    domains = []
    for dom_el in _children(usage_el, "domain"):
        text = (dom_el.text or "").strip()
        if text:
            domains.append({"value": text})
    if domains:
        data["domain"] = domains
    return data


def _parse_platform_action(action_el: ET.Element) -> dict[str, Any]:
    data: dict[str, Any] = {}
    _set_attr(data, action_el, "action-type")
    return data


def _parse_resources(resources_el: ET.Element) -> dict[str, Any]:
    data: dict[str, Any] = {}
    code_el = _first_child(resources_el, "code")
    if code_el is not None:
        data["code"] = _parse_code(code_el)

    data["css"] = [_parse_css(el) for el in _children(resources_el, "css")]
    data["img"] = [_parse_img(el) for el in _children(resources_el, "img")]
    data["resx"] = [_parse_resx(el) for el in _children(resources_el, "resx")]
    data["platform-library"] = [
        _parse_platform_library(el) for el in _children(resources_el, "platform-library")
    ]
    data["dependency"] = [
        _parse_dependency(el) for el in _children(resources_el, "dependency")
    ]
    return data


def _parse_code(code_el: ET.Element) -> dict[str, Any]:
    data: dict[str, Any] = {}
    _set_attr(data, code_el, "path")
    _set_int_attr(data, code_el, "order")
    return data


def _parse_css(css_el: ET.Element) -> dict[str, Any]:
    data: dict[str, Any] = {}
    _set_attr(data, css_el, "path")
    _set_int_attr(data, css_el, "order")
    return data


def _parse_img(img_el: ET.Element) -> dict[str, Any]:
    data: dict[str, Any] = {}
    _set_attr(data, img_el, "path")
    return data


def _parse_resx(resx_el: ET.Element) -> dict[str, Any]:
    data: dict[str, Any] = {}
    _set_attr(data, resx_el, "path")
    _set_attr(data, resx_el, "version")
    return data


def _parse_platform_library(lib_el: ET.Element) -> dict[str, Any]:
    data: dict[str, Any] = {}
    _set_attr(data, lib_el, "name")
    _set_attr(data, lib_el, "version")
    return data


def _parse_dependency(dep_el: ET.Element) -> dict[str, Any]:
    data: dict[str, Any] = {}
    _set_attr(data, dep_el, "type")
    _set_attr(data, dep_el, "name")
    _set_int_attr(data, dep_el, "order")
    _set_attr(data, dep_el, "load-type")
    return data


def _strip_ns(tag: str) -> str:
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def _children(parent: ET.Element, tag: str) -> list[ET.Element]:
    return [child for child in parent if _strip_ns(child.tag) == tag]


def _first_child(parent: ET.Element, tag: str) -> ET.Element | None:
    for child in parent:
        if _strip_ns(child.tag) == tag:
            return child
    return None


def _set_attr(target: dict[str, Any], element: ET.Element, attr: str) -> None:
    if attr in element.attrib:
        value = element.attrib[attr]
        if value != "":
            target[attr] = value


def _set_bool_attr(target: dict[str, Any], element: ET.Element, attr: str) -> None:
    if attr in element.attrib:
        value = element.attrib[attr].strip().lower()
        if value in {"true", "false"}:
            target[attr] = value == "true"


def _set_int_attr(target: dict[str, Any], element: ET.Element, attr: str) -> None:
    if attr in element.attrib:
        raw = element.attrib[attr].strip()
        if raw == "":
            return
        try:
            target[attr] = int(raw)
        except ValueError:
            target[attr] = raw
