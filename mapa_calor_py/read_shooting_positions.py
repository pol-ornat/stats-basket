# Function to import shot position from basquetcatala web

import re

def read_shooting_positions(filename):
    left_values = []
    top_values = []
    
    with open(filename, 'r') as file:
        html_text = file.read()

    pattern = r'style="left:\s*([\d.]+)%;\s*top:\s*([\d.]+)%;"'
    matches = re.findall(pattern, html_text)
    
    for match in matches:
        left_values.append(float(match[0]))
        top_values.append(float(match[1]))
    
    return left_values, top_values