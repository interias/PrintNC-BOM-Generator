# PrintNC BOM Generator

A Python-based tool to automate the creation of detailed Bills of Materials (BOM) for **PrintNC** builds. This tool organizes parts, calculates dimensions, and exports the BOM in CSV format for easy use and documentation.

---

## Features
- **Automated BOM Generation**: Automatically scans components and generates a detailed BOM.
- **Customizable Part Data**: Use a configurable dictionary to manage part names, descriptions, and display options.
- **Dimension and Length Calculation**: Calculates the largest dimension or detailed dimensions (XxYxZ) for parts based on configuration.
- **CSV Export**: Exports the BOM to a structured CSV file for further use.
- **BOM Sorted by CUSTOM_PARTS dict**: The BOM is sorted by the CUSTOM_PARTS dict.

---

## Installation

Either ollow the fusion 360 manual for creating a new script (https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-9701BBA7-EC0E-4016-A9C8-964AA4838954)

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

The tool uses a configurable `custom_parts` dictionary to define:
- **Part Name**: A readable name for the part (e.g., `"M5 Nut"`).
- **Description**: Additional information about the part.
- **Show Length**: Whether to display the largest dimension (`True` or `False`).
- **Show Dimensions**: Whether to display full dimensions in `XxYxZ` format (`True` or `False`).
- **Override Quantity**: If `False` the quantity will be aggregated, else if an integer value greater `0` is provided, the given value will be used for the quantity of this parts.

### Example `custom_parts` Entry
```python
custom_parts = {
    "m5 nut": {
        "name": "M5 Nut",
        "description": "Standard nut for M5 threads",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "xframe tubing": {
        "name": "XFrame Tubing",
        "description": "Tubing for the X-axis frame",
        "show_length": True,
        "show_dimensions": True,
        "override_quantity": False,
    },
    "1z hgr20 rail": {
        "name": "1Z HGR20 Rail",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": 2,
}
```

---

## Output
The exported CSV file includes the following columns:

| **Position** | **Name**             | **Description**                | **Quantity** | **Length (mm)** | **Dimensions (mm)** |
|--------------|----------------------|---------------------------------|--------------|-----------------|---------------------|
| 1            | M5 Threaded Rod      | Threaded rod with M5 thread    | 5            | 300.0           |                     |
| 2            | XFrame Tubing        | Tubing for the X-axis frame    | 2            | 500.0           | 500.0x50.0x50.0    |

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
