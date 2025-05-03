# CommsOnWheels Repository

A repository for vehicle communications tools and CAN bus analysis utilities, focusing on CAN bus monitoring and J1939 protocol implementations.
Team Members: Rohan Roy, Soumya Kataria, Bailey Kau, Jenil Makwana, Yilin Chen

## Repository Structure

### can-visualization

A Python application for visualizing Controller Area Network (CAN) data in real-time.

#### Overview

CAN Visualization is a tool for monitoring, analyzing, and visualizing CAN bus data from automotive and industrial systems. It supports:

- Loading and parsing DBC files for signal definitions
- Live data visualization through multiple display widgets
- Interactive dashboard with configurable widgets
- Real-time signal plotting and monitoring
- Simulation mode for testing without hardware
- Direct PCAN hardware interface support

![Dashboard Example](dashboard_example.png)

#### Features

- **Multiple Visualization Modes**:
  - Traditional signal table and plot view
  - Modern dashboard with customizable widgets
  - Configurable gauges, charts, and digital displays

- **CAN Interface Support**:
  - PCAN-USB adapters (PEAK-System)
  - Simulation mode with realistic signal trends
  - Direct PCAN interface compatible with existing tools

- **Signal Processing**:
  - DBC file parsing and message decoding
  - Signal trend generation and realistic simulation
  - Message filtering and sorting

- **User Experience**:
  - Qt-based graphical interface
  - Configurable dashboard widgets
  - Signal selection dialog with filtering
  - Profile saving/loading for dashboard configurations

#### Requirements

- Python 3.6+
- PyQt5
- python-can
- cantools
- pyqtgraph
- PyQtWebEngine (optional, for dashboard view)

Install dependencies with:

```bash
pip install -r requirements.txt
```

#### Getting Started

##### Running the Application with CSS-Electronics-SAE-J1939-DEMO.dbc:

```bash
# Basic mode with DBC file
python main_app.py --dbc=CSS-Electronics-SAE-J1939-DEMO.dbc

# Simulation mode (no hardware needed)
python main_app.py --dbc=CSS-Electronics-SAE-J1939-DEMO.dbc --simulation

# Dashboard mode
python main_app.py --dbc=CSS-Electronics-SAE-J1939-DEMO.dbc --dashboard

# Dashboard with Simulation (Recommended for Testing)
python main_app.py --dbc=CSS-Electronics-SAE-J1939-DEMO.dbc --dashboard --simulation

# With direct PCAN interface
python main_app.py --dbc=CSS-Electronics-SAE-J1939-DEMO.dbc --direct-pcan
```

##### Testing with Example Data

For testing without hardware, use the included test scripts:

```bash
# Test the regular dashboard
python test_dashboard.py

# Test the configurable dashboard
python test_configurable_dashboard.py
```

#### Architecture

The application follows a modular design:

- **CAN Interface Layer**:
  - `can_interface.py` - Standard interface for multiple channels
  - `direct_pcan_interface.py` - Direct hardware access compatible with existing tools

- **Data Processing**:
  - `dbc_parser.py` - Handles DBC file parsing
  - `message_processor.py` - Processes CAN messages and signals
  - `can_simulator.py` - Simulates realistic CAN traffic

- **Visualization**:
  - `signal_display.py` - Traditional table and plot views
  - `dashboard_view.py` - Modern dashboard UI
  - `configurable_dashboard_view.py` - Customizable dashboard

- **User Interface**:
  - `main_app.py` - Main application window
  - `signal_selection_dialog.py` - Dialog for selecting signals to monitor

#### DBC File Support

The application uses the cantools library to parse and process DBC files. It supports:

- J1939 protocol (extended IDs)
- Signal scaling and units
- Min/max values and ranges
- Signal descriptions and metadata

A sample J1939 DBC file is included for testing.

#### Configuration

##### Dashboard Configuration

The dashboard view can be configured with different widget types:

- **Gauge** - For RPM, temperature, and other analog values
- **Line Chart** - For trend visualization
- **Numeric Display** - For precise digital readings

Widget settings are saved in JSON format and can be loaded between sessions.

#### Usage Examples

##### Basic Signal Monitoring

1. Load a DBC file
2. Start the CAN interface
3. View signals in the table or plot tabs

##### Custom Dashboard Creation

1. Load a DBC file
2. Switch to dashboard mode 
3. Add widgets using the "Add Widget" button
4. Select signals from the dialog
5. Choose visualization type (gauge, chart, etc.)
6. Arrange and resize widgets as needed

#### Extending the Application

##### Adding New Widget Types

New widget types can be added to the dashboard by:

1. Adding the widget definition in the HTML/JavaScript code
2. Adding corresponding processing in the Python backend
3. Adding the widget option in the signal selection dialog

##### Supporting Additional Hardware

To add support for other CAN hardware:

1. Create a new interface class similar to `CANInterface` or `DirectPCANInterface`
2. Add the necessary hardware initialization and message handling
3. Integrate with the message processor

#### Troubleshooting

##### Common Issues

- **PCAN Hardware Not Found**: Ensure the PCAN-USB adapter is properly connected and PEAK drivers are installed
- **DBC File Loading Errors**: Check the DBC file format and compatibility
- **Dashboard Not Displaying**: Ensure PyQtWebEngine is installed

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