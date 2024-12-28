import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from get_data_brasil import run_crear_excel_brasil
from get_data_brasil_wcota import run_crear_excel_brasil_wcota
from get_data_pernambuco import run_crear_excel_recife
from get_data_ourworldindata import run_crear_excel_ourworldindata
from pandas import ExcelWriter
import colormap
import plotly.graph_objects as go
import base64
import os

matplotlib.use('agg')


def plotly_html(a_14_days, p_seven, dia, bra_title, save_path, filename_bg):

    for i in range(len(p_seven)):
        if p_seven[i] < 0.0:
            p_seven[i] = 0.0

    color_map = []
    for i in range(len(a_14_days)):
        if i < len(a_14_days) - 60:
            color_map.append('rgba(0, 0, 0, 0.1)')
        elif i == len(a_14_days) - 1:
            color_map.append('rgba(255, 255, 255, 0.6)')
        else:
            color_map.append('Blue')

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=a_14_days,
                             y=p_seven,
                             text=dia,
                             mode='lines+markers',
                             marker=dict(
                                 color=color_map,
                                 showscale=False,
                                 size=10,
                                 line=dict(
                                     color='Black',
                                     width=0.2)),
                             line=dict(
                                 color="Black",
                                 width=0.5,
                                 dash="dot"),
                             ))
    fig.add_shape(type="line",
                  x0=0,
                  y0=1,
                  x1=max(a_14_days),
                  y1=1,
                  line=dict(
                      color="Black",
                      width=1,
                      dash="dot",
                  ))

    image_filename = filename_bg
    img = base64.b64encode(open(image_filename, 'rb').read())
    x = round(a_14_days.max())
    y = round(p_seven.max())
    print(x, y)

    fig.add_layout_image(
        dict(
            source='data:image/png;base64,{}'.format(img.decode()),
            xref="x",
            yref="y",
            x=0,
            y=p_seven.max(),
            sizex=a_14_days.max(),
            sizey=p_seven.max(),
            xanchor="left",
            yanchor="top",
            sizing="stretch",
            opacity=0.95,
            layer="below"))
    fig.add_annotation(dict(font=dict(color='black', size=9),
                            xref="paper", yref="paper",
                            x=0.9, y=0.9,
                            text="EPG > 100: High", showarrow=False))

    fig.add_shape(type="rect",
                  xref="paper", yref="paper",
                  x0=0.9, x1=0.91, y0=0.87, y1=0.89, fillcolor="Red", line_color="Red")

    fig.add_annotation(dict(font=dict(color='black', size=9),
                            xref="paper", yref="paper",
                            x=0.9, y=0.86,
                            text=" 70 < EPG < 100: Moderate-high", showarrow=False))

    fig.add_shape(type="rect",
                  xref="paper", yref="paper",
                  x0=0.9, x1=0.91, y0=0.86, y1=0.78, fillcolor="Yellow", line_color="Yellow")

    fig.add_annotation(dict(font=dict(color='black', size=9),
                            xref="paper", yref="paper",
                            x=0.9, y=0.82,
                            text=" 30 < EPG < 70 : Moderate", showarrow=False))

    fig.add_annotation(dict(font=dict(color='black', size=9),
                            xref="paper", yref="paper",
                            x=0.9, y=0.78,
                            text="EPG < 30: Low", showarrow=False))
    fig.add_annotation(dict(font=dict(color='blue', size=9),
                            xref="paper", yref="paper",
                            x=0.9, y=0.728,
                            text="Last 60 days", showarrow=False))
    fig.add_shape(type="rect",
                  xref="paper", yref="paper",
                  x0=0.9, x1=0.91, y0=0.77, y1=0.74, fillcolor="Green", line_color="Green")
    fig.add_shape(type="rect",
                  xref="paper", yref="paper",
                  x0=0.9, x1=0.91, y0=0.725, y1=0.70, fillcolor="Blue", line_color="Blue")

    fig.update_layout(plot_bgcolor='rgb(255,255,255)',
                      width=800,
                      height=600,
                      xaxis_showgrid=False,
                      yaxis_showgrid=False,
                      xaxis_title="Attack rate per 10⁵ inh. (last 14 days)",
                      yaxis_title="\u03C1 (mean of the last 7 days)",
                      title={
                          'text': bra_title,
                          'y': 0.9,
                          'x': 0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'},
                      )

    fig.update_xaxes(rangemode="tozero")

    fig.update_yaxes(rangemode="tozero")

    # fig.show()
    os.remove(filename_bg)

    fig.write_html(filename_bg+'.html', include_plotlyjs="cdn")

def run_risk_diagrams(region_id, file_others_cases, file_others_pop, radio_valor, ourworldindata_country):
    last_days_time = 30
    html = False
    last_days = False

    if radio_valor == 1:
        last_days = True
    elif radio_valor == 2:
        html = True
    else:
        pass

    dataTable = []
    dataTable_EPG = []

    data_sources = {
        'brasil': {'function': run_crear_excel_brasil, 'filename': 'data/Data_Brasil.xlsx', 'population_file': 'data/pop_Brasil_v3.xlsx', 'sheet_name': 'Cases'},
        'brasil_regions': {'function': run_crear_excel_brasil, 'filename': 'data/Data_Brasil.xlsx', 'population_file': 'data/pop_Brasil_Regions_v3.xlsx', 'sheet_name': 'Regions'},
        'recife': {'function': run_crear_excel_recife, 'filename': 'data/cases-recife.xlsx', 'population_file': 'data/pop_recife_v1.xlsx', 'sheet_name': 'Cases'},
        'WCOTA': {'function': lambda: run_crear_excel_brasil_wcota('SP'), 'filename': 'data/cases-wcota.xlsx', 'population_file': 'data/pop_SP_v1.xlsx', 'sheet_name': 'Cases'},
        'ourworldindata': {'function': lambda: run_crear_excel_ourworldindata(ourworldindata_country), 'filename': 'data/ourworldindata.xlsx', 'population_file': 'data/pop_ourworldindata_v1.xlsx', 'sheet_name': 'Cases'},
        'others': {'filename': file_others_cases, 'population_file': file_others_pop, 'sheet_name': 'Cases'}
    }

    try:
        source = data_sources[region_id]
        if 'function' in source:
            source['function']()
        filename = source['filename']
        filename_population = source['population_file']
        sheet_name = source['sheet_name']
    except AttributeError:
        print("Error! Not found file or could not download!")

    """
    The cumulative cases excel file has a date column and a column for each region.
    The first column values are the dates, and the rest of the columns values are the cumulative number of cases per region on that date.

    The population excel file has a column for each region and the total population of that region at the line below it.

    The regions in the population excel file may not match all the regions in the cumulative cases excel file. This is because some regions do not have data available.
    """
    cumulative_cases = pd.read_excel(filename, sheet_name=sheet_name)
    dates = pd.to_datetime(cumulative_cases['date']).dt.strftime('%d/%m/%Y').to_numpy()
    population = pd.read_excel(filename_population)

    for region in population.columns:
        region_cumulative_cases = cumulative_cases[region].to_numpy()

       # Calculate the number of cases per day by subtracting the cumulative cases of the previous day from the current day's cumulative cases. 
        daily_cases = np.zeros((len(dates)), dtype=int)
        for i in range(len(dates)):
            daily_cases[i] = region_cumulative_cases[i] - region_cumulative_cases[i - 1] if i > 0 else region_cumulative_cases[i]
    
        # Calculate the velocity of the spread (rho) of each day by calculating the average number of cases per day over a rolling window of 7 days. 
        rho = np.zeros((len(dates)), dtype=float)
        for i in range(7, len(dates)):
            aux = daily_cases[i - 5] + daily_cases[i - 6] + daily_cases[i - 7]
            div = 1 if aux == 0 else aux
            rho[i] = min((daily_cases[i] + daily_cases[i - 1] + daily_cases[i - 2]) / div, 4)

        mean_7_day_rate = np.zeros((len(dates)), dtype=float)
        new_cases_14_days = np.zeros((len(dates)), dtype=float)
        attack_rate_14_days = np.zeros((len(dates)), dtype=float)
        risk = np.zeros((len(dates)), dtype=float)
        risk_per_100k = np.zeros((len(dates)), dtype=float)

        day13 = 13
        for i in range(day13, len(dates)):
            new_cases_14_days[i] = np.sum(daily_cases[i - day13: i + 1])
            mean_7_day_rate[i] = np.average(rho[i - 6:i + 1])
            attack_rate_14_days[i] = new_cases_14_days[i] / population[region] * 100_000
            risk[i] = new_cases_14_days[i] * mean_7_day_rate[i]
            risk_per_100k[i] = attack_rate_14_days[i] * mean_7_day_rate[i]

        first_day = dates[day13]
        last_day = dates[-1]
        first_day = first_day.replace('/', '-')
        last_day = last_day.replace('/', '-')

        # For last 15 days
        if last_days:
            a_14_days_solo = []
            day13 = len(attack_rate_14_days) - last_days_time
            first_day = dates[day13]
            for i in range(len(attack_rate_14_days)):
                if i >= len(attack_rate_14_days) - last_days_time:
                    a_14_days_solo.append(attack_rate_14_days[i])
                else:
                    a_14_days_solo.append(None)

        save_path = 'static_graphic' + '/' + last_day + '-' + region
        save_path_temp = 'static_graphic' + '/interactive_graphic/' + last_day + '-' + region
        save_path_xlsx = 'static_graphic/xlsx/'

        figure, axes = plt.subplots(sharex=True)
        del figure

        if last_days:
            axes.plot(attack_rate_14_days, mean_7_day_rate, 'o--', fillstyle='none', linewidth=0.5, color=(0, 0, 0, 0.15))
            axes.plot(a_14_days_solo, mean_7_day_rate, 'ko--', fillstyle='none', linewidth=0.5)  # For last 15 days
            axes.plot(a_14_days_solo[-1], mean_7_day_rate[-1], 'bo')
        else:
            axes.plot(attack_rate_14_days, mean_7_day_rate, 'ko--', fillstyle='none', linewidth=0.5)
            axes.plot(attack_rate_14_days[-1], mean_7_day_rate[-1], 'bo')

        # Set y-axis limits and add horizontal line at y=0
        max_y = 4
        axes.set_ylim(0, max_y)
        _, max_x = axes.get_xlim()
        max_x = int(max_x)
        x = np.ones(max_x)
        axes.plot(x, 'k--', fillstyle='none', linewidth=0.5)

        
        # Axes labels
        axes.set_ylabel('$\u03C1$ (mean of the last 7 days)')
        axes.set_xlabel('Attack rate per $10^5$ inh. (last 14 days)')

        ## Add legend to the plot
        # Colors
        red = dict(fc=(1, 0, 0, .5), lw=0, pad=2)
        yellow = dict(fc=(1, 1, 0, .5), lw=0, pad=2)
        green = dict(fc=(0, 1, 0, .5), lw=0, pad=2)
        plt.annotate('  ', (max_x - abs(max_x / 3.3), 3.8), color=(0, 0, 0), ha='left', va='center', fontsize='6', bbox=red)
        plt.annotate('  \n', (max_x - abs(max_x / 3.3), 3.55), color=(0, 0, 0), ha='left', va='center', fontsize='6', bbox=yellow)
        plt.annotate('  ', (max_x - abs(max_x / 3.3), 3.3), color=(0, 0, 0), ha='left', va='center', fontsize='6', bbox=green)

        # Labels
        plt.annotate(' EPG >= 100: High', (max_x - abs(max_x / 3.5), 3.8), color=(0, 0, 0), ha='left', va='center', fontsize='6', bbox=dict(fc=(0, 0, 0, 0), lw=0, pad=2))
        plt.annotate(' 70 < EPG < 100: Moderate-high\n 30 < EPG < 70 : Moderate', (max_x - abs(max_x / 3.5), 3.55), color=(0, 0, 0), ha='left', va='center', fontsize='6', bbox=dict(fc=(0, 0, 0, 0), lw=0, pad=2))
        plt.annotate(' EPG < 30: Low', (max_x - abs(max_x / 3.5), 3.3), color=(0, 0, 0), ha='left', va='center', fontsize='6', bbox=dict(fc=(0, 0, 0, 0), lw=0, pad=2))

        # First day and last day annotations
        axes.annotate(first_day, xy=(attack_rate_14_days[day13], mean_7_day_rate[day13]), xytext=(max_x-abs(max_x/1.5),2.7), arrowprops=dict(arrowstyle="->", connectionstyle="arc3", linewidth=0.4))
        axes.annotate(last_day, xy=(attack_rate_14_days[-1], mean_7_day_rate[-1]), xytext=(max_x-abs(max_x/2),3), arrowprops=dict(arrowstyle="->", connectionstyle="arc3", linewidth=0.4))
        
        plt.title(region)
            
        if ourworldindata_country is not None:
            plt.subplots_adjust(bottom=0.2)
            text_annotate = "*The risk diagram was developed using the Our World in Data database. Last update: " + str(last_day) + "."

            plt.text(0, -1, text_annotate, fontsize=7, wrap=False)

        granularity = 400
        rh = np.arange(0, max_x, 1)
        ar = np.linspace(0, max_y, granularity)
        rh, ar = np.meshgrid(rh, ar)
        epg = rh * ar

        # Normalize the EPG values to a range of 0-100
        epg[epg > 100] = 100

        # Create the colormap
        c = colormap.Colormap()
        mycmap = c.cmap_linear('green(w3c)', 'yellow', 'red')
        axes.pcolorfast([0, max_x], [0, max_y], epg, cmap=mycmap, alpha=0.6)

        axes.set_aspect('auto')

        if html:
            figt, axt = plt.subplots(sharex=True)
            axt.pcolorfast([0, max_x], [0, max_y], epg, cmap=mycmap, alpha=0.6)
            axt.set_axis_off()
            figt.savefig(save_path_temp, format='png', bbox_inches='tight', dpi=300, pad_inches=0)
            plotly_html(attack_rate_14_days, mean_7_day_rate, dates, region, save_path_xlsx, save_path_temp)
        else:
            plt.savefig(save_path + '.png', bbox_inches='tight', dpi=300)
            plt.close('all')
        print("\n\nPrediction for the region of " + region + " performed successfully!\nPath:" + save_path)

        dataTable.append([
            region,
            region_cumulative_cases[-1],
            daily_cases[-1],
            rho[-1],
            mean_7_day_rate[-1],
            new_cases_14_days[-1],
            attack_rate_14_days[-1],
            risk[-1],
            risk_per_100k[-1]
        ])

        for i in range(len(dates)):
            dataTable_EPG.append([dates[i], region, risk_per_100k[i]])

    df = pd.DataFrame(dataTable, columns=['State', 'Cumulative cases', 'New cases', 'ρ', 'ρ7', 'New cases last 14 days (N14)',
                                          'New cases last 14 days per 105 inhabitants (A14)', 'Risk (N14*ρ7)',  'Risk per 10^5 (A14*ρ7)'])
    df_EPG = pd.DataFrame(dataTable_EPG, columns=['DATE', 'CITY', 'EPG'])

    with ExcelWriter(save_path_xlsx + last_day + '_' + region_id + '_report.xlsx') as writer:
        df.to_excel(writer, sheet_name='Alt_Urgell')
    with ExcelWriter(save_path_xlsx + last_day + '_' + region_id + '_report_EPG.xlsx') as writer:
        df_EPG.to_excel(writer, sheet_name='Alt_Urgell')
