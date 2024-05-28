#!/usr/bin/env python3

# main.py - Main entry point for HWINFO

import time
import configparser
import os

from hwdata.GPU import GpuData
from hwdata.CPU import CpuData
from hwdata.FAN import Fan
from hwdata.SYS import SystemTemp


def main(POLL_INTERVAL=1, MAX_SAMPLES=60):
    for i in range(MAX_SAMPLES):
        print(GpuData(), end='\n\n')
        time.sleep(POLL_INTERVAL)

def create_config():
    config = configparser.ConfigParser()
 
    # Add sections and key-value pairs
    config['View'] = {
        'TITLE': True,
        'TITLE_TEXT': 'HWINFO',
        'TITLE_COLOR': 'white',
        'TITLE_SIZE': '30',
        'TITLE_POSITION': 'top',
        'TITLE_ALIGN': 'center',
        'GRID': False,
        'GRID_COLOR': 'white',
        'LEGEND': True,
        'LEGEND_POSITION': 'default',
        'LEGEND_SHOW_VALUES': False,
        'BACKGROUND': 'black',
    }
    config['Function'] = {
        'POLL_INTERVAl': 500, 
        'LOGGING': False,
        'LOG_FILE': 'hwinfo.log'
        }

    config['CPU'] = {
        'LINE_WIDTH': 1,
        'LINE_COLOR': 'turquoise',
        'LINE_STYLE': 'solid',
        'LABEL': 'CPU',
        'LABEL_COLOR': 'magenta',
        'LABEL_SIZE': '10',
        'VISIBLE': True
    }

    config['GPU'] = {
        'LINE_WIDTH': 1,
        'LINE_COLOR': 'magenta',
        'LINE_STYLE': 'solid',
        'LABEL': 'CPU',
        'LABEL_COLOR': 'magenta',
        'LABEL_SIZE': '10',
        'VISIBLE': True
    }

    config['SYS'] = {
        'LINE_WIDTH': 1,
        'LINE_COLOR': 'orange',
        'LINE_STYLE': 'solid',
        'LABEL': 'CPU',
        'LABEL_COLOR': 'magenta',
        'LABEL_SIZE': '10',
        'VISIBLE': True
    }

    config['BOTTOM_FAN'] = {
        'LINE_WIDTH': 1,
        'LINE_COLOR': 'green',
        'LINE_STYLE': 'solid',
        'LABEL': 'CPU',
        'LABEL_COLOR': 'magenta',
        'LABEL_SIZE': '10',
        'VISIBLE': True
    }
    config['REAR_FAN'] = {
        'LINE_WIDTH': 1,
        'LINE_COLOR': 'red',
        'LINE_STYLE': 'solid',
        'LABEL': 'CPU',
        'LABEL_COLOR': 'magenta',
        'LABEL_SIZE': '10',
        'VISIBLE': True
    }
 
    # Write the configuration to a file
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    read_config()

def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Booleans
    show_title = config.getboolean('View', 'TITLE')
    show_grid = config.getboolean('View', 'GRID')
    show_legend = config.getboolean('View', 'LEGEND')
    show_legend_values = config.getboolean('View', 'LEGEND_SHOW_VALUES')

    title_text = config.get('View', 'TITLE_TEXT')
    title_color = config.get('View', 'TITLE_COLOR')
    title_size = config.get('View', 'TITLE_SIZE')
    title_position = config.get('View', 'TITLE_POSITION')
    title_align = config.get('View', 'TITLE_ALIGN')

    grid_color = config.get('View', 'GRID_COLOR')
    graph_color = config.get('View', 'BACKGROUND')
    legend_position = config.get('View', 'LEGEND_POSITION')

    ###########################################################

    # App funtion
    poll_interval = config.getint('Function', 'POLL_INTERVAL')
    logging = config.getboolean('Function', 'LOGGING')
    log_file = config.get('Function', 'LOG_FILE')

    ###########################################################

    # Hardware settings

    # CPU
    cpu_line_width = config.getint('CPU', 'LINE_WIDTH')
    cpu_line_color = config.get('CPU', 'LINE_COLOR')
    cpu_line_style = config.get('CPU', 'LINE_STYLE')
    cpu_label = config.get('CPU', 'LABEL')
    cpu_label_color = config.get('CPU', 'LABEL_COLOR')
    cpu_label_size = config.get('CPU', 'LABEL_SIZE')
    cpu_visible = config.getboolean('CPU', 'VISIBLE')

    # GPU
    gpu_line_width = config.getint('GPU', 'LINE_WIDTH')
    gpu_line_color = config.get('GPU', 'LINE_COLOR')
    gpu_line_style = config.get('GPU', 'LINE_STYLE')
    gpu_label = config.get('GPU', 'LABEL')
    gpu_label_color = config.get('GPU', 'LABEL_COLOR')
    gpu_label_size = config.get('GPU', 'LABEL_SIZE')
    gpu_visible = config.getboolean('GPU', 'VISIBLE')

    # SYS
    sys_line_width = config.getint('SYS', 'LINE_WIDTH')
    sys_line_color = config.get('SYS', 'LINE_COLOR')
    sys_line_style = config.get('SYS', 'LINE_STYLE')
    sys_label = config.get('SYS', 'LABEL')
    sys_label_color = config.get('SYS', 'LABEL_COLOR')
    sys_label_size = config.get('SYS', 'LABEL_SIZE')
    sys_visible = config.getboolean('SYS', 'VISIBLE')

    # Bottom Fan
    bottom_line_width = config.getint('BOTTOM_FAN', 'LINE_WIDTH')
    bottom_line_color = config.get('BOTTOM_FAN', 'LINE_COLOR')
    bottom_line_style = config.get('BOTTOM_FAN', 'LINE_STYLE')
    bottom_label = config.get('BOTTOM_FAN', 'LABEL')
    bottom_label_color = config.get('BOTTOM_FAN', 'LABEL_COLOR')
    bottom_label_size = config.get('BOTTOM_FAN', 'LABEL_SIZE')
    bottom_visible = config.getboolean('BOTTOM_FAN', 'VISIBLE')

    # Rear Fan
    rear_line_width = config.getint('REAR_FAN', 'LINE_WIDTH')
    rear_line_color = config.get('REAR_FAN', 'LINE_COLOR')
    rear_line_style = config.get('REAR_FAN', 'LINE_STYLE')
    rear_label = config.get('REAR_FAN', 'LABEL')
    rear_label_color = config.get('REAR_FAN', 'LABEL_COLOR')
    rear_label_size = config.get('REAR_FAN', 'LABEL_SIZE')
    rear_visible = config.getboolean('REAR_FAN', 'VISIBLE')

    config_values = {
        'show_title': show_title,
        'show_grid': show_grid,
        'show_legend': show_legend,
        'show_legend_values': show_legend_values,
        'title_text': title_text,
        'title_color': title_color,
        'title_size': title_size,
        'title_position': title_position,
        'title_align': title_align,
        'grid_color': grid_color,
        'graph_color': graph_color,
        'legend_position': legend_position,
        'poll_interval': poll_interval,
        'logging': logging,
        'log_file': log_file,
        'cpu_line_width': cpu_line_width,
        'cpu_line_color': cpu_line_color,
        'cpu_line_style': cpu_line_style,
        'cpu_label': cpu_label,
        'cpu_label_color': cpu_label_color,
        'cpu_label_size': cpu_label_size,
        'cpu_visible': cpu_visible,
        'gpu_line_width': gpu_line_width,
        'gpu_line_color': gpu_line_color,
        'gpu_line_style': gpu_line_style,
        'gpu_label': gpu_label,
        'gpu_label_color': gpu_label_color,
        'gpu_label_size': gpu_label_size,
        'gpu_visible': gpu_visible,
        'sys_line_width': sys_line_width,
        'sys_line_color': sys_line_color,
        'sys_line_style': sys_line_style,
        'sys_label': sys_label,
        'sys_label_color': sys_label_color,
        'sys_label_size': sys_label_size,
        'sys_visible': sys_visible,
        'bottom_line_width': bottom_line_width,
        'bottom_line_color': bottom_line_color,
        'bottom_line_style': bottom_line_style,
        'bottom_label': bottom_label,
        'bottom_label_color': bottom_label_color,
        'bottom_label_size': bottom_label_size,
        'bottom_visible': bottom_visible,
        'rear_line_width': rear_line_width,
        'rear_line_color': rear_line_color,
        'rear_line_style': rear_line_style,
        'rear_label': rear_label,
        'rear_label_color': rear_label_color,
        'rear_label_size': rear_label_size,
        'rear_visible': rear_visible
    }

    return config_values

def update_config(setting, value):
    config = configparser.ConfigParser()
    default_config = create_config()
    current_config = config.read('config.ini')
    try:
        _setting_data_type = type(default_config[setting])

        if _setting_data_type == bool:
            try:
                value = bool(value)
            except ValueError:
                print('Invalid value for boolean setting')
        elif _setting_data_type == int:
            try:
                value = int(value)
            except ValueError:
                print('Invalid value for integer setting')
        else:
            try:
                value = str(value)
            except ValueError:
                print('Invalid value for string setting')
    except KeyError:
        print(f'Settings not found. Adding {setting} to config.ini')


    try:
        if value == 'True' or value == 'False':
            value = bool(value)
        elif value.isdigit():
            value = int(value)
        else:
            value = str(value)
    except ValueError:
        print(f'Invalid data type')

    if not setting in current_config.keys() or not setting in config.keys():
        current_config.add_section('OTHER')
        current_config.set('OTHER', setting, value)
    else:
        for section in current_config.sections():
            if setting in current_config[section]:
                current_config.set(section, setting, value)
    

    with open('config.ini', 'w') as configfile:
        configfile.write(current_config)
if __name__ == '__main__':
    if os.path.exists('config.ini'):
        config_data = read_config()
    else:
        config_data = create_config()
    main()

