from risk_diagrams import run_risk_diagrams
import sys
import requests

def download_and_process_covid_data(plot_type):
    continents = {
        'africa': ['Nigeria', 'South Africa', 'Malawi', 'Morocco', 'Africa', 'Zambia', 'Namibia',
                   'Senegal', 'Gabon', 'Botswana', 'Mozambique', 'Libya', 'Egypt', 'Sao Tome and Principe', 'Tunisia'],
        'europe': ['Spain', 'Portugal', 'France', 'Italy', 'Sweden', 'United Kingdom', 'Andorra', 'Germany'],
        'south_america': ['Chile', 'Brazil', 'Argentina', 'Bolivia', 'Colombia', 'Ecuador', 'Peru', 'Paraguay', 'Uruguay', 'Suriname', 'Venezuela', 'Guyana'],
        'central_america': ['Guatemala'],
        'middle_east': ['Israel', 'Palestine', 'United Arab Emirates', 'Turkey'],
        'north_america': ['Canada', 'United States'],
        'oceania': ['Australia', 'Papua New Guinea', 'New Zealand', 'Fiji']
    }

    print('Downloading COVID-19 data from Our World in Data')
    url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
    response = requests.get(url)
    with open('data/owid-covid-data.csv', 'wb') as file:
        file.write(response.content)

    # Retrieve HTTP meta-data
    print(f'Status code: {response.status_code}')
    print(f'Content type: {response.headers["content-type"]}')
    print(f'Encoding: {response.encoding}')

    for countries in continents.values():
        for country in countries:
            run_risk_diagrams('ourworldindata', plot_type, country)

if __name__ == "__main__":
    # plot_type =  "last_days" | "html"
    plot_type = "last_days"
    run_risk_diagrams('brasil_regions', plot_type)
    run_risk_diagrams('recife', plot_type)
    run_risk_diagrams('brasil', plot_type)
    download_and_process_covid_data(plot_type)

    plot_type = "html"
    run_risk_diagrams('brasil_regions', plot_type)
    run_risk_diagrams('recife', plot_type)
    run_risk_diagrams('brasil', plot_type)
    download_and_process_covid_data(plot_type)
   