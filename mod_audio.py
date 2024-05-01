import numpy as np
import pigpio
import time
import numpy as np
import scipy.io.wavfile as wav

def preprocess_audio(file_path):
    # Load the audio file
    rate, data = wav.read(file_path)
    if data.ndim > 1:  # Check if audio is stereo
        left_channel = data[:, 0]
        right_channel = data[:, 1]

    # Normalize and scale to PWM duty cycle
    max_pwm = 255
    left_duty = ((left_channel / np.max(np.abs(left_channel))) * (max_pwm / 2) + (max_pwm / 2)).astype(int)
    right_duty = ((right_channel / np.max(np.abs(right_channel))) * (max_pwm / 2) + (max_pwm / 2)).astype(int)

    # Save preprocessed data to file
    np.savez('preprocessed_duty_cycles.npz', left_duty=left_duty, right_duty=right_duty, sample_rate=rate)

# Call function with the path to your stereo audio file
preprocess_audio('path_to_your_stereo_audio.wav')


def play_pwm_signals(file_path):
    # Initialize pigpio
    pi = pigpio.pi()

    # GPIO pins for PWM
    left_pin = 18
    right_pin = 13

    # Load preprocessed data
    data = np.load(file_path)
    left_duty = data['left_duty']
    right_duty = data['right_duty']
    sample_rate = data['sample_rate']

    # PWM frequency
    frequency = 400  # Adjust as needed
    pi.set_PWM_frequency(left_pin, frequency)
    pi.set_PWM_frequency(right_pin, frequency)

    # Play PWM signals
    for left_value, right_value in zip(left_duty, right_duty):
        pi.set_PWM_dutycycle(left_pin, left_value)
        pi.set_PWM_dutycycle(right_pin, right_value)
        time.sleep(1 / sample_rate)  # Maintain timing

    # Cleanup
    pi.set_PWM_dutycycle(left_pin, 0)
    pi.set_PWM_dutycycle(right_pin, 0)
    pi.stop()

# Call function with the path to your preprocessed data
play_pwm_signals('preprocessed_duty_cycles.npz')


