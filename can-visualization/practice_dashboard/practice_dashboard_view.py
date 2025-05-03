import os
import random
import json
import logging
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QUrl, QTimer

# Use the compatibility wrapper instead of direct imports
from webengine_wrapper import QWebEngineView, QWebEngineSettings, HAS_WEBENGINE

class DashboardView(QWidget):
    """Modern dashboard view using web technologies for visualization"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger("DashboardView")
        self.message_processor = None
        self.dbc_parser = None
        self.logger.info("Initializing dashboard view")
        
        # Store messages temporarily
        self.recent_messages = {}
        
        # Initialize UI
        self.init_ui()
        
        # Start update timer - instead of using QWebChannel, we'll use periodic updates
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_dashboard)
        self.update_timer.start(200)  # Update 5 times per second
        
    def init_ui(self):
        """Initialize the user interface"""
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        if not HAS_WEBENGINE:
            # If web engine is not available, show a message
            layout.addWidget(QLabel("PyQtWebEngine is not available. Please install it with: pip install PyQtWebEngine"))
            self.logger.warning("PyQtWebEngine not available - dashboard functionality limited")
            return
        
        # Create web view
        self.web_view = QWebEngineView()
        
        # Create dashboard HTML file
        html_path = self.create_dashboard_html()
        if html_path:
            self.logger.info(f"Loading dashboard HTML from: {html_path}")
            self.web_view.load(QUrl.fromLocalFile(html_path))
        else:
            # Fallback message
            layout.addWidget(QLabel("Failed to create dashboard. Check logs for details."))
            self.logger.error("Failed to create dashboard HTML file")
            
        layout.addWidget(self.web_view)
    
    def create_dashboard_html(self):
        """Create the dashboard HTML file"""
        try:
            html_content = self.get_dashboard_html()
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard.html")
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_content)
                
            return file_path
        except Exception as e:
            self.logger.error(f"Error creating dashboard HTML: {e}")
            return None
    
    def get_dashboard_html(self):
        """Get the HTML content for the dashboard"""
        # We'll use a simpler approach without QWebChannel
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CAN Dashboard</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.7.0/chart.min.js"></script>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            height: 100%;
            background-color: #f0f2f5;
        }

        #app {
            height: 100%;
            display: flex;
            flex-direction: column;
        }

        .header {
            background-color: #1e3a8a;
            color: white;
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .content {
            flex: 1;
            padding: 20px;
            overflow: auto;
        }

        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }

        .card {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            padding: 15px;
            position: relative;
            overflow: hidden;
        }

        .card-title {
            font-size: 14px;
            color: #666;
            margin-bottom: 5px;
        }

        .card-value {
            font-size: 28px;
            font-weight: bold;
        }

        .card-unit {
            font-size: 14px;
            color: #999;
            margin-left: 5px;
        }

        .chart-container {
            height: 80px;
            margin-top: 10px;
            position: relative;
        }

        .gauge-container {
            height: 150px;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .gauge {
            width: 120px;
            height: 120px;
            position: relative;
        }

        .gauge-background {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background: #e0e0e0;
            position: absolute;
            clip-path: polygon(50% 0%, 100% 0%, 100% 100%, 50% 100%);
            transform: rotate(0deg);
        }

        .gauge-progress {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background: linear-gradient(to right, #4CAF50, #FFEB3B, #FF5722);
            position: absolute;
            clip-path: polygon(50% 0%, 100% 0%, 100% 100%, 50% 100%);
            transform-origin: center left;
        }

        .gauge-center {
            position: absolute;
            width: 80%;
            height: 80%;
            background: white;
            border-radius: 50%;
            top: 10%;
            left: 10%;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }

        .gauge-value {
            font-size: 24px;
            font-weight: bold;
        }

        .gauge-label {
            font-size: 12px;
            color: #666;
        }

        #content-charts {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .chart-card {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            padding: 15px;
            height: 300px;
        }

        .positive-change {
            color: #4CAF50;
        }

        .negative-change {
            color: #F44336;
        }

        /* Speedometer Styles */
        .speedometer-container {
            position: relative;
            width: 150px;
            height: 80px; /* Reduced height to fit better */
            margin: 10px auto; /* Center the speedometer */
        }

        .speedometer-scale {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border-radius: 50% 50% 0 0 / 100% 100% 0 0;
            background-color: #f0f0f0;
            overflow: hidden;
        }

        .speedometer-ticks {
            position: absolute;
            left: 50%;
            bottom: 10px;
            width: 80%;
            height: 1px;
            background-color: #333;
            transform-origin: 0% 0%;
        }

        .speedometer-ticks::before {
            content: '';
            position: absolute;
            left: 0;
            bottom: -5px;
            width: 1px;
            height: 5px;
            background-color: #333;
        }

        .speedometer-needle {
            position: absolute;
            bottom: 15px;
            left: 50%;
            width: 5px;
            height: 40%;
            background-color: red;
            transform-origin: 50% 100%;
            border-radius: 3px 3px 0 0;
        }

        .speedometer-value {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 16px;
            font-weight: bold;
            color: #333;
        }
    </style>
</head>
<body>
    <div id="app">
        <div class="header">
            <h2>CAN Visualization Dashboard</h2>
            <div id="status"></div>
        </div>

        <div class="content">
            <div class="dashboard">
                <div class="card">
                    <div class="card-title">Speed</div>
                    <div class="card-value" id="speed-value">0</div>
                    <div class="card-unit">km/h</div>
                    <div class="speedometer-container">
                        <div class="speedometer-scale">
                            <div class="speedometer-ticks" style="transform: rotate(-90deg);"></div>
                            <div class="speedometer-ticks" style="transform: rotate(-60deg);"></div>
                            <div class="speedometer-ticks" style="transform: rotate(-30deg);"></div>
                            <div class="speedometer-ticks" style="transform: rotate(0deg);"></div>
                            <div class="speedometer-ticks" style="transform: rotate(30deg);"></div>
                            <div class="speedometer-ticks" style="transform: rotate(60deg);"></div>
                            <div class="speedometer-ticks" style="transform: rotate(90deg);"></div>
                            <div class="speedometer-needle" id="speedometer-needle" style="transform: rotate(-90deg);"></div>
                            <div class="speedometer-value" id="speedometer-current-value">0</div>
                        </div>
                    </div>
                    <div class="chart-container">
                        <canvas id="speed-chart"></canvas>
                    </div>
                    <div class="card-change positive-change" id="speed-change">↑ 3.5%</div>
                </div>

                <div class="card">
                    <div class="card-title">Engine Speed</div>
                    <div class="card-value" id="engine-speed-value">0</div>
                    <div class="card-unit">rpm</div>
                    <div class="chart-container">
                        <canvas id="engine-speed-chart"></canvas>
                    </div>
                    <div class="card-change positive-change" id="engine-speed-change">↑ 8.7%</div>
                </div>

                <div class="card">
                    <div class="card-title">Fuel Rate</div>
                    <div class="card-value" id="fuel-rate-value">27.0</div>
                    <div class="card-unit">l/h</div>
                    <div class="chart-container">
                        <canvas id="fuel-rate-chart"></canvas>
                    </div>
                    <div class="card-change negative-change" id="fuel-rate-change">↓ 8.7%</div>
                </div>

                <div class="card">
                    <div class="card-title">Fuel Economy</div>
                    <div class="card-value" id="fuel-economy-value">2.5</div>
                    <div class="card-unit">km/l</div>
                    <div class="chart-container">
                        <canvas id="fuel-economy-chart"></canvas>
                    </div>
                    <div class="card-change positive-change" id="fuel-economy-change">↑ 9.8%</div>
                </div>

                <div class="card">
                    <div class="card-title">Power Level</div>
                    <div class="card-value" id="power-level-value">130</div>
                    <div class="card-unit">kW</div>
                    <div class="chart-container">
                        <canvas id="power-level-chart"></canvas>
                    </div>
                    <div class="card-change positive-change" id="power-level-change">↑ 10.5%</div>
                </div>

                <div class="card">
                    <div class="card-title">Fuel Level</div>
                    <div class="card-value" id="fuel-level-value">51</div>
                    <div class="card-unit">%</div>
                    <div class="chart-container">
                        <div style="width: 100%; height: 100%; background: #f5f5f5; position: relative; border-radius: 4px; overflow: hidden;">
                            <div id="fuel-level-bar" style="height: 100%; width: 51%; background: linear-gradient(to top, #FFC107, #FFEB3B); position: absolute; bottom: 0; transition: width 0.5s ease;"></div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="card">
                <div class="card-title">Dial Temperatures (degC)</div>
                <div style="display: flex; justify-content: space-around;">
                    <div class="gauge-container">
                        <div class="gauge">
                            <div class="gauge-background"></div>
                            <div class="gauge-progress" id="oil-temp-gauge" style="transform: rotate(0deg); background: #FFC107;"></div>
                            <div class="gauge-center">
                                <div class="gauge-value" id="oil-temp-value">101</div>
                                <div class="gauge-label">oil</div>
                            </div>
                        </div>
                    </div>

                    <div class="gauge-container">
                        <div class="gauge">
                            <div class="gauge-background"></div>
                            <div class="gauge-progress" id="fuel-temp-gauge" style="transform: rotate(0deg); background: #2196F3;"></div>
                            <div class="gauge-center">
                                <div class="gauge-value" id="fuel-temp-value">36</div>
                                <div class="gauge-label">fuel</div>
                            </div>
                        </div>
                    </div>

                    <div class="gauge-container">
                        <div class="gauge">
                            <div class="gauge-background"></div>
                            <div class="gauge-progress" id="coolant-temp-gauge" style="transform: rotate(0deg); background: #4CAF50;"></div>
                            <div class="gauge-center">
                                <div class="gauge-value" id="coolant-temp-value">90</div>
                                <div class="gauge-label">coolant</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div id="content-charts">
                <div class="chart-card">
                    <div class="card-title">Speed (km/h)</div>
                    <canvas id="speed-history-chart"></canvas>
                </div>

                <div class="chart-card">
                    <div class="card-title">EngineSpeed (rpm)</div>
                    <canvas id="engine-speed-history-chart"></canvas>
                </div>

                <div class="chart-card">
                    <div class="card-title">Message: CAN1_AMB_500</div>
                    <canvas id="can-message-chart"></canvas>
                </div>

                <div class="chart-card">
                    <div class="card-title">Warning Lamps</div>
                    <canvas id="warning-lamps-chart"></canvas>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Data storage
        const dataHistory = {
            speed: {
                values: Array(60).fill(0),
                chart: null
            },
            engineSpeed: {
                values: Array(60).fill(0),
                chart: null
            },
            fuelRate: {
                values: Array(60).fill(0),
                chart: null
            },
            fuelEconomy: {
                values: Array(60).fill(0),
                chart: null
            },
            powerLevel: {
                values: Array(60).fill(0),
                chart: null
            },
            temperatures: {
                oil: 101,
                coolant: 90,
                fuel: 36
            },
            canMessage: {
                labels: Array(60).fill(''),
                cylinderTemp: Array(60).fill(0).map(() => Math.floor(35 + Math.random() * 15)),
                sensorPressure: Array(60).fill(0).map(() => Math.floor(90 + Math.random() * 10)),
                chart: null
            },
            warningLamps: {
                labels: Array(60).fill(''),
                compressor: Array(60).fill(0),
                engineWarning: Array(60).fill(0),
                brakeActive: Array(60).fill(0),
                chart: null
            },
            fuelLevel: 51
        };

        // Initialize starting values
        document.getElementById('speed-value').textContent = '50';
        document.getElementById('engine-speed-value').textContent = '1800';

        // Function to update the speedometer
        function updateSpeedometer(value) {
            const needle = document.getElementById('speedometer-needle');
            const valueDisplay = document.getElementById('speedometer-current-value');
            const minSpeed = 0;
            const maxSpeed = 120; // Assuming a max speed for the speedometer
            const angle = -90 + (value - minSpeed) / (maxSpeed - minSpeed) * 180; // Map speed to angle

            needle.style.transform = `rotate(${angle}deg)`;
            valueDisplay.textContent = Math.round(value);
        }

        // Polling for updates - no need for web channel
        function pollForUpdates() {
            fetch('dashboard-data.json')
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        // If file not found, continue with simulation
                        simulateUpdates();
                        return null;
                    }
                })
                .then(data => {
                    if (data) {
                        processUpdates(data);
                    }
                })
                .catch(error => {
                    // On error, continue with simulation
                    console.log('Using simulation mode:', error);
                    simulateUpdates();
                });"""
    
    def init_web_channel(self, message_processor, dbc_parser):
        """Initialize with the message processor"""
        self.message_processor = message_processor
        self.dbc_parser = dbc_parser
        
        # Connect signals to update dashboard
        if message_processor:
            message_processor.message_decoded.connect(self.on_message_decoded)
    
    def on_message_decoded(self, frame_id, message_name, signals, interface):
        """Handle a decoded CAN message"""
        # Store the message for the next update cycle
        self.recent_messages[message_name] = signals
        self.logger.debug(f"Stored message for dashboard: {message_name}")
    
    def update_dashboard(self):
        """Update the dashboard with recent messages"""
        if not self.recent_messages:
            return
            
        try:
            # Write messages to a JSON file that the web view can read
            data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard-data.json")
            with open(data_path, "w", encoding="utf-8") as f:
                json.dump(self.recent_messages, f)
                
            # Clear recent messages
            self.recent_messages = {}
            
        except Exception as e:
            self.logger.error(f"Error updating dashboard: {e}")