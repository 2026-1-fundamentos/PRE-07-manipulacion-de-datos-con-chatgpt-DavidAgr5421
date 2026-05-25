import logging
import os

import pandas as pd
import matplotlib.pyplot as plt

from homework.utils import load_csv, save_csv, transform_by

def pipeline(file_path : str = 'files/'):
    
    input_path = file_path + 'input/'
    output_path = file_path + 'output/'
    plot_path = file_path + 'plots/'
    
    if not os.path.exists(output_path):
        
        os.mkdir(output_path)
    
    timesheet = load_csv(input_path + 'timesheet.csv')
    
    # Task 1
    
    timesheet_hours_miles_avg_unique = transform_by(timesheet)
    
    save_csv(timesheet_hours_miles_avg_unique, output_path + 'timesheet_hours_miles_avg_unique.csv')
    
    # Task 2
    
    timesheet_hours_avg = transform_by(timesheet, columns = ['hours-logged'], unique = False)
    
    save_csv(timesheet_hours_avg, output_path + 'timesheet_hours_avg.csv')
    
    # Task 3
    
    low_average = timesheet_hours_avg['hours-logged'] < timesheet_hours_avg['avg-hours-logged']
    timesheet_below = timesheet_hours_avg[low_average].copy()
    
    logging.info("Filtrado completado. Se ha creado la tabla 'timesheet_below'.")
    logging.info(f"Registros originales: {len(timesheet_hours_avg)} | Registros filtrados: {len(timesheet_below)}")
    
    # Task 4
    
    timesheet_hours_miles_sum_unique = transform_by(timesheet, transformation='sum')
    
    save_csv(timesheet_hours_miles_sum_unique, output_path + 'timesheet_hours_miles_sum_unique.csv')
    
    # Task 5
    
    drivers = load_csv(input_path + 'drivers.csv')
    
    summary = pd.merge(drivers[['driverId', 'name']], timesheet_hours_miles_sum_unique, on='driverId', how='inner')
    
    logging.info("Tabla 'summary' cargada y preparada en memoria.")
        
    save_csv(summary, output_path + 'summary.csv')
    
    # Task 6
    
    top10 = summary.nlargest(10, 'sum-miles-logged').copy()
    
    logging.info("Filtrado de los 10 conductores con más millas completado con éxito.")
    
    save_csv(top10, output_path + 'top10.csv')
    
    if not os.path.exists(plot_path):
        
        os.mkdir(plot_path)

    plt.figure(figsize=(8,5))
    top10.plot(x='name', y='sum-miles-logged', kind='bar', color='skyblue')
    plt.title('Frecuencia de Conductores')
    plt.xlabel('Conductor')
    plt.ylabel('Frecuencia')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(plot_path + 'top10_drivers.png', dpi=300, bbox_inches='tight')

if __name__ == '__main__':
    
    pipeline()