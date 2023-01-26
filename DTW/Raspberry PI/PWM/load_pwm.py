# send encoded audio input to PWM output

import pigpio # initialize pigpio
pi = gpio.pi()

pwm_pin = 13 # set the pwm output pin 12, 13, 19, 18 etc

pwm_freq = 44000 # ensure the PWM freq matches sample frequency

# start PWM on the pin
pi.set_mode(pwm_pin, pigpio.OUTPUT)
pi.hardware_PWM(pwm_pin, pwm_frequency, 0)

# send the encoded audio sample to the PWM output
pi.hardware_PWM(pwm_pin, pwm_frequency, int(encoded_sample))
