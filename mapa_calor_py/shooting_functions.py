from matplotlib.patches import Circle, Rectangle, Arc
import matplotlib.pyplot as plt
import numpy as np


##############################################################################
# Function to draw the court from nbashot git

def draw_court(ax=None, color='black', lw=2, outer_lines=False):
    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()

    # Create the various parts of an NBA basketball court

    # Create the basketball hoop
    # Diameter of a hoop is 18" so it has a radius of 9", which is a value
    # 7.5 in our coordinate system
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                          fill=False)
    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                          fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                     color=color)

    # Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                               color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    # I just played around with the theta values until they lined up with the 
    # threes
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                    color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)

    # List of the court elements to be plotted onto the axes
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                      bottom_free_throw, restricted, corner_three_a,
                      corner_three_b, three_arc, center_outer_arc,
                      center_inner_arc]

    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax

##############################################################################
# Function to define shot chart points outside 3pt arc

def is_point_outside_arc(x, y, arc: Arc):
    # Get arc parameters
    cx, cy = arc.center
    radius = arc.width / 2  # width = diameter
    theta1 = arc.theta1
    theta2 = arc.theta2

    # Convert point to polar coordinates relative to arc center
    dx = x - cx
    dy = y - cy
    r = np.hypot(dx, dy)
    theta = np.degrees(np.arctan2(dy, dx)) % 360

    # Check if point is within radius and angle range
    within_radius = r > radius
    within_angle = theta1 <= theta <= theta2

    return within_radius and within_angle


##############################################################################
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



###############################################################################

def read_score_shooting_positions(filename):
    left_score = []
    top_score = []
    left_miss = []
    top_miss = []  
    
    with open(filename, 'r') as file:
        html_text = file.read()  
    
    pattern = r'r-(ejvdv9|jwgaoi)"\s*style="left:\s*([\d.]+)%;\s*top:\s*([\d.]+)%;"'
    matches = re.findall(pattern, html_text)
    
    
    for match in matches:
        code = match[0]
        left_percentage = float(match[1])
        top_percentage = float(match[2])
        
    
        if code == "ejvdv9":
            left_score.append(left_percentage)
            top_score.append(top_percentage)
        elif code == "jwgaoi":
            left_miss.append(left_percentage)
            top_miss.append(top_percentage)
            
    return left_score, top_score, left_miss, top_miss