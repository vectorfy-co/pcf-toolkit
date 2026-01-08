"""XML serialization for PCF manifest models."""

from __future__ import annotations

from dataclasses import dataclass
import xml.etree.ElementTree as ET
from typing import Iterable

from pcf_manifest_toolkit import models

@dataclass(frozen=True)
class ManifestXmlSerializer:
    """Serializes manifest models into deterministic XML."""

    indent: str = "   "
    xml_declaration: bool = True
    encoding: str = "utf-8"

    def to_string(self, manifest: models.Manifest) -> str:
        """Serialize a manifest model to XML string."""
        root = self._manifest_to_element(manifest)
        tree = ET.ElementTree(root)
        ET.indent(tree, space=self.indent)
        data = ET.tostring(root, encoding=self.encoding, xml_declaration=self.xml_declaration)
        return data.decode(self.encoding)

    def _manifest_to_element(self, manifest: models.Manifest) -> ET.Element:
        root = ET.Element("manifest")
        root.append(self._control_to_element(manifest.control))
        return root

    def _control_to_element(self, control: models.Control) -> ET.Element:
        attribs = self._ordered_attribs(
            [
                ("namespace", control.namespace),
                ("constructor", control.constructor),
                ("version", control.version),
                ("display-name-key", control.display_name_key),
                ("description-key", control.description_key),
                ("control-type", control.control_type.value if control.control_type else None),
                ("preview-image", control.preview_image),
            ]
        )
        element = ET.Element("control", attrib=attribs)
        for item in control.property:
            element.append(self._property_to_element(item))
        for item in control.event:
            element.append(self._event_to_element(item))
        for item in control.data_set:
            element.append(self._dataset_to_element(item))
        for item in control.type_group:
            element.append(self._type_group_to_element(item))
        if control.property_dependencies:
            element.append(self._property_dependencies_to_element(control.property_dependencies))
        if control.feature_usage:
            element.append(self._feature_usage_to_element(control.feature_usage))
        if control.external_service_usage:
            element.append(self._external_service_usage_to_element(control.external_service_usage))
        if control.platform_action:
            element.append(self._platform_action_to_element(control.platform_action))
        element.append(self._resources_to_element(control.resources))
        return element

    def _property_to_element(self, prop: models.Property) -> ET.Element:
        attribs = self._ordered_attribs(
            [
                ("name", prop.name),
                ("display-name-key", prop.display_name_key),
                ("description-key", prop.description_key),
                ("of-type", prop.of_type.value if prop.of_type else None),
                ("of-type-group", prop.of_type_group),
                ("usage", prop.usage.value if prop.usage else None),
                ("required", self._bool_value(prop.required)),
                ("default-value", prop.default_value),
                ("pfx-default-value", prop.pfx_default_value),
            ]
        )
        element = ET.Element("property", attrib=attribs)
        if prop.types:
            element.append(self._types_to_element(prop.types))
        for value in prop.values:
            element.append(self._enum_value_to_element(value))
        return element

    def _event_to_element(self, event: models.Event) -> ET.Element:
        attribs = self._ordered_attribs(
            [
                ("name", event.name),
                ("pfx-default-value", event.pfx_default_value),
                ("display-name-key", event.display_name_key),
                ("description-key", event.description_key),
            ]
        )
        return ET.Element("event", attrib=attribs)

    def _dataset_to_element(self, dataset: models.DataSet) -> ET.Element:
        attribs = self._ordered_attribs(
            [
                ("name", dataset.name),
                ("display-name-key", dataset.display_name_key),
                ("description-key", dataset.description_key),
                ("cds-data-set-options", dataset.cds_data_set_options),
            ]
        )
        element = ET.Element("data-set", attrib=attribs)
        for prop_set in dataset.property_set:
            element.append(self._property_set_to_element(prop_set))
        return element

    def _property_set_to_element(self, prop_set: models.PropertySet) -> ET.Element:
        attribs = self._ordered_attribs(
            [
                ("name", prop_set.name),
                ("display-name-key", prop_set.display_name_key),
                ("description-key", prop_set.description_key),
                ("of-type", prop_set.of_type.value if prop_set.of_type else None),
                ("of-type-group", prop_set.of_type_group),
                ("usage", prop_set.usage.value if prop_set.usage else None),
                ("required", self._bool_value(prop_set.required)),
            ]
        )
        element = ET.Element("property-set", attrib=attribs)
        if prop_set.types:
            element.append(self._types_to_element(prop_set.types))
        return element

    def _type_group_to_element(self, group: models.TypeGroup) -> ET.Element:
        attribs = self._ordered_attribs([("name", group.name)])
        element = ET.Element("type-group", attrib=attribs)
        for item in group.types:
            element.append(self._type_element(item))
        return element

    def _types_to_element(self, types_element: models.TypesElement) -> ET.Element:
        element = ET.Element("types")
        for item in types_element.types:
            element.append(self._type_element(item))
        return element

    def _type_element(self, type_element: models.TypeElement) -> ET.Element:
        element = ET.Element("type")
        element.text = type_element.value.value
        return element

    def _enum_value_to_element(self, value: models.EnumValue) -> ET.Element:
        attribs = self._ordered_attribs(
            [
                ("name", value.name),
                ("display-name-key", value.display_name_key),
            ]
        )
        element = ET.Element("value", attrib=attribs)
        element.text = str(value.value)
        return element

    def _property_dependencies_to_element(
        self, deps: models.PropertyDependencies
    ) -> ET.Element:
        element = ET.Element("property-dependencies")
        for dep in deps.property_dependency:
            element.append(self._property_dependency_to_element(dep))
        return element

    def _property_dependency_to_element(
        self, dep: models.PropertyDependency
    ) -> ET.Element:
        attribs = self._ordered_attribs(
            [
                ("input", dep.input),
                ("output", dep.output),
                ("required-for", dep.required_for.value),
            ]
        )
        return ET.Element("property-dependency", attrib=attribs)

    def _feature_usage_to_element(self, usage: models.FeatureUsage) -> ET.Element:
        element = ET.Element("feature-usage")
        for item in usage.uses_feature:
            element.append(self._uses_feature_to_element(item))
        return element

    def _uses_feature_to_element(self, feature: models.UsesFeature) -> ET.Element:
        attribs = self._ordered_attribs(
            [
                ("name", feature.name),
                ("required", self._bool_value(feature.required)),
            ]
        )
        return ET.Element("uses-feature", attrib=attribs)

    def _external_service_usage_to_element(
        self, usage: models.ExternalServiceUsage
    ) -> ET.Element:
        attribs = self._ordered_attribs(
            [("enabled", self._bool_value(usage.enabled))]
        )
        element = ET.Element("external-service-usage", attrib=attribs)
        for domain in usage.domain:
            element.append(self._domain_to_element(domain))
        return element

    def _domain_to_element(self, domain: models.Domain) -> ET.Element:
        element = ET.Element("domain")
        element.text = domain.value
        return element

    def _platform_action_to_element(
        self, action: models.PlatformAction
    ) -> ET.Element:
        attribs = self._ordered_attribs(
            [("action-type", action.action_type.value if action.action_type else None)]
        )
        return ET.Element("platform-action", attrib=attribs)

    def _resources_to_element(self, resources: models.Resources) -> ET.Element:
        element = ET.Element("resources")
        element.append(self._code_to_element(resources.code))
        for item in resources.css:
            element.append(self._css_to_element(item))
        for item in resources.resx:
            element.append(self._resx_to_element(item))
        for item in resources.img:
            element.append(self._img_to_element(item))
        for item in resources.platform_library:
            element.append(self._platform_library_to_element(item))
        for item in resources.dependency:
            element.append(self._dependency_to_element(item))
        return element

    def _code_to_element(self, code: models.Code) -> ET.Element:
        attribs = self._ordered_attribs(
            [("path", code.path), ("order", str(code.order))]
        )
        return ET.Element("code", attrib=attribs)

    def _css_to_element(self, css: models.Css) -> ET.Element:
        attribs = self._ordered_attribs(
            [("path", css.path), ("order", str(css.order) if css.order else None)]
        )
        return ET.Element("css", attrib=attribs)

    def _img_to_element(self, img: models.Img) -> ET.Element:
        attribs = self._ordered_attribs([("path", img.path)])
        return ET.Element("img", attrib=attribs)

    def _resx_to_element(self, resx: models.Resx) -> ET.Element:
        attribs = self._ordered_attribs(
            [("path", resx.path), ("version", resx.version)]
        )
        return ET.Element("resx", attrib=attribs)

    def _platform_library_to_element(
        self, library: models.PlatformLibrary
    ) -> ET.Element:
        attribs = self._ordered_attribs(
            [("name", library.name.value), ("version", library.version)]
        )
        return ET.Element("platform-library", attrib=attribs)

    def _dependency_to_element(self, dependency: models.Dependency) -> ET.Element:
        attribs = self._ordered_attribs(
            [
                ("type", dependency.type.value),
                ("name", dependency.name),
                ("order", str(dependency.order) if dependency.order else None),
                ("load-type", dependency.load_type.value if dependency.load_type else None),
            ]
        )
        return ET.Element("dependency", attrib=attribs)

    def _ordered_attribs(self, pairs: Iterable[tuple[str, str | None]]) -> dict[str, str]:
        attribs: dict[str, str] = {}
        for key, value in pairs:
            if value is None or value == "":
                continue
            attribs[key] = value
        return attribs

    def _bool_value(self, value: bool | None) -> str | None:
        if value is None:
            return None
        return "true" if value else "false"
