import logging
import uuid

import pandas as pd

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_csv(
    path: str = 'timesheet.csv',
    sep: str = ","
    ) -> pd.DataFrame | None:
    
    try:
        
        df = pd.read_csv(path, sep=sep)
        
        logging.info(f"Archivo '{path}' cargado correctamente.")
        
        return df
    
    except FileNotFoundError:
        
        logging.error(f"El archivo '{path}' no se encuentra en la ruta especificada.")
        
        return None

def save_csv(
    dataframe: pd.DataFrame | None = None,
    path : str | None = None
    ) -> None:
    
    if dataframe is not None:
        
        if path and path.endswith('.csv'):
        
            dataframe.to_csv(path, index=False)
        
        else:
            
            path = 'dataframe-' + str(uuid.uuid4()) + '.csv'
            
            dataframe.to_csv(path, index=False)
            
        logging.info(f"Tabla guardada exitosamente en '{path}'")
        
        return
    
    logging.error("No hay ningún DataFrame para exportar")
    
    return

def transform_by(
    dataframe: pd.DataFrame | None = None,
    by : str = 'driverId',
    columns : list[str] = ['hours-logged', 'miles-logged'],
    transformation: str = 'mean',
    unique: bool = True) -> None:
    
    if dataframe is None:
        
        logging.error("No hay ningún DataFrame para transformar")
        
        return
    
    if transformation.isalpha():
        
        transformation = transformation.strip().lower()
        
        if transformation not in ('mean', 'sum', 'max-min'):
            
            logging.error("Transformación invalida")
            
            return
    else:
        
        logging.error("Transformación invalida")
        
        return
    
    if all(pd.Series([by] + columns).isin(dataframe.columns)):
        
        if 'mean' in transformation:
            
            result_columns = ['avg-' + name for name in columns]
            
            if unique:
                
                result = (
                    dataframe
                    .groupby(by)[columns]
                    .mean()
                    .reset_index()
                )

                # Renombrar las columnas para mayor claridad
                result = result.rename(columns=dict(zip(columns, result_columns)))
    
            else:
                
                # Hacemos una copia explícita para evitar modificar el DataFrame original por accidente
                result = dataframe.copy()
                
                # Calculamos el promedio por grupo y 'transformamos' el resultado al tamaño original        
                result[result_columns] = (
                    dataframe
                    .groupby(by)[columns]
                    .transform('mean')
                    )
                
                logging.info(f"Las nuevas columnas { ", ".join(result_columns)} calculada y añadida correctamente.")
        
            logging.info(f"Cálculo de promedios por {by} completado con éxito.")
    
        elif 'sum' in transformation:
            
            result_columns = ['sum-' + name for name in columns]
            
            if unique:
                
                result = (
                    dataframe
                    .groupby(by)[columns]
                    .sum()
                    .reset_index()
                )

                result = result.rename(columns=dict(zip(columns, result_columns)))
    
            else:
                
                result = dataframe.copy()
                
                # Calculamos la suma por grupo y transformamos el resultado
                result[result_columns] = (
                    dataframe
                    .groupby(by)[columns]
                    .transform('sum')
                    )
                
                logging.info(f"Las nuevas columnas { ", ".join(result_columns)} calculada y añadida correctamente.")
        
            logging.info(f"Cálculo de sumas por {by} completado con éxito.")
    
        else:
            
            result_columns = ['min-' + name for name in columns]
            
            if unique:
                
                result = (
                    dataframe
                    .groupby(by)[columns]
                    .agg(['min', 'max'])
                    .reset_index()
                )

                result = result.rename(columns=dict(zip(columns, result_columns)))
    
            else:
                
                result = dataframe.copy()
                
                # Calculamos la suma por grupo y transformamos el resultado
                result[result_columns] = (
                    dataframe
                    .groupby(by)[columns]
                    .transform('sum')
                    )
                
                logging.info(f"Las nuevas columnas { ", ".join(result_columns)} calculada y añadida correctamente.")
        
            logging.info(f"Cálculo de sumas por {by} completado con éxito.")
        
        # Mostrar el resultado formateado a través de logging
        
        logging.info("\n--- RESULTADOS DEL ANÁLISIS ---\n%s", result.head(5).to_string(index=False))
        
        return result
    
    logging.error(f"No se encontraron las columnas especificadas en el DataFrame: {", ".join([by] + columns)}")
    
    return