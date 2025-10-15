# Standard library imports
import time

# External library imports
import bluerobotics_navigator as navigator
from bluerobotics_navigator import PwmChannel

# Useful constants for PWM modulation for thrusters
PWM_DUTY_CYCLE_LOW     = 0.0
PWM_DUTY_CYCLE_NEUTRAL = 0.5
PWM_DUTY_CYCLE_HIGH    = 1.0


def init_rov_thrusters(pwm_freq, channels, run_full_init_cycle = False):
    '''
    Initializes the ROV's ESCs for the thrusters. This involves setting specified thrusters to the
    neutral PWM value (1.5 ms) for some chunk of time to ensure they all properly initialize.

    NOTE: This is assuming the navigator module has been properly initialized with 'navigator.init()'

    Rules to follow prior to initialization:
    - Frequency cannot be higher than 909 Hz, otherwise low PWM does not fit into signal.       (min = 1.1 ms)
    - Frequency cannot be higher than 666 Hz, otherwise neutral PWM does not fit into signal.   (neutral = 1.5 ms)
    - Frequency cannot be higher than 526 Hz, otherwise max PWM does not fit into signal.       (max = 1.9 ms)

    Arguments:
    - `pwm_freq` - The PWM Frequency for the servo rail
    - `channels` - An array of PWM Channels (via the bluerobotics_navigator.PwmChannel type) that are assigned to ROV thrusters
    - `run_full_init_cycle` - If true, this will set the PWM values to LOW, then HIGH, then NEUTRAL. Otherwise just set to NEUTRAL

    Example Usage:
    ```python
    import bluerobotics_navigator as navigator
    from bluerobotics_navigator import PwmChannel

    print("Initializing navigator module...")
    navigator.init()

    print("Initializing ROV thrusters...")
    init_rov_thrusters(
        pwm_freq=200,
        channels=[
            PwmChannel.Ch1,
            PwmChannel.Ch2,
            PwmChannel.Ch3,
            PwmChannel.Ch4,
            PwmChannel.Ch5,
            PwmChannel.Ch6,
        ],
        run_full_init_cycle=False
    )

    print("Done!")
    ```

    Formulas:
    - duration (ms) = (1 / frequency) * 1000
    - pwm_value     = 4095 * (neutral_pwm / duration)
    '''

    if pwm_freq < 1 or pwm_freq > 526:
        raise Exception('Frequency has to be constrained between 1 Hz and 526 Hz')

    # Setup PWM frequency for all channels
    navigator.set_pwm_freq_hz(pwm_freq)

    # Enables or disables the PWM chip
    navigator.set_pwm_enable(True)

    # The number of seconds to delay for each step of the intialization process
    DELAY_EACH_STEP         = 4.0 # seconds (default: 8.0 sec)

    # Set PWM channels to neutral
    print('  Initializing ESCs: Setting PWM Channels to NEUTRAL...')
    navigator.set_pwm_channel_duty_cycle(channels, PWM_DUTY_CYCLE_NEUTRAL)
    time.sleep(DELAY_EACH_STEP)

    if run_full_init_cycle:
        # Set PWM channels to min range
        print('  Initializing ESCs: Setting PWM Channels to HIGH...')
        navigator.set_pwm_channel_duty_cycle(channels, PWM_DUTY_CYCLE_LOW)
        time.sleep(DELAY_EACH_STEP)

        # Set PWM channels to high range
        print('  Initializing ESCs: Setting PWM Channels to LOW...')
        navigator.set_pwm_channel_duty_cycle(channels, PWM_DUTY_CYCLE_HIGH)
        time.sleep(DELAY_EACH_STEP)

        # Set PWM channels to neutral
        print('  Initializing ESCs: Setting PWM Channels to NEUTRAL...')
        navigator.set_pwm_channels_duty_cycle(channels, PWM_DUTY_CYCLE_NEUTRAL)
        time.sleep(DELAY_EACH_STEP)


if __name__ == '__main__':
    print("Initializing navigator module...")
    navigator.init()

    print("Initializing ROV thrusters...")
    init_rov_thrusters(
        pwm_freq=200,
        channels=[
            PwmChannel.Ch1,
            # PwmChannel.Ch2,
            # PwmChannel.Ch3,
            # PwmChannel.Ch4,
            # PwmChannel.Ch5,
            # PwmChannel.Ch6,
        ],
        run_full_init_cycle=False
    )

    print("Done!")
