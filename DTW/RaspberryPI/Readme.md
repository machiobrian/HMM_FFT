
## Raspberry PI ADC.


> The first step would be to **get the ADC samples out of raspberry pi**

> When successful, we shall `visualize` them, I am working on that and I will share it once completed.

> I will constanctly be updating the `requirements.txt`

* Ensure the sampling frequency while streaming input, matches PMW frequency - in this case its 44 KHz.
* Encoded audio must be in integer form.

Order of use is as follows:
1. `Get` ADC output from the raspberry pi `(file: get_audio_rasp.py)`

2. `Load` the extracted values from step(1) into PWM pins of the raspberry pi (`file: load_pwm.py)` 

3. `Save` the loaded audio values from step(2) into a csv file `(file: save_as_csv.py)`

> **Note: It may be necessary the you `merge` the files or `import` file 1 into file 2 - for loading ADC values into PWM and later import files 1&2 into file 3 for saving into csv**