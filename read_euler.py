import serial
import json
from scipy.spatial.transform import Rotation as R

# Set up serial connection to /dev/ttyACM0
serial_port = '/dev/ttyACM0'  # Adjust if necessary
baud_rate = 115200  # Adjust based on your device's settings

# Open the serial connection
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# Function to convert quaternion to Euler angles (roll, pitch, yaw)
def quaternion_to_euler(quaternion):
    # Extract quaternion components
    w = quaternion['quat_w']
    x = quaternion['quat_x']
    y = quaternion['quat_y']
    z = quaternion['quat_z']
    
    # Create a Rotation object from the quaternion
    r = R.from_quat([x, y, z, w])
    
    # Convert to Euler angles (roll, pitch, yaw) in radians
    euler_angles = r.as_euler('xyz', degrees=True)
    
    return euler_angles

# Function to read data from the serial port
def read_from_serial():
    try:
        while True:
            # Read a line of data from the serial port
            line = ser.readline().decode('utf-8').strip()
            
            # If we have data, try to parse it as a JSON object
            if line:
                try:
                    quaternion = json.loads(line)
                    
                    # Convert the quaternion to Euler angles
                    euler_angles = quaternion_to_euler(quaternion)
                    
                    # Print the Euler angles
                    print(f"Roll: {euler_angles[0]:.3f}°, Pitch: {euler_angles[1]:.3f}°, Yaw: {euler_angles[2]:.3f}°")
                except json.JSONDecodeError:
                    print("Invalid data received, skipping line.")
    
    except KeyboardInterrupt:
        print("Terminating program.")
    finally:
        # Close the serial connection when done
        ser.close()

# Start reading and converting data from the serial port
if __name__ == "__main__":
    read_from_serial()

