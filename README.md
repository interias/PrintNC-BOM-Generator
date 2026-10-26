# PrintNC BOM Generator

A Python-based tool to automate the creation of detailed Bills of Materials (BOM) for **PrintNC** builds. This tool organizes parts, calculates dimensions, and exports the BOM in CSV format for easy use and documentation.

---

## Features

- **Automated BOM Generation**: Recursively scans the full component hierarchy from the root component and generates a detailed BOM.
- **Customizable Part Data**: Use a configurable `CUSTOM_PARTS` dictionary to manage part names, descriptions, and display options.
- **Flexible Name Matching**: Body names are normalized (lowercased, non-alphanumerics stripped) and matched by prefix. Optional `aliases` let one part definition match several body names.
- **Dimension and Length Calculation**: Calculates the largest dimension or detailed dimensions (XxYxZ) for parts based on configuration.
- **Generic-Body Filtering**: Imported hardware often ships as one named body plus siblings named `Body1`, `Body (2)`, etc. These generic siblings are skipped so they don't inflate quantities.
- **Ignored Components**: Reference geometry, temporary parts, and fabrication guides (e.g. cutting area, plywood, drill guides) are excluded from the BOM.
- **Purchased vs. Fabricated Sections**: Parts are split into *Purchased Components* and *Locally Sourced & Fabricated Parts* based on each part's `category`.
- **Unrecognized Parts Report**: Bodies that don't match any custom part are listed in a separate section (with their model path) so model changes can be spotted.
- **Model & Cutting-Area Header**: The CSV header includes the model name and the cutting area read from the `XCuttingArea` / `YCuttingArea` Fusion parameters.
- **CSV Export**: Exports the BOM to a structured CSV file, prefixed with a `sep=,` directive so Excel opens it correctly regardless of the system list separator.
- **BOM Sorted by CUSTOM_PARTS dict**: Within each section, parts appear in the order they are defined in `CUSTOM_PARTS`.

---

## Installation

Follow the Fusion 360 manual for creating a new script and paste in `generate_bom.py`: https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-9701BBA7-EC0E-4016-A9C8-964AA4838954

## Usage

1. Open a **Fusion 360** project for your PrintNC design.
2. Run the script from the `Scripts and Add-Ins` menu.
3. The script will:
   - Scan the model hierarchy.
   - Identify parts based on the configurable `custom_parts` dictionary.
   - Calculate quantities, dimensions, and other details.
   - Export the BOM to a CSV file.
4. Save the CSV file to your desired location.

---

## Configuration

The tool uses a `CUSTOM_PARTS` dictionary (defined at the top of `generate_bom.py`) to define each part. The **key** is a normalized lowercase string matched against the start of each body's name. Each value supports:

- **name**: A readable name for the part shown in the BOM (e.g., `"M5 Nut"`).
- **description**: Additional information about the part.
- **show_length**: Whether to display the largest dimension in mm (`True` or `False`).
- **show_dimensions**: Whether to display full dimensions in `XxYxZ` format (`True` or `False`).
- **override_quantity**: If `False`, the quantity is aggregated by counting matching bodies. If an integer `> 0` is provided, that fixed value is used as the quantity instead.
- **category** *(optional)*: `"purchased"` or `"fabricated"`; defaults to `"purchased"`.
- **aliases** *(optional)*: A list of additional key strings that should also match this part.
- **supplier_hint** *(optional)*: Where to source the part, shown in the **Supplier Hint** column when `INCLUDE_SUPPLIER_HINTS = True` (off by default). The bundled hints are sourcing routes for EU builders, not fixed quotes.

> **Note:** Matching is by normalized prefix, so define more specific keys before more general ones (e.g. `"sfu1204 ballscrew nut block 22mm bore"` before `"sfu1204 ballscrew nut"`).

### Example `CUSTOM_PARTS` Entries

```python
CUSTOM_PARTS = {
    "m5 nut": {
        "name": "M5 Nut",
        "description": "M5 hex nut",
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
    "1z hgr20 rail": {
        "name": "1Z HGR20 Rail",
        "description": "Z-axis linear rail",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": 2,
    },
    "xframe tubing": {
        "name": "Steel: X Frame Tubing",
        "description": "X-frame steel tubing",
        "show_length": True,
        "show_dimensions": True,
        "override_quantity": False,
        "category": "fabricated",
    },
}
```

Components whose path contains any of the entries in `IGNORED_COMPONENT_PATH_PARTS`
(e.g. cutting area, plywood, printed/milled parts, drill guides) are skipped entirely.

---

## Output

The exported CSV starts with a `sep=,` line (for Excel) followed by a header with the model name and cutting area, then the parts grouped into sections:

1. **Purchased Components** — parts with `category` `"purchased"` (the default).
2. **Locally Sourced & Fabricated Parts** — parts with `category` `"fabricated"`.
3. **Unrecognized Parts** — bodies that matched no custom part, listed with their model path (only relevant when the Fusion model changes; can usually be ignored).

Each parts section uses the following columns:

| **Position** | **Name**            | **Description**   | **Quantity** | **Length (mm)** | **Dimensions (mm)** |
| ------------ | ------------------- | ----------------- | ------------ | --------------- | ------------------- |
| 1            | X M5 Threaded Rod   | X-axis threaded rod | 5          | 300.0           |                     |
| 2            | Steel: X Frame Tubing | X-frame steel tubing | 2       | 500.0           | 500 x 50 x 50       |

With `INCLUDE_SUPPLIER_HINTS = True`, the parts sections add a trailing **Supplier Hint** column. The Unrecognized Parts section adds a trailing **Path** column showing where each unmatched body lives in the component tree.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to enhance the tool.

---

## Acknowledgments

Special thanks to the PrintNC community for inspiring this project.

---

## Contact

For questions or feedback, please reach out via GitHub Issues or contact me directly on discord under #sbrzl_3.14.
