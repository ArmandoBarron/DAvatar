# Transversal Processing Services (TPS)
Los TPS son microservicios para el procesamiento de datos provenientes de una o varias etapas dentro de flujos de trabajo. Para que sea considerado un TPS este debe seguir un efoque de procesamiento ETL (Extract-Transform-Load), mantener las caracteristicas de un microservicio (Escalabilidad, Modularidad, independiente, autocontenido, etc.), y ser capaz de ser desplegado en diferentes infraestructuras de computo.


# TPS de preprocesamiento de datos
A continuacion se describen los TPS utilizados para el preprocesamiento de datos.

## __CleaningTools__  : 
herramientas de limpieza. cuenta con un servicio de limpieza basico para datos nulos y outliers:

* _cleanningtools_: 
    ### URL:
    > POST http://localhost:11003/cleaning/basic'

    ### Datos que recibe:

    > (__data__) : conjunto de datos.

    > (__columns__) : lista de columnas con las que se trabajara
    
    > (__ReplaceWithNa__) : lista de valores para reemplazar con un valor de Na.
    
    > (__DropNa__) : Opciones para eliminar filas con valores NA.comprobar las opciones de pandas dropna. debe ser un dict ().
    
    > (__NaReaplace__) : Opción para rellenar todos los valores NA (por ejemplo, media, moda, -99, 'No valido').
    
    > (__DataTypes__) : lista de dict(). Castear columnas a tipos de datos específicas. Por ejemplo, [{'column':'last_name','type':'string'}]

    ```json 
    {"data":[
    {"Date": "2016-12-06", "Radiation":0.23, "test":-99, "Temperature": 0.7895, "Source": "GCAG"},
    {"Date": "2016-11-06", "Radiation":0.64, "test":-99, "Temperature": 0.7504, "Source": "GCAG"},
    {"Date": "2016-10-06", "Radiation":0.18, "test":35, "Temperature": 0.7292, "Source": "GCAG"},
    {"Date": "2016-05-06", "Radiation":0.73, "test":30, "Temperature": 0.93, "Source": "GISTEMP"},
    {"Date": "2016-04-06", "Radiation":0.65, "test":24, "Temperature": 1.0733, "Source": "GCAG"},
    {"Date": "2016-04-06", "Radiation":0.61, "test":31, "Temperature": 1.09, "Source": "GISTEMP"},
    {"Date": "2016-03-06", "Radiation":0.53, "test":30, "Temperature": 1.2245, "Source": "GCAG"},
    {"Date": "2016-03-06", "Radiation":0.89, "test":11, "Temperature": 1.3, "Source": "GISTEMP"} 
    ],
        "columns":"all","ReplaceWithNa":['None',-99,-99.0,'NaN','nan'],
    "DropNa":None,"NaReaplace":"interpolate"}
    ```

* _melt_: 
Herramienta de transformacion para convertir un dataset en un formato donde ona o mas columnas son identificadores y en resto son desacopladas al eje de las filas (rows).
    ### URL:
        > POST http://localhost:11003/transform/melt'

    ### Datos que recibe:

    > (__data__) : conjunto de datos.

    > (__id_vars__: lista de columnas que funjiran como dientificador
    
    > (__var_name__) : Nombre a utilizar para la columna de la variable.
    
    > (__value_name__) : Nombre para la columna con el valor. (para mas informacion ver funcion melt de pandas.)

    ```json 
    {"data":[
        {"Date": "2016-12-06", "Radiation":0.23, "test":-99, "Temperature": 0.7895, "Source": "GCAG"},
        {"Date": "2016-11-06", "Radiation":0.64, "test":-99, "Temperature": 0.7504, "Source": "GCAG"},
        {"Date": "2016-10-06", "Radiation":0.18, "test":35, "Temperature": 0.7292, "Source": "GCAG"},
        {"Date": "2016-05-06", "Radiation":0.73, "test":30, "Temperature": 0.93, "Source": "GISTEMP"},
        {"Date": "2016-04-06", "Radiation":0.65, "test":24, "Temperature": 1.0733, "Source": "GCAG"},
        {"Date": "2016-04-06", "Radiation":0.61, "test":31, "Temperature": 1.09, "Source": "GISTEMP"},
        {"Date": "2016-03-06", "Radiation":0.53, "test":30, "Temperature": 1.2245, "Source": "GCAG"},
        {"Date": "2016-03-06", "Radiation":0.89, "test":11, "Temperature": 1.3, "Source": "GISTEMP"} 
    ],
    "id_vars":['Date'],"var_name":"Source","value_name":"value_test"}
    ```
        
* _group_: 
Funcion para el agrupamiento de un conjunto de registros en base a ciertas condiciones.
    ### URL:
        > POST http://localhost:11003/transform/group'

    ### Datos que recibe:

    > (__data__) : conjunto de datos.
    
    > (__group__) : lista de nombres de columnas con las que se realizsara el agrupamiento.
    
    > (__variable__) : lista de variables (separadas por ,) a las cuales se les aplicara la funcion de agrupamiento.
    
    > (__group_by__) : funcion de agrupamiento (mean,median, mode,sum, etc).


    ```json 
    {"data":[
        {"Date": "2016-12-06", "Radiation":0.23, "test":-99, "Temperature": 0.7895, "Source": "GCAG"},
        {"Date": "2016-11-06", "Radiation":0.64, "test":-99, "Temperature": 0.7504, "Source": "GCAG"},
        {"Date": "2016-10-06", "Radiation":0.18, "test":35, "Temperature": 0.7292, "Source": "GCAG"},
        {"Date": "2016-05-06", "Radiation":0.73, "test":30, "Temperature": 0.93, "Source": "GISTEMP"},
        {"Date": "2016-04-06", "Radiation":0.65, "test":24, "Temperature": 1.0733, "Source": "GCAG"},
        {"Date": "2016-04-06", "Radiation":0.61, "test":31, "Temperature": 1.09, "Source": "GISTEMP"},
        {"Date": "2016-03-06", "Radiation":0.53, "test":30, "Temperature": 1.2245, "Source": "GCAG"},
        {"Date": "2016-03-06", "Radiation":0.89, "test":11, "Temperature": 1.3, "Source": "GISTEMP"} 
    ],
        "group":['Source','Date'],"variable":"test","group_by":"mean" }
    ```

# TPS de analitica de datos
A continuacion se describen los TPS utilizados para analitica de datos.

## __Summary__  : 
TPS para la obtencion de datos estadisticos programado en lenguaje R, el cual puede ser accedido a traves de peticiones rest. Cuenta con los siguientes servicios:

* _Corrleation_:  Obtiene la varianza, covarianza, y coeficiente de correlacion de un dataset.
    
    ### URL:
    > POST http://localhost:11002/api/v1/correlation
    
    ### Datos que recibe:

    > Parametro(__columns__) : Cadena de texto con los nombres de las variables a caulcuar el coeficiente de correlacion (las variables deben ir separadas por ',' y ser al menos 2) 
    >
    > Parametro(__method__) : Define el metodo de correlacion (pearson, spearman, kendall; pearson por default).
    >
    > __data__: Json en formato de registros con los datos a procesar. e.g:
    ```json 
    {"data":[
    {"Date": "2016-12-06", "Radiation":0.23, "test":34, "Temperature": 0.7895, "Source": "GCAG"},
    {"Date": "2016-11-06", "Radiation":0.64, "test":30, "Temperature": 0.7504, "Source": "GCAG"},
    {"Date": "2016-10-06", "Radiation":0.18, "test":35, "Temperature": 0.7292, "Source": "GCAG"},
    {"Date": "2016-05-06", "Radiation":0.73, "test":30, "Temperature": 0.93, "Source": "GISTEMP"},
    {"Date": "2016-04-06", "Radiation":0.65, "test":24, "Temperature": 1.0733, "Source": "GCAG"},
    {"Date": "2016-04-06", "Radiation":0.61, "test":31, "Temperature": 1.09, "Source": "GISTEMP"},
    {"Date": "2016-03-06", "Radiation":0.53, "test":30, "Temperature": 1.2245, "Source": "GCAG"},
    {"Date": "2016-03-06", "Radiation":0.89, "test":11, "Temperature": 1.3, "Source": "GISTEMP"} 
    ]}
    ```
    ### Ejemplo de respuesta:

    ```json 
    {
        "correlation": {
            "size": 8,
            "variables": "test,Temperature,Radiation",
            "covariance": [
                {
                    "test": 58.6964,
                    "Temperature": -1.2083,
                    "Radiation": -1.4311,
                    "_row": "test"
                },
                {
                    "test": -1.2083,
                    "Temperature": 0.0482,
                    "Radiation": 0.0348,
                    "_row": "Temperature"
                },
                {
                    "test": -1.4311,
                    "Temperature": 0.0348,
                    "Radiation": 0.0584,
                    "_row": "Radiation"
                }
            ],
            "correlation": [
                {
                    "test": 1,
                    "Temperature": -0.7186,
                    "Radiation": -0.7728,
                    "_row": "test"
                },
                {
                    "test": -0.7186,
                    "Temperature": 1,
                    "Radiation": 0.656,
                    "_row": "Temperature"
                },
                {
                    "test": -0.7728,
                    "Temperature": 0.656,
                    "Radiation": 1,
                    "_row": "Radiation"
                }
            ],
            "correlationMethod": "pearson",
            "variance": {
                "test": 58.6964,
                "Temperature": 0.0482,
                "Radiation": 0.0584
            },
            "standarDeviation": {
                "test": 7.6614,
                "Temperature": 0.2195,
                "Radiation": 0.2417
            }
        }
}
    ```


* _Covariance_: Calcula la covarianza de al menos 2 variables dentro de un dataset.

    ### URL:
    > POST http://localhost:11002/api/v1/covariance
    ### Datos que recibe:

    > Parametro(__columns__) : Cadena de texto con los nombres de las variables a calcular la covarianza (las variables deben ir separadas por ',' y ser al menos 2).
    >
    > __data__: Json en formato de registros con los datos a procesar. e.g:
    ```json 
    {"data":[
    {"Date": "2016-12-06", "Radiation":0.23, "test":34, "Temperature": 0.7895, "Source": "GCAG"},
    {"Date": "2016-11-06", "Radiation":0.64, "test":30, "Temperature": 0.7504, "Source": "GCAG"},
    {"Date": "2016-10-06", "Radiation":0.18, "test":35, "Temperature": 0.7292, "Source": "GCAG"},
    {"Date": "2016-05-06", "Radiation":0.73, "test":30, "Temperature": 0.93, "Source": "GISTEMP"},
    {"Date": "2016-04-06", "Radiation":0.65, "test":24, "Temperature": 1.0733, "Source": "GCAG"},
    {"Date": "2016-04-06", "Radiation":0.61, "test":31, "Temperature": 1.09, "Source": "GISTEMP"},
    {"Date": "2016-03-06", "Radiation":0.53, "test":30, "Temperature": 1.2245, "Source": "GCAG"},
    {"Date": "2016-03-06", "Radiation":0.89, "test":11, "Temperature": 1.3, "Source": "GISTEMP"} 
    ]}
    ```
    ### Ejemplo de respuesta:
    ```json 
        {
        "covariance": {
            "len": 3,
            "variables": "test,Temperature,Radiation",
            "result": [
                {
                    "test": 58.6964,
                    "Temperature": -1.2083,
                    "Radiation": -1.4311,
                    "_row": "test"
                },
                {
                    "test": -1.2083,
                    "Temperature": 0.0482,
                    "Radiation": 0.0348,
                    "_row": "Temperature"
                },
                {
                    "test": -1.4311,
                    "Temperature": 0.0348,
                    "Radiation": 0.0584,
                    "_row": "Radiation"
                }
            ],
            "var": {
                "test": 58.6964,
                "Temperature": 0.0482,
                "Radiation": 0.0584
            }
        }
    }
    ```

* _Describe_ : Realiza una descripcion estadistica de un dataset mediante el calculo de medidas de tendencia central.

    ### URL:
    > POST http://localhost:11002/api/v1/describe
    ### Datos que recibe:

    > Parametro(__columns__) (opcional): Cadena de texto con los nombres de las variables a realizar los calculos estadisticos por separado, por default se calcula para todas las columnas numericas (las variables deben ir separadas por ',' y ser al menos 2).
    >
    > __data__: Json en formato de registros con los datos a procesar. e.g:
    ```json 
    {"data":[
    {"Date": "2016-12-06", "Radiation":0.23, "test":34, "Temperature": 0.7895, "Source": "GCAG"},
    {"Date": "2016-11-06", "Radiation":0.64, "test":30, "Temperature": 0.7504, "Source": "GCAG"},
    {"Date": "2016-10-06", "Radiation":0.18, "test":35, "Temperature": 0.7292, "Source": "GCAG"},
    {"Date": "2016-05-06", "Radiation":0.73, "test":30, "Temperature": 0.93, "Source": "GISTEMP"},
    {"Date": "2016-04-06", "Radiation":0.65, "test":24, "Temperature": 1.0733, "Source": "GCAG"},
    {"Date": "2016-04-06", "Radiation":0.61, "test":31, "Temperature": 1.09, "Source": "GISTEMP"},
    {"Date": "2016-03-06", "Radiation":0.53, "test":30, "Temperature": 1.2245, "Source": "GCAG"},
    {"Date": "2016-03-06", "Radiation":0.89, "test":11, "Temperature": 1.3, "Source": "GISTEMP"} 
    ]}
    ```
    ### Ejemplo de respuesta:
    ```json 
    {
        "description": {
            "Radiation": {
                "length": 8,
                "min": 0.18,
                "max": 0.89,
                "mean": 0.5575,
                "median": 0.625,
                "mode": 0.23,
                "range": [
                    0.18,
                    0.89
                ],
                "var": 0.0584,
                "sd": 0.2417,
                "quantile": {
                    "0%": 0.18,
                    "25%": 0.455,
                    "50%": 0.625,
                    "75%": 0.67,
                    "100%": 0.89
                }
            }
        }
    }
    ```
## __Clustering__  
TPS con algoritmos de agrupamiento de datos.

* _Kmeans_ [Presente en dislib] : Realiza el agrupamiento de los datos utilizando el algoritmo kmeans. Se agrega una etiqueta de clase (class) a cada registro.
    ### URL:

    > POST http://localhost:11001/kmeans
    ### Datos que recibe:
    El servicio recibe como entrada un json cons las siguientes caracteristicas:
    > __K__: Numero de grupos (2 por default).
    >
    > __columns__: cadena de texto con las variables a utilizar para el agrupamiento (separadas por ',').
    >
    > __data__: Json en formato de registros con los datos a procesar.
    ```json 
    {
        "K":3,
        "columns":"Temperature",
        "data":[
        {"Date": "2016-12-06", "Radiation":0.23, "test":34, "Temperature": 0.7895, "Source": "GCAG"},
        {"Date": "2016-11-06", "Radiation":0.64, "test":30, "Temperature": 0.7504, "Source": "GCAG"},
        {"Date": "2016-10-06", "Radiation":0.18, "test":35, "Temperature": 0.7292, "Source": "GCAG"},
        {"Date": "2016-05-06", "Radiation":0.73, "test":30, "Temperature": 0.93, "Source": "GISTEMP"},
        {"Date": "2016-04-06", "Radiation":0.65, "test":24, "Temperature": 1.0733, "Source": "GCAG"},
        {"Date": "2016-04-06", "Radiation":0.61, "test":31, "Temperature": 1.09, "Source": "GISTEMP"},
        {"Date": "2016-03-06", "Radiation":0.53, "test":30, "Temperature": 1.2245, "Source": "GCAG"},
        {"Date": "2016-03-06", "Radiation":0.89, "test":11, "Temperature": 1.3, "Source": "GISTEMP"} 
        ]
    }
    ```
    ### Ejemplo de respuesta:
    ```json 
    {"status": "OK", "path": null, 
        "result": [
            {"Date": "2016-12-06", "Radiation": 0.23, "test": 34, "Temperature": 0.7895, "Source": "GCAG", "class": 1},
            {"Date": "2016-11-06", "Radiation": 0.64, "test": 30, "Temperature": 0.7504, "Source": "GCAG", "class": 1},
            {"Date": "2016-10-06", "Radiation": 0.18, "test": 35, "Temperature": 0.7292, "Source": "GCAG", "class": 1},
            {"Date": "2016-05-06", "Radiation": 0.73, "test": 30, "Temperature": 0.93, "Source": "GISTEMP", "class": 0},
            {"Date": "2016-04-06", "Radiation": 0.65, "test": 24, "Temperature": 1.0733, "Source": "GCAG", "class": 0},
            {"Date": "2016-04-06", "Radiation": 0.61, "test": 31, "Temperature": 1.09, "Source": "GISTEMP", "class": 0},
            {"Date": "2016-03-06", "Radiation": 0.53, "test": 30, "Temperature": 1.2245, "Source": "GCAG", "class": 2},
            {"Date": "2016-03-06", "Radiation": 0.89, "test": 11, "Temperature": 1.3, "Source": "GISTEMP", "class": 2}
        ]}
    ```

* _Hierarchical clustering_ : Realiza el agrupamiento de los datos utilizando un algoritmo herarhico.
    ### URL:

    > POST http://localhost:11001/herarhical
    ### Datos que recibe:
    El servicio recibe como entrada un json cons las siguientes caracteristicas:
    > __K__: Numero de grupos (altura del arbol).
    >    
    > __columns__: cadena de texto con las variables a utilizar para el agrupamiento (separadas por ',').
    >
    >__method__: Criterio de vinculación utilizar (ward,complete,average,single). El criterio de vinculación determina qué distancia usar entre conjuntos de observación. El algoritmo fusionará los pares de clúster que minimizan este criterio. 
    >
    >> * _Ward_ minimiza la varianza de los grupos que se fusionan.
    >> * _Average_ usa el promedio de las distancias de cada observación de los dos conjuntos.
    >> * _Complete_ utiliza las distancias máximas entre todas las observaciones de los dos conjuntos.
    >> * _single_ usa el mínimo de las distancias entre todas las observaciones de los dos conjuntos.
    >
    > __index__ (opcional): Agrupa los registros en base a un index. e.g. si index es "DATA" se agrupan todos los registros con un mismo valor de "DATE" y se promedian, obteniendo un unico registro para el agrupamiento.
    >
    > __data__: Json en formato de registros con los datos a procesar.
    ```json 
    {
        "K":3,
        "columns":"Temperature",
        "method":"single",
        "data":[
        {"Date": "2016-12-06", "Radiation":0.23, "test":34, "Temperature": 0.7895, "Source": "GCAG"},
        {"Date": "2016-11-06", "Radiation":0.64, "test":30, "Temperature": 0.7504, "Source": "GCAG"},
        {"Date": "2016-10-06", "Radiation":0.18, "test":35, "Temperature": 0.7292, "Source": "GCAG"},
        {"Date": "2016-05-06", "Radiation":0.73, "test":30, "Temperature": 0.93, "Source": "GISTEMP"},
        {"Date": "2016-04-06", "Radiation":0.65, "test":24, "Temperature": 1.0733, "Source": "GCAG"},
        {"Date": "2016-04-06", "Radiation":0.61, "test":31, "Temperature": 1.09, "Source": "GISTEMP"},
        {"Date": "2016-03-06", "Radiation":0.53, "test":30, "Temperature": 1.2245, "Source": "GCAG"},
        {"Date": "2016-03-06", "Radiation":0.89, "test":11, "Temperature": 1.3, "Source": "GISTEMP"} 
        ]
    }
    ```
    ### Ejemplo de respuesta:
    ```json 
    "status": "OK", "path": null, 
    "result": [
        {"Date": "2016-12-06", "Radiation": 0.23, "test": 34, "Temperature": 0.7895, "Source": "GCAG", "class": 1}, 
        {"Date": "2016-11-06", "Radiation": 0.64, "test": 30, "Temperature": 0.7504, "Source": "GCAG", "class": 1}, 
        {"Date": "2016-10-06", "Radiation": 0.18, "test": 35, "Temperature": 0.7292, "Source": "GCAG", "class": 1}, 
        {"Date": "2016-05-06", "Radiation": 0.73, "test": 30, "Temperature": 0.93, "Source": "GISTEMP", "class": 2}, 
        {"Date": "2016-04-06", "Radiation": 0.65, "test": 24, "Temperature": 1.0733, "Source": "GCAG", "class": 0}, 
        {"Date": "2016-04-06", "Radiation": 0.61, "test": 31, "Temperature": 1.09, "Source": "GISTEMP", "class": 0}, 
        {"Date": "2016-03-06", "Radiation": 0.53, "test": 30, "Temperature": 1.2245, "Source": "GCAG", "class": 0}, 
        {"Date": "2016-03-06", "Radiation": 0.89, "test": 11, "Temperature": 1.3, "Source": "GISTEMP", "class": 0}]
    }
    ```
* _Silhouette_ : Realiza una comparativa entre los algoritmos de kmeans y herarhico con el metodo single, comprobando valores de k de 1 a 15. El resultado de las pruebas se grafica.
    ### URL:

    > POST http://localhost:11001/silhouette
    ### Datos que recibe:
    El servicio recibe como entrada un json cons las siguientes caracteristicas:
   
    > __columns__: cadena de texto con las variables a utilizar para el agrupamiento (separadas por ',').
    >
    > __index__ (opcional): Agrupa los registros en base a un index. e.g. si index es "DATA" se agrupan todos los registros con un mismo valor de "DATE" y se promedian, obteniendo un unico registro para el agrupamiento.
    >
    > __data__: Json en formato de registros con los datos a procesar.
    ```json 
    {
        "K":3,
        "columns":"Temperature",
        "data":[
        {"Date": "2016-12-06", "Radiation":0.23, "test":34, "Temperature": 0.7895, "Source": "GCAG"},
        {"Date": "2016-11-06", "Radiation":0.64, "test":30, "Temperature": 0.7504, "Source": "GCAG"},
        {"Date": "2016-10-06", "Radiation":0.18, "test":35, "Temperature": 0.7292, "Source": "GCAG"},
        {"Date": "2016-05-06", "Radiation":0.73, "test":30, "Temperature": 0.93, "Source": "GISTEMP"},
        {"Date": "2016-04-06", "Radiation":0.65, "test":24, "Temperature": 1.0733, "Source": "GCAG"},
        {"Date": "2016-04-06", "Radiation":0.61, "test":31, "Temperature": 1.09, "Source": "GISTEMP"},
        {"Date": "2016-03-06", "Radiation":0.53, "test":30, "Temperature": 1.2245, "Source": "GCAG"},
        {"Date": "2016-03-06", "Radiation":0.89, "test":11, "Temperature": 1.3, "Source": "GISTEMP"} 
        ]
    }
    ```
    ### Ejemplo de respuesta:
    ```json 
    {"status": "OK", "path": "/static/4483788386721272487.png","winner": "kmeans",
    "result": [
        {"Date": "2016-12-06", "Radiation": 0.23, "test": 34, "Temperature": 0.7895, "Source": "GCAG", "class": 0}, 
        {"Date": "2016-11-06", "Radiation": 0.64, "test": 30, "Temperature": 0.7504, "Source": "GCAG", "class": 0}, 
        {"Date": "2016-10-06", "Radiation": 0.18, "test": 35, "Temperature": 0.7292, "Source": "GCAG", "class": 0}, 
        {"Date": "2016-05-06", "Radiation": 0.73, "test": 30, "Temperature": 0.93, "Source": "GISTEMP", "class": 3}, 
        {"Date": "2016-04-06", "Radiation": 0.65, "test": 24, "Temperature": 1.0733, "Source": "GCAG", "class": 2}, 
        {"Date": "2016-04-06", "Radiation": 0.61, "test": 31, "Temperature": 1.09, "Source": "GISTEMP", "class": 2}, 
        {"Date": "2016-03-06", "Radiation": 0.53, "test": 30, "Temperature": 1.2245, "Source": "GCAG", "class": 1}, 
        {"Date": "2016-03-06", "Radiation": 0.89, "test": 11, "Temperature": 1.3, "Source": "GISTEMP", "class": 1}]}
    ```
    > Para ver la grafica, se utiliza el path que retorna el servicio de la forma:
    >   
    > http://localhost:11001/static/4483788386721272487.png



## __ClusteringTools__  
Herramientas para la validacion de clusters.

* _Validation_ : Realiza la validacion de clusers en base a diferentes indices.

    ### URL:

    > POST http://localhost:3131/api/v1/validation

    ### Datos que recibe:
    
    >__data__ = conjunto de datos.

    >__column__ = columna que tiene las etiquetas de cluster (por default se toma la ultima).
    
    >__indexes__ = lista de indices a calcular, separados por coma. Indices disponibles:  Ball_Hall,Banfeld_Raftery,C_index,Calinski_Harabasz,Davies_Bouldin,Det_Ratio,Dunn8 intCriteria,Gamma,G_plus,GDI11,GDI12,GDI13,GDI21,GDI22,GDI23,GDI31,GDI32,GDI33,GDI41,GDI42,GDI43,GDI51,GDI52,GDI53,Ksq_DetW,Log_Det_Ratio,Log_SS_Ratio,McClain_Rao,PBM,Point_Biserial,Ray_Turi,Ratkowsky_Lance,Scott_Symons,SD_Scat,SD_Dis,S_Dbw,Silhouette,Tau,Trace_W,Trace_WiB,Wemmert_Gancarski,Xie_Beni" 
    
    >__ignore_columns__ = (OPCIONAL) lista de columas a ignorar (separadas por ,)
    ```json
    {"data":[
    {"Date": "2016-12-06", "Radiation":0.23, "test":1, "Temperature": 0.7895, "Source": "GCAG"},
    {"Date": "2016-11-06", "Radiation":0.64, "test":1, "Temperature": 0.7504, "Source": "GCAG"},
    {"Date": "2016-10-06", "Radiation":0.18, "test":2, "Temperature": 0.7292, "Source": "GCAG"},
    {"Date": "2016-05-06", "Radiation":0.73, "test":1, "Temperature": 0.93, "Source": "GISTEMP"},
    {"Date": "2016-04-06", "Radiation":0.65, "test":1, "Temperature": 1.0733, "Source": "GCAG"},
    {"Date": "2016-04-06", "Radiation":0.61, "test":1, "Temperature": 1.09, "Source": "GISTEMP"},
    {"Date": "2016-03-06", "Radiation":0.53, "test":1, "Temperature": 1.2245, "Source": "GCAG"},
    {"Date": "2016-03-06", "Radiation":0.89, "test":2, "Temperature": 1.3, "Source": "GISTEMP"} 
    ],
       "indexes":"Silhouette,Tau,Trace_W","column":"test","ignore_columns":"Date,Source"}
   ```
* _Jaccard_ : Calculo de indice de validacion jaccard para la comparativa de etiquetas de cluster.

    ### URL:

    > POST http://localhost:3131/api/v1/jaccard

    ### Datos que recibe:
    
    >__data__ = conjunto de datos.

    >__columns__ = Lista de columnas con etiquetas de clase (MAX. 2).Por default se seleccionan las 2 ultimas.

    ```json
   {"data":[
    {"Date": "2016-12-06", "Radiation":0.23, "cluster1":1,"cluster2":2, "Temperature": 0.7895, "Source": "GCAG"},
    {"Date": "2016-11-06", "Radiation":0.64, "cluster1":1,"cluster2":2, "Temperature": 0.7504, "Source": "GCAG"},
    {"Date": "2016-10-06", "Radiation":0.18, "cluster1":2,"cluster2":2, "Temperature": 0.7292, "Source": "GCAG"},
    {"Date": "2016-05-06", "Radiation":0.73, "cluster1":1,"cluster2":2, "Temperature": 0.93, "Source": "GISTEMP"},
    {"Date": "2016-04-06", "Radiation":0.65, "cluster1":1,"cluster2":2, "Temperature": 1.0733, "Source": "GCAG"},
    {"Date": "2016-04-06", "Radiation":0.61, "cluster1":1,"cluster2":2, "Temperature": 1.09, "Source": "GISTEMP"},
    {"Date": "2016-03-06", "Radiation":0.53, "cluster1":1,"cluster2":2, "Temperature": 1.2245, "Source": "GCAG"},
    {"Date": "2016-03-06", "Radiation":0.89, "cluster1":2,"cluster2":2, "Temperature": 1.3, "Source": "GISTEMP"} 
    ],"columns":"cluster1,cluster2"}
   ```


## __MLPNN__  
Red neuronal multi capa.

* _training_ : funcion para el entrenamiento de una red neuronal.

    ### URL:

    > POST http://localhost:11004/mlprnn/training

    ### Datos que recibe:
    
    >__data__ = json con el conjunto de datos de entrenamiento (formato: records).
    
    >__params__ = parametros para la red neuronal:    
    > list_var: lista de variables a utilizar.  
    > target: variable objetivo.    
    > test_size: tamaño de la muestra para la validacion (en porcentaje de 0 a 1. e.g. 0.2)
    > max_iter: (DEFAULT 500) cantidad maxima de interaciones.
    > solver: DEFUALT adam 
    > hidden_layer_sizes: (DEFAULT [20,20] )lista con la cantidad de neuronas por capa. e.g. [20,20,20] (tres capas de 20 neuronas)
    > model_tag: (OPCIONAL) Nombre que se le dara al archivo del modelo generado.

    ```json
    {        
        "params":{
            "list_var":["Temperature"],
            "test_size":0.2,
            "target":"test",
            "hidden_layer_sizes":[7,10,7],
        },
        "data":[
        {"Date": "2016-12-06", "Radiation":0.23, "test":34, "Temperature": 0.7895, "Source": "GCAG"},
        {"Date": "2016-11-06", "Radiation":0.64, "test":30, "Temperature": 0.7504, "Source": "GCAG"},
        {"Date": "2016-10-06", "Radiation":0.18, "test":35, "Temperature": 0.7292, "Source": "GCAG"},
        {"Date": "2016-05-06", "Radiation":0.73, "test":30, "Temperature": 0.93, "Source": "GISTEMP"},
        {"Date": "2016-04-06", "Radiation":0.65, "test":24, "Temperature": 1.0733, "Source": "GCAG"},
        {"Date": "2016-04-06", "Radiation":0.61, "test":31, "Temperature": 1.09, "Source": "GISTEMP"},
        {"Date": "2016-03-06", "Radiation":0.53, "test":30, "Temperature": 1.2245, "Source": "GCAG"},
        {"Date": "2016-03-06", "Radiation":0.89, "test":11, "Temperature": 1.3, "Source": "GISTEMP"} 
        ]
    }
* _predict_ : funcion para la clasificacion de un conjunto de datos en base a un modelo ya entrenado.

    ### URL:

    > POST http://localhost:11004/mlprnn/predict

    ### Datos que recibe:
    
    >__data__ = json con el conjunto de datos de entrenamiento (formato: records).
    
    >__params__ = parametros para la red neuronal:    
    > list_var: lista de variables a utilizar.  
    > model_tag: Tag del modelo a utilizar.

    ```json
    {        
        "params":{
            "list_var":["Temperature"],
            "model_tag":"MLPR_NN_model_29074781"
        },
        "data":[
        {"Date": "2016-12-06", "Radiation":0.23, "test":34, "Temperature": 0.7895, "Source": "GCAG"},
        {"Date": "2016-11-06", "Radiation":0.64, "test":30, "Temperature": 0.7504, "Source": "GCAG"},
        {"Date": "2016-10-06", "Radiation":0.18, "test":35, "Temperature": 0.7292, "Source": "GCAG"},
        {"Date": "2016-05-06", "Radiation":0.73, "test":30, "Temperature": 0.93, "Source": "GISTEMP"},
        {"Date": "2016-04-06", "Radiation":0.65, "test":24, "Temperature": 1.0733, "Source": "GCAG"},
        {"Date": "2016-04-06", "Radiation":0.61, "test":31, "Temperature": 1.09, "Source": "GISTEMP"},
        {"Date": "2016-03-06", "Radiation":0.53, "test":30, "Temperature": 1.2245, "Source": "GCAG"},
        {"Date": "2016-03-06", "Radiation":0.89, "test":11, "Temperature": 1.3, "Source": "GISTEMP"} 
        ]
    }

## __graphics__  
Servicio para la generacion de graficas con base a un conjunto de datos.

* _scatter_ : grafica de dispercion.

    ### URL:

    > POST http://localhost:11005/scatter

    ### Datos que recibe:
    
    >__data__ = lista de json con el conjunto de datos (formato: records).
    
    >__variables__ = lista de variables a graficar (MAX. 3) 
    
    > __labels__: (OPCIONAL) lista de etiquetas para asignar color a los puntos.
  
    > __point_label__: (OPCIONAL) lista de etiquetas para asignar un texto a los puntos.  

    ```json
    {        

        "variables":["Temperature","Radiation"],
        "point_label":"Source",
        "data":[
        {"Date": "2016-12-06", "Radiation":0.23, "test":34, "Temperature": 0.7895, "Source": "GCAG"},
        {"Date": "2016-11-06", "Radiation":0.64, "test":30, "Temperature": 0.7504, "Source": "GCAG"},
        {"Date": "2016-10-06", "Radiation":0.18, "test":35, "Temperature": 0.7292, "Source": "GCAG"},
        {"Date": "2016-05-06", "Radiation":0.73, "test":30, "Temperature": 0.93, "Source": "GISTEMP"},
        {"Date": "2016-04-06", "Radiation":0.65, "test":24, "Temperature": 1.0733, "Source": "GCAG"},
        {"Date": "2016-04-06", "Radiation":0.61, "test":31, "Temperature": 1.09, "Source": "GISTEMP"},
        {"Date": "2016-03-06", "Radiation":0.53, "test":30, "Temperature": 1.2245, "Source": "GCAG"},
        {"Date": "2016-03-06", "Radiation":0.89, "test":11, "Temperature": 1.3, "Source": "GISTEMP"} 
        ]
    }
    ```
    ### Resultado:
    nombre del archivo generado. Para acceder a la imagen hay que mandar llamar el servicio _get_images_.
    ```json
    {"status":"ok","file":"scatter_2319_3213_213.jpg"}
    ```
* _line_ : grafica linear.

    ### URL:

    > POST http://localhost:11005/line

    ### Datos que recibe:
    
    >__data__ = lista de json con el conjunto de datos (formato: records).
    
    >__variables__ = lista de variables a graficar (MAX. 3) 
    
    > __labels__: (OPCIONAL) lista de etiquetas para asignar color a las lineas.

    ```json
    {        

        "variables":["Temperature","Radiation"],
        "data":[
        {"Date": "2016-12-06", "Radiation":0.23, "test":34, "Temperature": 0.7895, "Source": "GCAG"},
        {"Date": "2016-11-06", "Radiation":0.64, "test":30, "Temperature": 0.7504, "Source": "GCAG"},
        {"Date": "2016-10-06", "Radiation":0.18, "test":35, "Temperature": 0.7292, "Source": "GCAG"},
        {"Date": "2016-05-06", "Radiation":0.73, "test":30, "Temperature": 0.93, "Source": "GISTEMP"},
        {"Date": "2016-04-06", "Radiation":0.65, "test":24, "Temperature": 1.0733, "Source": "GCAG"},
        {"Date": "2016-04-06", "Radiation":0.61, "test":31, "Temperature": 1.09, "Source": "GISTEMP"},
        {"Date": "2016-03-06", "Radiation":0.53, "test":30, "Temperature": 1.2245, "Source": "GCAG"},
        {"Date": "2016-03-06", "Radiation":0.89, "test":11, "Temperature": 1.3, "Source": "GISTEMP"} 
        ]
    }
    ```
    ### Resultado:
    nombre del archivo generado. Para acceder a la imagen hay que mandar llamar el servicio _get_images_.
    ```json
    {"status":"ok","file":"line_2319_3213_213.jpg"}
    ```
* _bar_ : grafica de barras.

    ### URL:

    > POST http://localhost:11005/bar

    ### Datos que recibe:
    
    >__data__ = lista de json con el conjunto de datos (formato: records).
    
    >__variables__ = lista de variables a graficar (MAX. 3) 
    
    > __labels__: (OPCIONAL) lista de etiquetas para asignar color a las barras.

    ```json
    {        

        "variables":["Temperature","Radiation"],
        "data":[
        {"Date": "2016-12-06", "Radiation":0.23, "test":34, "Temperature": 0.7895, "Source": "GCAG"},
        {"Date": "2016-11-06", "Radiation":0.64, "test":30, "Temperature": 0.7504, "Source": "GCAG"},
        {"Date": "2016-10-06", "Radiation":0.18, "test":35, "Temperature": 0.7292, "Source": "GCAG"},
        {"Date": "2016-05-06", "Radiation":0.73, "test":30, "Temperature": 0.93, "Source": "GISTEMP"},
        {"Date": "2016-04-06", "Radiation":0.65, "test":24, "Temperature": 1.0733, "Source": "GCAG"},
        {"Date": "2016-04-06", "Radiation":0.61, "test":31, "Temperature": 1.09, "Source": "GISTEMP"},
        {"Date": "2016-03-06", "Radiation":0.53, "test":30, "Temperature": 1.2245, "Source": "GCAG"},
        {"Date": "2016-03-06", "Radiation":0.89, "test":11, "Temperature": 1.3, "Source": "GISTEMP"} 
        ]
    }
    ```
    ### Resultado:
    nombre del archivo generado. Para acceder a la imagen hay que mandar llamar el servicio _get_images_.
    ```json
    {"status":"ok","file":"bar_2319_3213_213.jpg"}
    ```
* _hist_ : histograma.

    ### URL:

    > POST http://localhost:11005/bar

    ### Datos que recibe:
    
    >__data__ = lista de json con el conjunto de datos (formato: records).
    
    >__variables__ = lista de variables a graficar.

    > __alpha__: (OPCIONAL) Tamaño de las barras en porcentaje 0 a 1. e.g. 0.25

    > __bins__: (OPCIONAL) cantidad de barras, no mayor al numero de registros.


    ```json
    {        

        "variables":["Temperature","Radiation"],
        "bins":20,
        "data":[
        {"Date": "2016-12-06", "Radiation":0.23, "test":34, "Temperature": 0.7895, "Source": "GCAG"},
        {"Date": "2016-11-06", "Radiation":0.64, "test":30, "Temperature": 0.7504, "Source": "GCAG"},
        {"Date": "2016-10-06", "Radiation":0.18, "test":35, "Temperature": 0.7292, "Source": "GCAG"},
        {"Date": "2016-05-06", "Radiation":0.73, "test":30, "Temperature": 0.93, "Source": "GISTEMP"},
        {"Date": "2016-04-06", "Radiation":0.65, "test":24, "Temperature": 1.0733, "Source": "GCAG"},
        {"Date": "2016-04-06", "Radiation":0.61, "test":31, "Temperature": 1.09, "Source": "GISTEMP"},
        {"Date": "2016-03-06", "Radiation":0.53, "test":30, "Temperature": 1.2245, "Source": "GCAG"},
        {"Date": "2016-03-06", "Radiation":0.89, "test":11, "Temperature": 1.3, "Source": "GISTEMP"} 
        ]
    }
    ```
    ### Resultado:
    nombre del archivo generado. Para acceder a la imagen hay que mandar llamar el servicio _get_images_.
    ```json
    {"status":"ok","file":"hist_2319_3213_213.jpg"}
    ```

* _get_images_ : Descarga de imagenes.

    ### URL:

    > GET http://localhost:11005/<_file_>

    ### Datos que recibe:
    
    >_file_ = identificador o nombre de la imagen a descargar.
    
    ### Resultado:
    Archivo solicitado.