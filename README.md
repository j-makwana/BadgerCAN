Project CANnonball: Real-Time Vehicle Data Configuration and Visualization
Team Name: BadgerCAN
Team Members: Soumya Kataria, Rohan Roy, Yilin Chen, Jenil Makwana, Bailey Kau
Mentors: Chris Sebastian, Justin Neils, Brent Voakes, Hector Baez, Colin Brown, Jacob Shelley

Project Description:
Project CANnonball will be an intuitive application designed to decode and display critical data from heavy-duty vehicles. With a dynamic, user-friendly interface built using PQt, you’ll easily interpret and manage complex CAN data to keepyour vehicle running smoothly.

Part 1: Crafting a Modular and User-Friendly UI
Part 2: Decoding Vehicular Data and Integrating with CAN Hardware



Content from the Mentors and other Research/References:

Resources from Slack from Hector - 2/27
https://www.linkedin.com/pulse/advanced-dbc-file-format-concepts-saravana-pandian-annamalai-hhzhc#:~:text=Multiplexed%20message%20in%20DBC%20file&text=A%20multiplexed%20message%20is%20a,are%20transmitted%20within%20the%20message 

Slack - Justin Neils - 2/27

Networks & Messages:
What is the relationship between "Networks," "Nodes," "Messages," and "Signals"?
Networks are the backbone of communication, i.e. the CAN bus.
Nodes are the communication source that send/receive messages on the CAN bus, i.e. controllers.
Messages are the communications that are sent/receive, they encapsulate the meta data, i.e. signals.
Signals are the specific meta data being communicated, i.e. sensor readings, function commands, etc.
How does a message (e.g., "Message B") interact with its signals?
The message encapsulates the metadata, it is just a container for it.
What does the "ID" field in the message definition represent, and how is it used?
The ID field is how you can determine/identify one packet of data (message A) from another (message B), it is what tells you who is talking and what they are saying on the CAN bus.
Transmitters & Transmission Method:
What does "Transmitters" refer to in this context? Does it mean the device sending the CAN message?
Transmitter is the module/source of a message being communicated on the CAN bus. Yes, the message sender.
What is the difference between transmission methods (e.g., "cyclic")?
Messages can be repeatedly sent at a pace (cyclic). Or they can be sent in response to requests for information (on-demand). They can also be event based.
How is the "Cycle Time" value determined, and how does it affect data transmission?
This can be determined by industry standards, controller requirements, application specifics, etc. This affects the rate at which the message is communicated on the CAN bus. 50 ms cycle time means the message is communicated every 50 ms.
Device Table (Bottom Section):
What does each column represent? (e.g., "Serial C", "Baud", "Bus Lo")
I'm guessing the text got cut off in the wireframes. Baud is the network speed of the CAN bus, and Bus Loading. Serial indicates the serial number of the USB/CAN adapter.  This can be used to help distinguish between CAN/USB adapters if there are multiple ones connected to the PC.
What does "Bus Lo" indicate? Is it related to network load?
Bus Loading is a percentage representative of the amount of the traffic on the bus that it can handle.
What happens if a device is "unassigned"? Does it still receive/send data?
I don't recall exactly in the picture what this referenced. If it is about a bus, no. A device has to be assigned to a bus in order to send/receive data. If it is about a source address, yes.
General Usability & Improvements:
Are there any pain points users currently experience with this interface?
One of the biggest pain points on our existing software is not being able to see nested multiplexed messages in the send and receive windows.
Do users need more customization options for data display or filtering?
Being able to display signal values both as raw CAN and/or converted based on the DBC would be a nice customization. 

Email - Jacob Shelley - CAN Architecture - 2/20

Let’s look at this section:

Line 84 lists the DBC ID.  If you enter it into a calculator, you’ll find that it’s 32 bits.  The DBC ID isn’t very meaningful because It’s only found in the DBC, and what’s broadcast over the CAN bus is something called a CAN ID.  This CAN ID is either 11 or 29 bits, so your app will have to convert the DBC IDs to CAN IDs.  I’ve heard both of these IDs referred to as “Message IDs” which can be confusing.
If the 32nd bit of the DBC ID is a “1” then it contains an extended CAN ID which is 29-bits.  Otherwise, it’s a standard 11-bit ID.  To convert it to a 29-bit CAN ID, simply mask the DBC ID with 0x7FFFFFF.  To convert it to an 11-bit ID, mask it with 0x7FF.
The extended identifiers are broken down with more information that you might find meaningful at some point in the project.  See here, CAN ID Explanation | Tractor Hacking.  It contains a priority, source controller address, data page (DP), extended data page (EDP), and protocol data unit (PDU).   A DBC ID of 2560098046 (0x9897FEFE) has a CAN ID of 0x1897FEFE, which, based on the bitfield decomposition shown in the link above, has a priority of 6 and a source address of 254.  (A lower priority is faster, but you shouldn’t have to worry about that for your project.)
Back to line 84 in the DBC---the NCS is the source controller name, aka source node.  The source node (NCS) on that line should line up with the source address from the CAN ID---254 in the example above.
The “8” on line 84 of the DBC indicates how many bytes the data section is.  In this case, there are 8 bytes worth of signals. 
Lines 85 and 86 show the signals.  Here is a figure for understanding how the signals are broken down into meaningful information.  Note that the bit start is zero-indexed, meaning a start bit of “0” rather than “1” is the first bit in the data bytes.

When we receive or record data from the bus, it’s looks something like this:
0xCF004FE   FF FF FF 68 13 FF FF FF
   	     ^^least sig byte     ^^most significant byte
 
For this example, your application has to search the DBC for an ID that matches 0xCF004FE.  It’ll find that it corresponds to the EEC1 message.  And then it has to go through all of the signals in the DBC and assign values to those signals based on the raw data bytes.   So for the EngineSpeed signal, it uses the bits from 24 through 39 (this comes from the start and length bits shown in the figure above).  Bits 24-39 in data bytes FF FF FF 68 13 FF FF FF are just 0x1368.  Notice it’s not 0x6813, because the least significant byte in the data is on the left.  The value 0x1368 in decimal is 4968, which has a scaling of 0.125 (noted in the figure above).  This brings the EngineSpeed value to 4968 * 0.125 =  621 rpm.
