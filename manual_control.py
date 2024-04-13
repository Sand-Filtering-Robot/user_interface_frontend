from flask import Flask, request, jsonify
from motor import MotorDriver, MotorPins

app = Flask(__name__, static_url_path="")

# Define motor pins
motor_pins_list = [
    MotorPins(pwm=12, inA=20, inB=21),  # motor 0 pins
    MotorPins(pwm=13, inA=5, inB=6),    # motor 1 pins
    MotorPins(pwm=18, inA=23, inB=24),  # motor 2 pins
    MotorPins(pwm=19, inA=2, inB=3)     # motor 3 pins
]

# Initialize the motor driver
driver = MotorDriver(motorPins=motor_pins_list)

# Global variable to keep track of control mode
control_mode = 'autonomous'

# Define a route to listen for POST requests for motor control
@app.route('/set-mode', methods=['POST'])
def set_mode():
    global control_mode
    requested_mode = request.get_json().get('mode', None)
    if requested_mode in ['autonomous', 'manual']:
        control_mode = requested_mode
        if requested_mode == 'manual':
            driver.stop()  # Stop all motions when switching to remote control
        return jsonify({'status': 'Mode set to ' + requested_mode}), 200
    return jsonify({'error': 'Invalid mode requested'}), 400

@app.route('/motor-control', methods=['POST'])
def motor_control():
    if control_mode != 'manual':
        return jsonify({'error': 'Robot is not in remote control mode'}), 403

    data = request.get_json()
    direction = data.get('direction')
    speed = data.get('speed', 0.2)  # Default speed
    
    # Call the appropriate MotorDriver method based on the direction
    if direction == 'up':
        driver.forward(speed)
        print(driver)
    elif direction == 'down':
        driver.backward(speed)
        print(driver)
    elif direction == 'left':
        driver.left(speed)
        print(driver)
    elif direction == 'right':
        driver.right(speed)
        print(driver)
    else:
        return jsonify({'error': 'Invalid direction'}), 400

    return jsonify({'status': 'Motor command executed'}), 200

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)