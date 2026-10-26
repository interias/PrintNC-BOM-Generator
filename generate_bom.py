import adsk.core, adsk.fusion, traceback
import csv
import re


IGNORED_COMPONENT_PATH_PARTS = (
    "cutting area",
    "plywood",
    "printed-milled parts:1",
    "printed drill guides:1",
)


# Default body names Fusion assigns per UI language (string table key
# BodyDefaultUserName). The language of whoever created the body applies, so a
# model can mix them, e.g. "Body1" next to "Körper2".
GENERIC_BODY_NAMES = (
    "Body",     # en
    "Körper",   # de
    "Corps",    # fr
    "Cuerpo",   # es
    "Corpo",    # it, pt-BR
    "Bryła",    # pl
    "Gövde",    # tr
    "ボディ",    # ja
    "본체",      # ko
    "实体",      # zh-CN
)
GENERIC_BODY_NAME_PATTERN = re.compile(
    r"(?:" + "|".join(map(re.escape, GENERIC_BODY_NAMES)) + r")\s*(?:\d+)?(?:\s*\(\d+\))*",
    re.IGNORECASE,
)


CUSTOM_PARTS = {
    "m4x8 Pan Head": {
        "name": "M4x8 Pan Head",
        "description": "M4 pan-head screw",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m4x12": {
        "name": "M4x12",
        "description": "M4 Hex socket-head screw",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m4x16": {
        "name": "M4x16",
        "description": "M4 Hex socket-head screw",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m5x12": {
        "name": "M5x12",
        "description": "M5 Hex socket-head screw",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m5x20": {
        "name": "M5x20",
        "description": "M5 Hex socket-head screw",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
        "aliases": ["m5-20"],
    },    
    "m6x12": {
        "name": "M6x12",
        "description": "M6 Hex socket-head screw",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m6x20": {
        "name": "M6x20",
        "description": "M6 Hex socket-head screw",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m6x30": {
        "name": "M6x30",
        "description": "M6 Hex socket-head screw",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m6x50": {
        "name": "M6x50",
        "description": "M6 Hex socket-head screw",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m8x8 grub": {
        "name": "M8x8 Grub",
        "description": "M8 grub screw",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m8x45": {
        "name": "M8x45",
        "description": "M8 Hex socket-head screw",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },    
    "x m5 threaded rod": {
        "name": "X M5 Threaded Rod",
        "description": "X-axis threaded rod",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "y m5 threaded rod": {
        "name": "Y M5 Threaded Rod",
        "description": "Y-axis threaded rod",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m5 nut": {
        "name": "M5 Nut",
        "description": "M5 hex nut",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "x m6 threaded rod": {
        "name": "X M6 Threaded Rod",
        "description": "X-axis threaded rod",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "y m6 threaded rod": {
        "name": "Y M6 Threaded Rod",
        "description": "Y-axis threaded rod",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m6 nut": {
        "name": "M6 Nut",
        "description": "M6 hex nut",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m5 washer": {
        "name": "M5 Washer",
        "description": "M5 flat washer",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m6 washer": {
        "name": "M6 Washer",
        "description": "M6 flat washer",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "x hgr20 rail": {
        "name": "X HGR20 Rail",
        "description": "X-axis linear rail",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": 2,
    },
    "y hgr20 rail": {
        "name": "Y HGR20 Rail",
        "description": "Y-axis linear rail",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "1z hgr20 rail": {
        "name": "1Z HGR20 Rail",
        "description": "Z-axis linear rail",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": 2,
    },
    "2z hgr15 rail": {
        "name": "2Z HGR15 Rail",
        "description": "Z-axis linear rail",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": 2,
    },
    "hgh15ca": {
        "name": "HGH15CA slider block",
        "description": "HGR15 carriage block",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },    
    "hgw20cc": {
        "name": "HGW20CC slider block",
        "description": "HGR20 carriage block",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },    
    "y 1610 ballscrew": {
        "name": "Y 1610 Ballscrew",
        "description": "Y-axis ballscrew",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "y 2010 ballscrew": {
        "name": "Y 2010 Ballscrew",
        "description": "Y-axis ballscrew",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "x 1610 ballscrew": {
        "name": "X 1610 Ballscrew",
        "description": "X-axis ballscrew",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "x 2010 ballscrew": {
        "name": "X 2010 Ballscrew",
        "description": "X-axis ballscrew",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "z 1204 ballscrew": {
        "name": "Z 1204 Ballscrew",
        "description": "Z-axis ballscrew",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m6 flush grease fitting": {
        "name": "M6 Flush Grease Fitting",
        "description": "Flush grease fitting",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m6-1.0 90 grease fitting": {
        "name": "M6-1.0 90° Grease Fitting",
        "description": "Right-angle grease fitting",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "hm12-57": {
        "name": "HM12-57 Ballscrew Mount",
        "description": "1610 ballscrew fixed mount",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "hm15-57": {
        "name": "HM15-57 Ballscrew Mount",
        "description": "2010 ballscrew fixed mount",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "hm10-57": {
        "name": "HM10-57 Ballscrew Mount",
        "description": "1204 ballscrew fixed mount",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "bk10": {
        "name": "BK10 Ballscrew Mount",
        "description": "1204 ballscrew fixed mount",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "bk12": {
        "name": "BK12 Ballscrew Mount",
        "description": "1610 ballscrew fixed mount",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "bk15": {
        "name": "BK15 Ballscrew Mount",
        "description": "2010 ballscrew fixed mount",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "bf12": {
        "name": "BF12 Ballscrew Mount",
        "description": "Ballscrew support mount",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "bf15": {
        "name": "BF15 Ballscrew Mount",
        "description": "2010 ballscrew support mount",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "d30l40 8-10mm coupler": {
        "name": "D30L40 8-10mm Coupler",
        "description": "Motor-to-ballscrew coupler",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "d30l40 8-12mm coupler": {
        "name": "D30L40 8-12mm Coupler",
        "description": "Motor-to-ballscrew coupler",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "d25l30 8-8mm coupler": {
        "name": "D25L30 8-8mm Coupler",
        "description": "Motor-to-ballscrew coupler",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "sfu1610 nut": {
        "name": "SFU1610 Ballscrew Nut",
        "description": "1610 ballscrew nut",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "sfu2010 nut": {
        "name": "SFU2010 Ballscrew Nut",
        "description": "2010 ballscrew nut",
        "show_length": False,
        "show_dimensions": False,
        # The X-axis nut body is generically named "Body1" in V4.0.37.
        "override_quantity": 3,
    },
    # Keep the more specific nut-block entry before the nut entry because names
    # are matched by prefix after normalization.
    "sfu1204 ballscrew nut block 22mm bore": {
        "name": "SFU1204 Ballscrew Nut Block (22mm Bore)",
        "description": "1204 nut mounting block",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "sfu1204 ballscrew nut": {
        "name": "SFU1204 Ballscrew Nut",
        "description": "1204 ballscrew nut",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "nema23 stepper": {
        "name": "NEMA23 Stepper Motor and Driver",
        "description": "Axis stepper motor and driver",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m8 npn-nc inductive sensor": {
        "name": "M8 NPN-NC Inductive Sensor",
        "description": "Inductive limit sensor",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "80mm 3 hole spindle clamp": {
        "name": "80mm 3-Hole Spindle Clamp",
        "description": "80mm spindle mount",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "80mm 2.2kw spindle": {
        "name": "80mm 2.2kW Spindle",
        "description": "Water-cooled spindle",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "wasteboard": {
        "name": "Wasteboard",
        "description": "Replaceable work surface",
        "show_length": False,
        "show_dimensions": True,
        "override_quantity": False,
        "category": "fabricated",
    },
    "xrollershim": {
        "name": "X Roller Shim (alu or steel)",
        "description": "X-roller alignment shim (alu easier for manual cutting/drilling)",
        "show_length": False,
        "show_dimensions": True,
        "override_quantity": False,
        "category": "fabricated",
    },
    "1z plate": {
        "name": "1Z Plate (alu or steel)",
        "description": "Single-carriage Z plate (alu easier for manual cutting/drilling)",
        "show_length": False,
        "show_dimensions": True,
        "override_quantity": False,
        "category": "fabricated",
    },
    "2z 300mm z plate": {
        "name": "2Z Plate (alu or steel)",
        "description": "Dual-carriage Z plate (alu easier for manual cutting/drilling)",
        "show_length": False,
        "show_dimensions": True,
        "override_quantity": False,
        "category": "fabricated",
    },
    "2z tram plate": {
        "name": "2Z Tram Plate (alu or steel)",
        "description": "Spindle tram plate (alu easier for manual cutting/drilling)",
        "show_length": False,
        "show_dimensions": True,
        "override_quantity": False,
        "category": "fabricated",
    },
    "2z zplate tram bar": {
        "name": "2Z Tram Bar (alu or steel)",
        "description": "Z-plate tram bar (alu easier for manual cutting/drilling)",
        "show_length": False,
        "show_dimensions": True,
        "override_quantity": False,
        "category": "fabricated",
    },
    "2z spindle clamp tram blocks": {
        "name": "2Z Spindle Clamp Tram Block (alu or steel)",
        "description": "Spindle clamp tram block (alu easier for manual cutting/drilling)",
        "show_length": False,
        "show_dimensions": True,
        "override_quantity": False,
        "category": "fabricated",
    },
    "xframe tubing": {
        "name": "X Frame Tubing (steel)",
        "description": "X-frame steel tubing",
        "show_length": True,
        "show_dimensions": True,
        "override_quantity": False,
        "category": "fabricated",
    },
    "yframe tubing": {
        "name": "Y Frame Tubing (steel)",
        "description": "Y-frame steel tubing",
        "show_length": True,
        "show_dimensions": True,
        "override_quantity": False,
        "category": "fabricated",
    },
    "yroller tubing": {
        "name": "Y Roller Tubing (steel)",
        "description": "Y-roller steel tubing",
        "show_length": True,
        "show_dimensions": True,
        "override_quantity": False,
        "category": "fabricated",
    },
    "yroller brace": {
        "name": "Y Roller Brace (alu or steel)",
        "description": "Y-roller brace (alu easier for manual cutting/drilling)",
        "show_length": False,
        "show_dimensions": True,
        "override_quantity": False,
        "category": "fabricated",
    },
    "xgantry tubing": {
        "name": "X Gantry Tubing (steel)",
        "description": "X-gantry steel tubing",
        "show_length": True,
        "show_dimensions": True,
        "override_quantity": False,
        "category": "fabricated",
    },
    "xroller tubing": {
        "name": "X Roller Tubing (steel)",
        "description": "X-roller steel tubing",
        "show_length": True,
        "show_dimensions": True,
        "override_quantity": False,
        "category": "fabricated",
    },
    "xroller angle": {
        "name": "X Roller Angle (alu or steel)",
        "description": "X-roller angle (alu easier for manual cutting/drilling)",
        "show_length": True,
        "show_dimensions": True,
        "override_quantity": False,
        "category": "fabricated",
    },
}


def calculate_body_dimensions_from_vertices(body):
    """
    Calculates the dimensions of a body using its vertices.

    Args:
        body: The Fusion 360 body to measure.

    Returns:
        A tuple containing:
        - The largest dimension (float) of the body in millimeters.
        - A string in the format "XxYxZ" with dimensions in millimeters.
    """
    min_x = min_y = min_z = float("inf")
    max_x = max_y = max_z = float("-inf")

    for vertex in body.vertices:
        point = vertex.geometry
        min_x = min(min_x, point.x * 10)  # Convert cm to mm
        min_y = min(min_y, point.y * 10)  # Convert cm to mm
        min_z = min(min_z, point.z * 10)  # Convert cm to mm
        max_x = max(max_x, point.x * 10)  # Convert cm to mm
        max_y = max(max_y, point.y * 10)  # Convert cm to mm
        max_z = max(max_z, point.z * 10)  # Convert cm to mm

    # Calculate lengths in each direction and sort descending for reporting.
    dimensions = sorted(
        [round(max_x - min_x, 2), round(max_y - min_y, 2), round(max_z - min_z, 2)],
        reverse=True,
    )

    # Format dimensions to only show decimals if needed
    format_dimension = lambda v: f"{v:.2f}".rstrip('0').rstrip('.')
    x, y, z = map(format_dimension, dimensions)

    # Return the largest dimension and the dimensions in XxYxZ format
    return x, f"{x} x {y} x {z}"


def normalize_name(s):
    """Normalize a name for matching: lowercase and strip non-alphanumerics."""
    if not s:
        return ""
    return re.sub(r'[^0-9a-z]', '', s.lower())


def find_custom_part(name, custom_parts):
    """Return the custom part definition matching a body name, if any."""
    name_norm = normalize_name(name)
    for custom_key, custom_value in custom_parts.items():
        candidates = [custom_key] + (custom_value.get("aliases", []) or [])
        if any(name_norm.startswith(normalize_name(candidate)) for candidate in candidates):
            return custom_value

    return None


def is_generic_body_name(name):
    """Return whether a Fusion body has an automatically generated name."""
    if not name:
        return True
    return GENERIC_BODY_NAME_PATTERN.fullmatch(name.strip()) is not None


def process_component(component, component_path, parts_list, custom_parts, unrecognized_parts):
    """
    Processes a component and its bodies, aggregating counts for custom parts.

    Args:
        component: The current Fusion 360 component being processed.
        component_path: Full component path for reporting.
        parts_list: A dictionary to store aggregated counts for parts.
        custom_parts: A dictionary of custom part names and their properties.
    Returns:
        None
    """
    # Reference geometry, temporary parts, and fabrication guides are not BOM items.
    component_path_lower = component_path.lower()
    if any(path_part in component_path_lower for path_part in IGNORED_COMPONENT_PATH_PARTS):
        return

    visible_bodies = [body for body in component.bRepBodies if body.isVisible]
    body_matches = [(body, find_custom_part(body.name, custom_parts)) for body in visible_bodies]
    has_recognized_body = any(part_info is not None for _, part_info in body_matches)

    # Some parts (e.g. the 2Z plates) only carry their name on the component and
    # consist of generically named bodies; identify those by the component name.
    if not has_recognized_body:
        component_part = find_custom_part(component.name, custom_parts)
        if component_part is not None:
            body_matches = [
                (body, component_part if is_generic_body_name(body.name) else part_info)
                for body, part_info in body_matches
            ]

    for body, part_info in body_matches:
        # Imported hardware often consists of one properly named body plus
        # several bodies named Body1, Body2 (1), etc. Those generic siblings do
        # not represent additional BOM items.
        if part_info is None and has_recognized_body and is_generic_body_name(body.name):
            continue

        # Calculate the largest dimension and XxYxZ dimensions for reporting
        largest_dimension, xyz_dimensions = calculate_body_dimensions_from_vertices(body)

        if part_info is None:
            # Collect unrecognized parts (count by body name + dimensions)
            display_name = body.name if body.name else "Unnamed Body"
            key_unrec = (display_name, xyz_dimensions, component_path)
            if key_unrec in unrecognized_parts:
                unrecognized_parts[key_unrec] += 1
            else:
                unrecognized_parts[key_unrec] = 1
            continue

        # Get dimensions and length based on custom parts configuration
        name = part_info["name"]
        description = part_info["description"]
        length = largest_dimension if part_info.get("show_length", False) else None
        dimensions = xyz_dimensions if part_info.get("show_dimensions", False) else None
        override_quantity = part_info.get("override_quantity", False)

        # Set quantity directly if override_quantity is provided
        quantity = override_quantity if override_quantity else 1

        # Aggregate the part in the parts list
        key = (name, description, length, dimensions)  # Use name, description, length, and dimensions as the unique key
        if key in parts_list:
            if override_quantity is False:
                parts_list[key] += 1
        else:
            parts_list[key] = quantity

    # Process sub-components recursively
    for occurrence in component.occurrences:
        occ_name = occurrence.name or occurrence.component.name
        next_path = f"{component_path}->{occ_name}" if component_path else occ_name
        process_component(occurrence.component, next_path, parts_list, custom_parts, unrecognized_parts)


def export_parts_list_to_csv(parts_list, custom_parts, unrecognized_parts, model_name, cutting_area):
    """
    Exports the aggregated parts list to a CSV file.

    Args:
        parts_list: A dictionary with aggregated parts data.

    Returns:
        The path to the saved CSV file or None if the save operation is canceled.
    """
    app = adsk.core.Application.get()
    ui = app.userInterface
    try:
        file_dialog = ui.createFileDialog()
        file_dialog.isMultiSelectEnabled = False
        file_dialog.title = "Select Save Location for the Parts List CSV"
        file_dialog.filter = "CSV Files (*.csv)"
        file_dialog.filterIndex = 0
        dialog_result = file_dialog.showSave()

        if dialog_result == adsk.core.DialogResults.DialogOK:
            file_path = file_dialog.filename

            # Keep the platform encoding so Excel honors "sep=", but don't fail on
            # characters it cannot represent (e.g. Japanese body names).
            with open(file_path, "w", newline="", errors="replace") as csvfile:
                # Tell Excel to use commas regardless of the system list separator.
                csvfile.write("sep=,\n")
                csv_writer = csv.writer(csvfile)

                # Header section
                csv_writer.writerow([f"Model: {model_name}"])
                csv_writer.writerow([f"Cutting Area: {cutting_area}"])
                csv_writer.writerow([])

                def write_parts_section(title, category):
                    csv_writer.writerow([title])
                    csv_writer.writerow(
                        ["Position", "Name", "Description", "Quantity", "Length (mm)", "Dimensions (mm)"]
                    )

                    position = 1
                    for custom_key, custom_part in custom_parts.items():
                        if custom_part.get("category", "purchased") != category:
                            continue

                        for (name, description, length, dimensions), quantity in parts_list.items():
                            if name == custom_part["name"]:
                                csv_writer.writerow(
                                    [
                                        position,
                                        name,
                                        description,
                                        quantity,
                                        length if length is not None else "",
                                        dimensions if dimensions is not None else "",
                                    ]
                                )
                                position += 1

                write_parts_section("Purchased Components", "purchased")
                csv_writer.writerow([])
                csv_writer.writerow([])
                write_parts_section(
                    "Locally Sourced & Fabricated Parts",
                    "fabricated",
                )

                # Write unrecognized parts (if any)
                if unrecognized_parts:
                    csv_writer.writerow([])
                    csv_writer.writerow([])
                    csv_writer.writerow([])
                    csv_writer.writerow(["Unrecognized Parts (only relevant if Fusion model changes and can usually be ignored)"])
                    csv_writer.writerow(["Position", "Name", "Description", "Quantity", "Length (mm)", "Dimensions (mm)", "Path"])
                    pos_unrec = 1
                    for (name, dimensions, path), quantity in unrecognized_parts.items():
                        csv_writer.writerow([pos_unrec, name, "", quantity, "", dimensions, path])
                        pos_unrec += 1

            return file_path
        else:
            return None
    except Exception as e:
        return str(e)


def list_and_count_parts():
    """
    Main function to execute the parts counting script in Fusion 360.

    This function initializes the required variables, processes the root component, and exports the results to a CSV file.
    """
    app = adsk.core.Application.get()
    ui = app.userInterface
    try:
        design = app.activeProduct
        if not isinstance(design, adsk.fusion.Design):
            ui.messageBox("Please open a Fusion 360 design.")
            return

        root_comp = design.rootComponent
        model_name = design.parentDocument.name if design.parentDocument else root_comp.name

        def get_param_text(param_name):
            param = None
            if hasattr(design, "userParameters") and design.userParameters:
                param = design.userParameters.itemByName(param_name)
            if (param is None) and hasattr(design, "allParameters") and design.allParameters:
                param = design.allParameters.itemByName(param_name)
            if param is None:
                return ""
            return param.expression if hasattr(param, "expression") else str(param.value)

        x_cutting_area = get_param_text("XCuttingArea")
        y_cutting_area = get_param_text("YCuttingArea")
        cutting_area = f"{x_cutting_area} x {y_cutting_area}"

        parts_list = {}
        unrecognized_parts = {}

        # Process full assembly from root component, but omit root name in reported sub-paths.
        process_component(root_comp, "", parts_list, CUSTOM_PARTS, unrecognized_parts)

        # Export the results to a CSV file
        csv_path = export_parts_list_to_csv(parts_list, CUSTOM_PARTS, unrecognized_parts, model_name, cutting_area)
        if csv_path:
            ui.messageBox(f"Parts list exported: {csv_path}")
        else:
            ui.messageBox("Save operation canceled.")
    except:
        ui.messageBox("Error:\n{}".format(traceback.format_exc()))


list_and_count_parts()
