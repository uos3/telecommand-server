from django.db import models
from django.forms import ModelForm

# Create your models here.


class config(models.Model):

    choices_tx_interval_downlink = (
        (0, '0 ms'),
        (50, '500 ms'),
        (60, '600 ms'),
        (70, '700 ms'),
        (80, '800 ms'),
        (90, '900 ms'),
        (100, '1000 ms'),
        (150, '1500 ms'),
        (200, '2000 ms'),
    )
    choices_tx_datarate = (
        (0, '0.25 kbps'),
        (3, '0.5 kbps'),
        (6, '1 kbps'),
        (9, '3 kbps'),
        (12, '6 kbps'),
    )
    choices_tx_power = (
        (0, '10 mW'),
        (3, '50 mW'),
        (6, '100 mW'),
        (9, '200 mW'),
        (12, '300 mW'),
    )
    choices_image_acquisition_profile = (
        (0, '1600x1200'),
        (1, '640x480'),
    )
    choices_operational_mode = (
        (0, 'Deployment Phases'),
        (1, 'Nominal Operations'),
        (3, 'Safe Mode'),
    )
    choices_bool = (
        (0, 'Off'),
        (1, 'On'),
    )

    date_submitted = models.DateTimeField(auto_now_add=True)
    user_submitted = models.CharField(max_length=64)

    tx_enable = models.BooleanField(default=True)
    tx_interval = models.PositiveSmallIntegerField()
    tx_interval_downlink = models.IntegerField(choices=choices_tx_interval_downlink)
    tx_datarate = models.IntegerField(choices=choices_tx_datarate)
    tx_power = models.IntegerField(choices=choices_tx_power)
    tx_overtemp = models.PositiveSmallIntegerField()
    rx_overtemp = models.PositiveSmallIntegerField()
    batt_overtemp = models.PositiveSmallIntegerField()
    obc_overtemp = models.PositiveSmallIntegerField()
    pa_overtemp = models.PositiveSmallIntegerField()
    low_voltage_threshold = models.PositiveSmallIntegerField()
    low_voltage_recovery = models.PositiveSmallIntegerField()
    health_acquisition_interval = models.PositiveIntegerField()
    configuration_acquisition_interval = models.PositiveIntegerField()
    imu_acquisition_interval = models.PositiveIntegerField()
    imu_sample_count = models.PositiveSmallIntegerField()
    imu_sample_interval = models.PositiveSmallIntegerField()
    gps_acquisition_interval = models.PositiveIntegerField()
    gps_sample_count = models.PositiveSmallIntegerField()
    gps_sample_interval = models.PositiveSmallIntegerField()
    image_acquisition_time = models.BigIntegerField()
    image_acquisition_profile = models.BooleanField(choices=choices_image_acquisition_profile)
    time = models.BigIntegerField()
    operational_mode = models.IntegerField(choices=choices_operational_mode)
    self_test = models.BooleanField(choices=choices_bool, default=False)
    power_rail_1 = models.BooleanField(choices=choices_bool, default=True)
    power_rail_3 = models.BooleanField(choices=choices_bool, default=True)
    power_rail_5 = models.BooleanField(choices=choices_bool, default=True)
    power_rail_6 = models.BooleanField(choices=choices_bool, default=True)
    reset_power_rail_1 = models.BooleanField(choices=choices_bool, default=False)
    reset_power_rail_2 = models.BooleanField(choices=choices_bool, default=False)
    reset_power_rail_3 = models.BooleanField(choices=choices_bool, default=False)
    reset_power_rail_4 = models.BooleanField(choices=choices_bool, default=False)
    reset_power_rail_5 = models.BooleanField(choices=choices_bool, default=False)
    reset_power_rail_6 = models.BooleanField(choices=choices_bool, default=False)
    imu_accel_enabled = models.BooleanField(choices=choices_bool, default=False)
    imu_gyro_enabled = models.BooleanField(choices=choices_bool, default=False)
    imu_magno_enabled = models.BooleanField(choices=choices_bool, default=False)
    downlink_stop_time = models.BigIntegerField()


class configForm(ModelForm):
    class Meta:
        model = config
        exclude = [
            'date_submitted',
        ]
