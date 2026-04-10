# Importamos librerías necesarias 
from pyspark.sql import SparkSession, functions as F 
from pyspark.sql.types import FloatType

# Inicializa la sesión de Spark 
spark = SparkSession.builder.appName('AnalisisSalud').getOrCreate() 

# Define la ruta del archivo
file_path = 'hdfs://localhost:9000/Tarea3/Health.csv' 

# Lee el archivo .csv
df = spark.read.format('csv') \
    .option('header', 'true') \
    .option('inferSchema', 'true') \
    .load(file_path) 

# Imprimimos el esquema
df.printSchema() 

# Limpieza de datos
df_clean = df.na.drop().dropDuplicates()
for col in columnas_numericas:
    df_clean = df_clean.withColumn(col, F.col(f"`{col}`").cast(FloatType()))
print(f"Registros originales: {df.count()} | Registros tras limpieza: {df_clean.count()}")

# 1. Análisis de casos por región (País)
print("Consulta 1: Total de población afectada por país (Región)")
casos_por_region = df.groupBy("Country") \
    .agg(F.sum("Population Affected").alias("Total_Afectados")) \
    .orderBy(F.col("Total_Afectados").desc())
casos_por_region.show()

# 2. Evolución temporal de las enfermedades
print("Consulta 2: Evolución de la tasa de incidencia por enfermedad y año")
evolucion_enfermedades = df.groupBy("Year", "Disease Name") \
    .agg(F.avg("Incidence Rate (%)").alias("Media_Incidencia")) \
    .orderBy("Year", "Disease Name")
evolucion_enfermedades.show()

# 3. Comparación de eventos de salud entre diferentes años
print("Consulta 3: Comparativa anual de Mortalidad y Recuperación")
comparativa_anual = df.groupBy("Year") \
    .agg(
        F.avg("Mortality Rate (%)").alias("Mortalidad_Promedio"),
        F.avg("Recovery Rate (%)").alias("Recuperacion_Promedio")
    ).orderBy("Year")
comparativa_anual.show()

# Estadísticas básicas generales del dataset
print("Resumen estadístico general:")
df.summary().show()