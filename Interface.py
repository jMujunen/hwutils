#!/usr/bin/env python3

# Interface.py - GUI interface for HWINFO

import sys
import os
import psutil

import PySimpleGUI as sg

from hwutilsDISK import Disk
from hwutils import NetworkInterface
from hwutils import GpuInfo
from hwutils import SystemTemp

import human_bytes

THEME = "Dark Green 5"
ALPHA = 0.5
GSIZE = (160, 160)
UPDATE_FREQUENCY_MILLISECONDS = 1 * 1000


def human_size(bytes, units=(" bytes", "KB", "MB", "GB", "TB", "PB", "EB")):
    """Returns a human readable string reprentation of bytes"""
    return str(bytes) + " " + units[0] if bytes < 1024 else human_size(bytes >> 10, units[1:])


def main_menu():
    sg.theme(THEME)

    ping_box = InterfaceBoxes("-PING_BOX-")
    cpu_temp_box = InterfaceBoxes("-CPU_TEMP_BOX-")
    cpu_clock_box = InterfaceBoxes("-CPU_CLOCK_BOX-")
    cpu_voltage_box = InterfaceBoxes("-CPU_VOLTAGE_BOX-")
    gpu_usage_box = InterfaceBoxes("-GPU_USAGE_BOX-")
    gpu_power_box = InterfaceBoxes("-GPU_POWER-")
    gpu_temp_box = InterfaceBoxes("-GPU_TEMP-")
    # ram_box InterfaceBoxes('-RAM_BOX-') enable_events=True)
    ram_box = InterfaceBoxes("-RAM_BOX-")
    layout = [
        [ping_box, cpu_temp_box, cpu_clock_box, cpu_voltage_box],
        [gpu_usage_box, gpu_power_box, gpu_temp_box, ram_box],
    ]

    window = sg.Window(
        "RAM Usage Widget Square",
        layout,
        location=(0, 0),
        no_titlebar=True,
        grab_anywhere=True,
        margins=(0, 0),
        element_padding=(0, 0),
        alpha_channel=ALPHA,
        finalize=True,
        right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT,
        enable_close_attempted_event=True,
        keep_on_top=True,
    )

    while True:  # Event Loop
        # ----------- update the graphics and text in the window ------------
        ram = psutil.virtual_memory()
        ram_element = ram_box.draw_rectangle(ram.percent)
        ram_text_percent = ram_box.draw_percentage_text(ram.percent)
        ram_text_used = ram_box.draw_text(f"{human_size(ram.used)} used")

        cpu = CpuData()
        cputemp_percent = round(cpu.average_temp / 90 * 100)
        cpu_temp_element = cpu_temp_box.draw_rectangle(cputemp_percent)
        cpu_temp_used = cpu_temp_box.draw_text(f"{(cpu.average_temp)}°C", font="Any 40", modifier=2)
        cpu_temp_footer = cpu_temp_box.draw_text("CPU")

        wifi = NetworkInterface(interface="wlan0")
        ping_element = ping_box.draw_rectangle(wifi.ping(destination="1.1.1.1"))
        ping_text = ping_box.draw_text(
            f'{(wifi.ping(destination="1.1.1.1"))}ms', font="Any 30", modifier=2
        )

        """
        cpuavgclock_percent = round(cpu.average_clock / 4750 * 100)
        cpu_avg_clock_element = cpu_clock_box.draw_rectangle(cpuavgclock_percent)
        cpu_text_avg_clock_percent = cpu_clock_box.draw_percentage_text(cpuavgclock_percent)
        cpu_text_avg_clock_used = cpu_clock_box.draw_text(f'{cpu.average_clock}MHz')
        """

        cpumaxclock_percent = round(cpu.max_clock / 5500 * 100)
        cpu_max_clock_element = cpu_clock_box.draw_rectangle(cpumaxclock_percent)
        cpu_text_max_clock_percent = cpu_clock_box.draw_percentage_text(cpumaxclock_percent)
        cpu_text_max_clock_used = cpu_clock_box.draw_text(f"{cpu.max_clock}MHz")

        cpuvoltage_percent = round(float(cpu.voltage) / 1.4 * 100)
        cpu_voltage_element = cpu_voltage_box.draw_rectangle(cpuvoltage_percent)
        cpu_text_voltage_percent = cpu_voltage_box.draw_percentage_text(cpuvoltage_percent)
        cpu_text_voltage_used = cpu_voltage_box.draw_text(f"{cpu.voltage}V")

        gpu = GpuInfo()
        gpu_useage_element = gpu_usage_box.draw_rectangle(gpu.core_usage)
        gpu_usage_text_percent = gpu_usage_box.draw_percentage_text(gpu.core_usage)
        gpu_text_used = gpu_usage_box.draw_text(f"{gpu.name}")

        gpupower_percent = round(gpu.power / 300 * 100)
        gpu_power_element = gpu_power_box.draw_rectangle(gpupower_percent)
        gpu_text_power_percent = gpu_power_box.draw_percentage_text(gpupower_percent)
        gpu_text_power_used = gpu_power_box.draw_text(f"{gpu.power}W")

        gpu_temp_element = gpu_temp_box.draw_rectangle(gpu.core_temp)
        gpu_text_temp_value = gpu_temp_box.draw_text(
            f"{gpu.core_temp}°C", font="Any 40", modifier=2
        )
        gpu_text_temp_used = gpu_temp_box.draw_text(f"{gpu.name}")

        """
        systemp = SystemTemp()
        systemp_percent = systemp.temp / 60 * 100
        sys_temp_element = sys_temp_box.draw_rectangle(systemp_percent)
        sys_temp_text_percent = sys_temp_box.draw_percentage_text(systemp_percent)
        sys_temp_value = sys_temp_box.draw_text(f'{systemp.temp}°C')
        """
        event, values = window.read(timeout=UPDATE_FREQUENCY_MILLISECONDS)
        if event in (sg.WIN_CLOSED, "Exit", sg.WIN_CLOSE_ATTEMPTED_EVENT):
            if event != sg.WIN_CLOSED:
                sg.user_settings_set_entry(
                    "-location-", window.current_location()
                )  # The line of code to save the position before exiting
            break
        if event == "Edit Me":
            sg.execute_editor(__file__)
        elif event == "Version":
            sg.popup_scrolled(
                __file__,
                sg.get_versions(),
                location=window.current_location(),
                keep_on_top=True,
                non_blocking=True,
            )

        ram_box.kill(kwarg1=ram_element, kwarg2=ram_text_percent, kwarg3=ram_text_used)
        ping_box.kill(kwarg1=ping_element, kwarg2=ping_text)
        cpu_temp_box.kill(kwarg1=cpu_temp_element, kwarg2=cpu_temp_used)
        # cpu_clock_box.kill(kwarg1=cpu_avg_clock_element, kwarg2=cpu_text_avg_clock_percent,
        #   kwarg3=cpu_text_avg_clock_used)
        cpu_clock_box.kill(
            kwarg1=cpu_max_clock_element,
            kwarg2=cpu_text_max_clock_percent,
            kwarg3=cpu_text_max_clock_used,
        )
        cpu_voltage_box.kill(
            kwarg1=cpu_voltage_element,
            kwarg2=cpu_text_voltage_percent,
            kwarg3=cpu_text_voltage_used,
        )
        gpu_usage_box.kill(kwarg1=gpu_useage_element, kwarg2=gpu_usage_text_percent)
        gpu_power_box.kill(
            kwarg1=gpu_power_element, kwarg2=gpu_text_power_percent, kwarg3=gpu_text_power_used
        )
        gpu_temp_box.kill(
            kwarg1=gpu_temp_element, kwarg2=gpu_text_temp_used, kwarg3=gpu_text_temp_value
        )

    window.close()


class InterfaceBoxes(sg.Graph):
    def __init__(self, key):
        super().__init__(GSIZE, (0, 0), GSIZE, key=key, enable_events=True)

    def draw_rectangle(self, value_as_percent):
        return super().draw_rectangle(
            (0, self.rectangle_height(value_as_percent)),
            (GSIZE[0], 0),
            fill_color=sg.theme_button_color()[1],
            line_width=0,
        )

    def draw_text(self, value, font="Any 20", modifier=4):
        return super().draw_text(
            value,
            (GSIZE[0] // 2, GSIZE[1] // modifier),
            font=font,
            text_location=sg.TEXT_LOCATION_CENTER,
            color=sg.theme_button_color()[0],
        )

    def draw_percentage_text(self, value):
        return super().draw_text(
            f"{value}%",
            (GSIZE[0] // 2, GSIZE[1] // 2),
            font="Any 40",
            text_location=sg.TEXT_LOCATION_CENTER,
            color=sg.theme_button_color()[0],
        )

    def rectangle_height(self, value):
        return int(GSIZE[1] * float(value) / 100)

    def kill(self, **kwargs):
        for arg, value in kwargs.items():
            self.delete_figure(value)


if __name__ == "__main__":
    main_menu()
