import can
import cantools

# Load the DBC file
db = cantools.database.load_file('Demo.dbc')

# Set up the CAN bus connection
bus = can.interface.Bus(channel='can0', bustype='socketcan')

# Receive a message
message = bus.recv()

# Decode the message using the DBC definitions
decoded_message = db.decode_message(message.arbitration_id, message.data)
print(decoded_message)

print('test')
