import adsk.core, adsk.fusion, traceback
import csv


CUSTOM_PARTS = {
    "m4x12": {
        "name": "M4x12",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m4x16": {
        "name": "M4x16",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m5x12": {
        "name": "M5x12",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m5x20": {
        "name": "M5x20",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m6x12": {
        "name": "M6x12",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m6x20": {
        "name": "M6x20",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m6x30": {
        "name": "M6x30",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m6x50": {
        "name": "M6x50",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m8x8 grub": {
        "name": "M8x8 Grub",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "x m5 threaded rod": {
        "name": "X M5 Threaded Rod",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "y m5 threaded rod": {
        "name": "Y M5 Threaded Rod",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m5 nut": {
        "name": "M5 Nut",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "x m6 threaded rod": {
        "name": "X M6 Threaded Rod",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "y m6 threaded rod": {
        "name": "Y M6 Threaded Rod",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m6 nut": {
        "name": "M6 Nut",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m5 washer": {
        "name": "M5 Washer",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m6 washer": {
        "name": "M6 Washer",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "xframe tubing": {
        "name": "XFrame Tubing",
        "description": "",
        "show_length": True,
        "show_dimensions": True,
        "override_quantity": False,
    },
    "yframe tubing": {
        "name": "YFrame Tubing",
        "description": "",
        "show_length": True,
        "show_dimensions": True,
        "override_quantity": False,
    },
    "yroller tubing": {
        "name": "YRoller Tubing",
        "description": "",
        "show_length": True,
        "show_dimensions": True,
        "override_quantity": False,
    },
    "yroller brace": {
        "name": "YRoller Brace",
        "description": "",
        "show_length": False,
        "show_dimensions": True,
        "override_quantity": False,
    },
    "xgantry tubing": {
        "name": "XGantry Tubing",
        "description": "",
        "show_length": True,
        "show_dimensions": True,
        "override_quantity": False,
    },
    "xroller tubing": {
        "name": "XRoller Tubing",
        "description": "",
        "show_length": True,
        "show_dimensions": True,
        "override_quantity": False,
    },
    "xroller angle": {
        "name": "XRoller Angle",
        "description": "",
        "show_length": True,
        "show_dimensions": True,
        "override_quantity": False,
    },
    "x hgr20 rail": {
        "name": "X HGR20 Rail",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": 2,
    },
    "y hgr20 rail": {
        "name": "Y HGR20 Rail",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "y2 hgr20 rail": {
        "name": "Y2 HGR20 Rail",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "1z hgr20 rail": {
        "name": "1Z HGR20 Rail",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": 2,
    },
    "2z hgr15 rail": {
        "name": "2Z HGR15 Rail",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": 2,
    },
    "y 1610 ballscrew": {
        "name": "Y 1610 Ballscrew",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "y 2010 ballscrew": {
        "name": "Y 2010 Ballscrew",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "x 1610 ballscrew": {
        "name": "X 1610 Ballscrew",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "x 2010 ballscrew": {
        "name": "X 2010 Ballscrew",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "y2 1610 ballscrew": {
        "name": "Y2 1610 Ballscrew",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "y2 2010 ballscrew": {
        "name": "Y2 2010 Ballscrew",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "z 1204 ballscrew": {
        "name": "Z 1204 Ballscrew",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
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

    # Calculate lengths in each direction
    x = round(max_x - min_x, 2)
    y = round(max_y - min_y, 2)
    z = round(max_z - min_z, 2)

    # Format dimensions to only show decimals if needed
    format_dimension = lambda v: f"{v:.2f}".rstrip('0').rstrip('.')
    x, y, z = map(format_dimension, (x, y, z))

    # Return the largest dimension and the dimensions in XxYxZ format
    return format_dimension(max(float(x), float(y), float(z))), f"{x} x {y} x {z}"


def process_component(component, parts_list, custom_parts, visited_bodies):
    """
    Processes a component and its bodies, aggregating counts for custom parts.

    Args:
        component: The current Fusion 360 component being processed.
        parts_list: A dictionary to store aggregated counts for parts.
        custom_parts: A dictionary of custom part names and their properties.
        visited_bodies: A set to track already processed bodies.

    Returns:
        None
    """
    for body in component.bRepBodies:
        if not body.isVisible or body.entityToken in visited_bodies:
            continue
        visited_bodies.add(body.entityToken)

        # Check for custom part matches
        body_name_lower = body.name.lower()
        part_info = None
        for custom_key, custom_value in custom_parts.items():
            if body_name_lower.startswith(custom_key):
                part_info = custom_value
                break

        if part_info is None:
            continue  # Skip unmatched parts

        # Calculate the largest dimension and XxYxZ dimensions
        largest_dimension, xyz_dimensions = calculate_body_dimensions_from_vertices(body)

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
        process_component(occurrence.component, parts_list, custom_parts, visited_bodies)


def export_parts_list_to_csv(parts_list, custom_parts):
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

            with open(file_path, "w", newline="") as csvfile:
                csv_writer = csv.writer(csvfile)

                # Write the header
                csv_writer.writerow(["Position", "Name", "Description", "Quantity", "Length (mm)", "Dimensions (mm)"])

                # Sort parts by the custom_parts dictionary order
                position = 1
                for custom_key in custom_parts.keys():
                    for (name, description, length, dimensions), quantity in parts_list.items():
                        if name == custom_parts[custom_key]["name"]:
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

        parts_list = {}
        visited_bodies = set()  # Track visited bodies to avoid duplicates

        # Start processing from the root component
        process_component(root_comp, parts_list, CUSTOM_PARTS, visited_bodies)

        # Export the results to a CSV file
        csv_path = export_parts_list_to_csv(parts_list, CUSTOM_PARTS)
        if csv_path:
            ui.messageBox(f"Parts list exported: {csv_path}")
        else:
            ui.messageBox("Save operation canceled.")
    except:
        ui.messageBox("Error:\n{}".format(traceback.format_exc()))


list_and_count_parts()
