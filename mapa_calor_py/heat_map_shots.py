import matplotlib.pyplot as plt
# import pandas as pd
# import seaborn as sns
import numpy as np
from scipy.ndimage import gaussian_filter
import matplotlib.cm as cm
from matplotlib.patches import Arc
from .shooting_functions import *

##################################################################################
def plot_heat_map_shots(filename, mapa_calor):
    interval_min_x = -250
    interval_max_x = 250
    interval_min_y = -47.5
    interval_max_y = 422.5

    # filename = 'vedruna_22-23.txt'
    # filename = 'marf4.txt'
    # filename = '2_taja_shot_chart.txt't 
    # filename = '15_stefy_shot_chart.txt'
    # filename = '6_trigue_shot_chart.txt'
    # filename = '8_bello_shot_chart.txt'
    # filename = 'aniento_nbo.txt'
    titol = ''
    # mapa_calor = 1

    LOC_X_o, LOC_Y_o, LOC_X_x, LOC_Y_x = read_score_shooting_positions(filename)

    LOC_X_x = np.array(LOC_X_x)
    LOC_Y_x = np.array(LOC_Y_x)
    LOC_X_o = np.array(LOC_X_o)
    LOC_Y_o = np.array(LOC_Y_o)

    # LOC_X = np.array([52.3533, 48.06, 21.4533, 57.1867, 18.5133, 63.68, 37.8467, 71.72, 38.62, 72.0333, 24.86,
    #                43.42, 36.92, 53.0067, 53.32, 72.4933, 37.54, 55.02, 80.8467, 23.7733, 14.8067, 55.02,
    #                63.3733, 53.6267, 21.3, 43.7267, 76.1467, 58.8133, 45.12, 23, 9.08, 2.27333, 53.78, 
    #                46.0467, 55.3267, 25.7867, 55.7933, 42.6467, 38.62, 56.72,70.9467, 94.3067, 38.5733, 
    #                56.5667, 52.08, 55.3267, 47.44, 95.3867, 67.8533, 44.6533, 53.0067, 44.6533, 5.06, 42.9533,
    #                56.4133, 57.0267, 40.48, 59.66, 46.9733, 84.8667, 3.04667 
    #                ])

    # LOC_Y = np.array([67.5571, 63.3857, 55.6, 24.2929, 40.8571, 20.3214, 19.6643, 34.5643, 63.2143, 56.7571,
    #               12.2071, 23.4714, 18.6714, 13.3714, 20.1571, 58.9143, 17.6714, 16.1786, 54.9357, 57.25, 
    #               48.3143, 17.5071, 22.1429, 30.2643, 24.7929, 60.8929, 57.4214, 13.3643, 14.5286, 66.0357,
    #               43.0143, 15.1929, 17.6714, 13.6286, 19.3286, 57.9143, 13.5286, 17.0071, 11.7071, 14.8571,
    #               57.4143, 33.4, 21.8643, 18.3357, 31.0929, 19.5, 15.6857, 23.9643, 31.75, 17.1786, 17.0143,
    #               18.0571, 27.6143, 15.35, 22.9714, 16.0143, 34.5643, 17.6714, 17.1786, 25.4571, 14.0286
    #               ])

    scaled_LOC_X_x = (LOC_X_x  / 100) * (interval_max_x - interval_min_x) + interval_min_x
    scaled_LOC_Y_x = (LOC_Y_x  / 100) * (interval_max_y - interval_min_y) + interval_min_y
    scaled_LOC_X_o = (LOC_X_o  / 100) * (interval_max_x - interval_min_x) + interval_min_x
    scaled_LOC_Y_o = (LOC_Y_o  / 100) * (interval_max_y - interval_min_y) + interval_min_y

    scaled_LOC_X = np.concatenate((scaled_LOC_X_x, scaled_LOC_X_o))
    scaled_LOC_Y = np.concatenate((scaled_LOC_Y_x, scaled_LOC_Y_o))

    #########################################################
    # Define % in 6 zones of the court

    # Paint
    paint_X_o = []
    paint_Y_o = []
    paint_X_x = []
    paint_Y_x = []

    for x, y in zip(scaled_LOC_X_o, scaled_LOC_Y_o):
        if -80 <= x <= 80 and -47.5 <= y <= 142.5:
            paint_X_o.append(x)
            paint_Y_o.append(y)
            
    for x, y in zip(scaled_LOC_X_x, scaled_LOC_Y_x):
        if -80 <= x <= 80 and -47.5 <= y <= 142.5:
            paint_X_x.append(x)
            paint_Y_x.append(y)

    # Left side middie
    sideMiddieL_X_o = []
    sideMiddieL_Y_o = []
    sideMiddieL_X_x = []
    sideMiddieL_Y_x = []

    for x, y in zip(scaled_LOC_X_o, scaled_LOC_Y_o):
        if -220 <= x <= -80 and -47.5 <= y <= 92.6:
            sideMiddieL_X_o.append(x)
            sideMiddieL_Y_o.append(y)
            
    for x, y in zip(scaled_LOC_X_x, scaled_LOC_Y_x):
        if -220 <= x <= -80 and -47.5 <= y <= 92.6:
            sideMiddieL_X_x.append(x)
            sideMiddieL_Y_x.append(y)

    # Right side middie
    sideMiddieR_X_o = []
    sideMiddieR_Y_o = []
    sideMiddieR_X_x = []
    sideMiddieR_Y_x = []

    for x, y in zip(scaled_LOC_X_o, scaled_LOC_Y_o):
        if -220 <= x <= -80 and -47.5 <= y <= 92.6:
            sideMiddieR_X_o.append(x)
            sideMiddieR_Y_o.append(y)
            
    for x, y in zip(scaled_LOC_X_x, scaled_LOC_Y_x):
        if -220 <= x <= -80 and -47.5 <= y <= 92.6:
            sideMiddieR_X_x.append(x)
            sideMiddieR_Y_x.append(y)

    # Corner left
    cornerL_X_o = []
    cornerL_Y_o = []
    cornerL_X_x = []
    cornerL_Y_x = []

    for x, y in zip(scaled_LOC_X_o, scaled_LOC_Y_o):
        if -250 <= x < -220 and -47.5 <= y <= 92.6:
            cornerL_X_o.append(x)
            cornerL_Y_o.append(y)
            
    for x, y in zip(scaled_LOC_X_x, scaled_LOC_Y_x):
        if -250 <= x < -220 and -47.5 <= y <= 92.6:
            cornerL_X_x.append(x)
            cornerL_Y_x.append(y)

    # Corner Right
    cornerR_X_o = []
    cornerR_Y_o = []
    cornerR_X_x = []
    cornerR_Y_x = []

    for x, y in zip(scaled_LOC_X_o, scaled_LOC_Y_o):
        if 220 < x <= 250 and -47.5 <= y <= 92.6:
            cornerR_X_o.append(x)
            cornerR_Y_o.append(y)
            
    for x, y in zip(scaled_LOC_X_x, scaled_LOC_Y_x):
        if 220 < x <= 250 and -47.5 <= y <= 92.6:
            cornerR_X_x.append(x)
            cornerR_Y_x.append(y)

    # Wing left 3pt
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=2, color='black')
    wingL_X_o = []
    wingL_Y_o = []
    wingL_X_x = []
    wingL_Y_x = []

    for x, y in zip(scaled_LOC_X_o, scaled_LOC_Y_o):
        if -220 < x < -80 and (is_point_outside_arc(x,y,three_arc)):
            wingL_X_o.append(x)
            wingL_Y_o.append(y)

    for x, y in zip(scaled_LOC_X_x, scaled_LOC_Y_x):
        if -220 < x < -80 and (is_point_outside_arc(x,y,three_arc)):
            wingL_X_x.append(x)
            wingL_Y_x.append(y)
            
    # Wing right 3pt
    wingR_X_o = []
    wingR_Y_o = []
    wingR_X_x = []
    wingR_Y_x = []

    for x, y in zip(scaled_LOC_X_o, scaled_LOC_Y_o):
        if 80 < x < 220 and (is_point_outside_arc(x,y,three_arc)):
            wingR_X_o.append(x)
            wingR_Y_o.append(y)

    for x, y in zip(scaled_LOC_X_x, scaled_LOC_Y_x):
        if 80 < x < 220 and (is_point_outside_arc(x,y,three_arc)):
            wingR_X_x.append(x)
            wingR_Y_x.append(y)

    # Wing left middie
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=2, color='black')
    wingML_X_o = []
    wingML_Y_o = []
    wingML_X_x = []
    wingML_Y_x = []

    for x, y in zip(scaled_LOC_X_o, scaled_LOC_Y_o):
        if -220 < x < -80 and (~is_point_outside_arc(x,y,three_arc)) and y > 92.6:
            wingML_X_o.append(x)
            wingML_Y_o.append(y)

    for x, y in zip(scaled_LOC_X_x, scaled_LOC_Y_x):
        if -220 < x < -80 and (~is_point_outside_arc(x,y,three_arc)) and y > 92.6:
            wingML_X_x.append(x)
            wingML_Y_x.append(y)

    # Wing right middie
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=2, color='black')
    wingMR_X_o = []
    wingMR_Y_o = []
    wingMR_X_x = []
    wingMR_Y_x = []

    for x, y in zip(scaled_LOC_X_o, scaled_LOC_Y_o):
        if 80 < x < 220 and (~is_point_outside_arc(x,y,three_arc)) and y > 92.6:
            wingMR_X_o.append(x)
            wingMR_Y_o.append(y)

    for x, y in zip(scaled_LOC_X_x, scaled_LOC_Y_x):
        if 80 < x < 220 and (~is_point_outside_arc(x,y,three_arc)) and y > 92.6:
            wingMR_X_x.append(x)
            wingMR_Y_x.append(y)
            
    # Top 3pt
    top3_X_o = []
    top3_Y_o = []
    top3_X_x = []
    top3_Y_x = []

    for x, y in zip(scaled_LOC_X_o, scaled_LOC_Y_o):
        if -80 <= x <= 80 and (is_point_outside_arc(x,y,three_arc)):
            top3_X_o.append(x)
            top3_Y_o.append(y)
            
    for x, y in zip(scaled_LOC_X_x, scaled_LOC_Y_x):
        if -80 <= x <= 80 and (is_point_outside_arc(x,y,three_arc)):
            top3_X_x.append(x)
            top3_Y_x.append(y)

    # Top middie
    top_X_o = []
    top_Y_o = []
    top_X_x = []
    top_Y_x = []

    for x, y in zip(scaled_LOC_X_o, scaled_LOC_Y_o):
        if -80 <= x <= 80 and (~is_point_outside_arc(x,y,three_arc)) and y > 142.5:
            top_X_o.append(x)
            top_Y_o.append(y)
            
    for x, y in zip(scaled_LOC_X_x, scaled_LOC_Y_x):
        if -80 <= x <= 80 and (~is_point_outside_arc(x,y,three_arc)) and y > 142.5:
            top_X_x.append(x)
            top_Y_x.append(y)

    ###########################################################################################################
    # First draw court lines

    fig = plt.figure(figsize=(8,7))
    fig, ax = plt.subplots(figsize=(15,5))
    if not mapa_calor:
        plt.scatter(scaled_LOC_X_x, scaled_LOC_Y_x,marker='x',c='#d62728')
        plt.scatter(scaled_LOC_X_o, scaled_LOC_Y_o,marker='o',c='#2ca02c')

    def safe_divide(numerator, denominator, fallback=0):
        return numerator / denominator if denominator != 0 else fallback


    ratio_paint = safe_divide(np.size(paint_X_o), np.size(paint_X_o) + np.size(paint_X_x)) *100
    ratio_sideMiddieL = safe_divide(np.size(sideMiddieL_X_o), np.size(sideMiddieL_X_o) + np.size(sideMiddieL_X_x)) *100
    ratio_sideMiddieR = safe_divide(np.size(sideMiddieR_X_o), np.size(sideMiddieR_X_o) + np.size(sideMiddieR_X_x)) *100
    ratio_cornerL = safe_divide(np.size(cornerL_X_o), np.size(cornerL_X_o) + np.size(cornerL_X_x)) * 100
    ratio_cornerR = safe_divide(np.size(cornerR_X_o), np.size(cornerR_X_o) + np.size(cornerR_X_x)) *100
    ratio_wingL = safe_divide(np.size(wingL_X_o), np.size(wingL_X_o) + np.size(wingL_X_x)) *100
    ratio_wingR = safe_divide(np.size(wingR_X_o), np.size(wingR_X_o) + np.size(wingR_X_x)) *100
    ratio_wingML = safe_divide(np.size(wingML_X_o), np.size(wingML_X_o) + np.size(wingML_X_x)) *100
    ratio_wingMR = safe_divide(np.size(wingMR_X_o), np.size(wingMR_X_o) + np.size(wingMR_X_x)) *100
    ratio_top = safe_divide(np.size(top_X_o), np.size(top_X_o) + np.size(top_X_x)) *100
    ratio_top3 = safe_divide(np.size(top3_X_o), np.size(top3_X_o) + np.size(top3_X_x)) *100

    plt.text(-21, -15, '%.d/%.d \n  %.d%%'%(np.size(paint_X_o),np.size(paint_X_o) + np.size(paint_X_x),ratio_paint), fontsize=12, color='gray')
    plt.text(-175, 70, '%.d/%.d \n  %.d%%'%(np.size(sideMiddieL_X_o),np.size(sideMiddieL_X_o) + np.size(sideMiddieL_X_x),ratio_sideMiddieL), fontsize=12, color='gray')
    plt.text(125, 70, '%.d/%.d \n  %.d%%'%(np.size(sideMiddieR_X_o),np.size(sideMiddieR_X_o) + np.size(sideMiddieR_X_x),ratio_sideMiddieR), fontsize=12, color='gray')
    plt.text(-300, 50, '%.d/%.d \n  %.d%%'%(np.size(cornerL_X_o),np.size(cornerL_X_o) + np.size(cornerL_X_x),ratio_cornerL), fontsize=12, color='gray')
    plt.text(260, 50, '%.d/%.d \n  %.d%%'%(np.size(cornerR_X_o),np.size(cornerR_X_o) + np.size(cornerR_X_x),ratio_cornerR), fontsize=12, color='gray')
    plt.text(-200, 250, '%.d/%.d \n  %.d%%'%(np.size(wingL_X_o),np.size(wingL_X_o) + np.size(wingL_X_x),ratio_wingL), fontsize=12, color='gray')
    plt.text(180, 250, '%.d/%.d \n  %.d%%'%(np.size(wingR_X_o),np.size(wingR_X_o) + np.size(wingR_X_x),ratio_wingR), fontsize=12, color='gray')
    plt.text(-160, 160, '%.d/%.d \n  %.d%%'%(np.size(wingML_X_o),np.size(wingML_X_o) + np.size(wingML_X_x),ratio_wingML), fontsize=12, color='gray')
    plt.text(110, 160, '%.d/%.d \n  %.d%%'%(np.size(wingMR_X_o),np.size(wingMR_X_o) + np.size(wingMR_X_x),ratio_wingMR), fontsize=12, color='gray')
    plt.text(-12, 190,'%.d/%.d \n  %.d%%'%(np.size(top_X_o),np.size(top_X_o) + np.size(top_X_x),ratio_top), fontsize=12, color='gray')
    plt.text(-12, 280,'%.d/%.d \n  %.d%%'%(np.size(top3_X_o),np.size(top3_X_o) + np.size(top3_X_x),ratio_top3), fontsize=12, color='gray')

    draw_court(outer_lines=True)
    plt.xlim(interval_min_x,interval_max_x)

    # Descending values along th y axis from bottom to top
    # in order to place the hoop by the top of plot
    plt.ylim(interval_max_y, interval_min_y)
    # plt.show()

    ######################################################################################
    # On top of the court, we draw the heatmap

    s = 5 # sigma of gaussian filter
    heatmap, xedges, yedges = np.histogram2d(scaled_LOC_X, scaled_LOC_Y, bins=200, 
                                            range=[[interval_min_x, interval_max_x], [interval_min_y, interval_max_y]])
    heatmap = gaussian_filter(heatmap, sigma=s)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    ax = plt.gca()
    if mapa_calor:
        im = ax.imshow(heatmap.T, extent=extent, origin='lower', cmap=cm.CMRmap_r)
    ax.set_title(titol)
    # plt.colorbar(im)
    plt.show()

    return fig



