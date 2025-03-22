# CommsOnWheels Repository

A repository for vehicle communications tools and CAN bus analysis utilities, focusing on CAN bus monitoring and J1939 protocol implementations.
Team Members: Rohan Roy, Soumya Kataria, Bailey Kau, Jenil Makwana, Yilin Chen


## Repository Structure

### can-visualization
Our primary project - a Python application for real-time CAN bus data visualization and analysis.

- Complete implementation for monitoring J1939 protocol messages
- Support for both standard and direct PCAN interfaces
- Real-time signal monitoring with table and plot views
- DBC file parsing and signal visualization
- Simulation mode for testing without hardware

**Requirements:**
- Python 3.6+
- python-can ≥4.0.0
- cantools ≥37.0.0
- PyQt5 ≥5.15.0
- pyqtgraph ≥0.12.0

**Usage:**
```
python test_canvis.py --dbc path/to/file.dbc [--simulation] [--direct-pcan]
```

### CommsOnWheels
Legacy project from previous year, primarily R-based implementations.
- Contains sample DBC files for testing
- Reference material for CAN protocol handling

### UI
Basic PyQt shell implementation by team member.
- Simple graphical user interface foundations
- Starting point for the expanded GUI in the can-visualization tool

### cantools_testing
Development and learning files for cantools library.
- Early implementation tests and examples
- Test scripts for DBC file parsing
- Reference code for CAN message encoding/decoding

## Development Status

This project is under active development. The CAN visualization tool is functional but still being enhanced with additional features.

### Future Work

- Adding message filtering capabilities
- Improving signal visualization options
- Enhancing message sending interface
- Improving UI
- Integrating functionality for DBC modification