# 🏥 Análisis de Salud Global con Apache Spark — Tarea 3

Script de procesamiento batch desarrollado con **PySpark** que analiza un dataset de salud global (`Health.csv`) almacenado en HDFS. El pipeline cubre limpieza de datos, análisis exploratorio, uso de RDDs y tres consultas analíticas sobre enfermedades, países y evolución temporal.

---

## 📋 Descripción de la Solución

El script implementa un pipeline completo de procesamiento de datos en las siguientes etapas:

| Etapa | Descripción |
|-------|-------------|
| **1. Inicialización** | Crea una `SparkSession` con el nombre `AnalisisSalud_Tarea3` |
| **2. Carga (Batch)** | Lee `Health.csv` desde HDFS con inferencia de esquema automática |
| **3. Limpieza** | Elimina nulos, duplicados y castea columnas de tasas a `FloatType` |
| **4. EDA** | Resumen estadístico de variables clave y países únicos |
| **5. RDD** | Conteo de registros por género usando transformaciones RDD (`map` + `reduceByKey`) |
| **6. Consultas Batch** | Tres consultas analíticas con `groupBy`, `agg`, `orderBy` |

### Consultas implementadas

- **Consulta 1 — Población afectada por país:** Agrupa y suma `Population Affected` por `Country`, ordenado de mayor a menor.
- **Consulta 2 — Evolución temporal por enfermedad:** Calcula la incidencia media (`Incidence Rate (%)`) agrupada por `Year` y `Disease Name`.
- **Consulta 3 — Mortalidad vs. Recuperación anual:** Compara año a año las medias de `Mortality Rate (%)` y `Recovery Rate (%)`.

---

## 🗂️ Estructura esperada del dataset

El archivo `Health.csv` debe contener al menos las siguientes columnas:

| Columna | Tipo |
|---------|------|
| `Country` | String |
| `Year` | Integer |
| `Disease Name` | String |
| `Gender` | String |
| `Population Affected` | Integer / Long |
| `Incidence Rate (%)` | Float |
| `Mortality Rate (%)` | Float |
| `Recovery Rate (%)` | Float |

---

## ⚙️ Requisitos

- **Apache Hadoop** ≥ 3.x (HDFS activo en `hdfs://localhost:9000`)
- **Apache Spark** ≥ 3.x
- **Python** ≥ 3.8
- **PySpark** instalado y configurado (`SPARK_HOME` en el PATH)
- El archivo `Health.csv` subido a HDFS en la ruta `/Tarea3/Health.csv`

---

## 🚀 Instrucciones de Ejecución

### 1. Verificar que HDFS esté activo

```bash
# Iniciar los servicios de Hadoop si no están corriendo
start-dfs.sh
start-yarn.sh

# Comprobar que el namenode está disponible
hdfs dfsadmin -report
```

### 2. Subir el dataset a HDFS

```bash
# Crear el directorio en HDFS (si no existe)
hdfs dfs -mkdir -p /Tarea3

# Copiar el archivo CSV desde el sistema local
hdfs dfs -put /ruta/local/Health.csv /Tarea3/Health.csv

# Verificar que el archivo fue subido correctamente
hdfs dfs -ls /Tarea3/
```

### 3. Ejecutar el script con spark-submit

```bash
spark-submit \
  --master local[*] \
  analisis_salud.py
```

> **Nota:** Reemplaza `local[*]` por la URL de tu cluster si ejecutas en modo distribuido (p. ej. `yarn` o `spark://master:7077`).

### 4. Ejecución en clúster con YARN (opcional)

```bash
spark-submit \
  --master yarn \
  --deploy-mode client \
  --num-executors 2 \
  --executor-memory 2g \
  --executor-cores 2 \
  analisis_salud.py
```

---

## 📤 Salida esperada

Al ejecutarse correctamente, el script imprime en consola:

```
--- Estructura Original del Dataset ---
root
 |-- Country: string ...
 ...

Registros originales: XXXX | Registros tras limpieza: YYYY

--- Resumen Estadístico de Variables Clave ---
...

Países únicos en el estudio:
...

Conteo por género (Calculado con RDD):
[('Male', N), ('Female', M), ...]

--- Consulta 1: Población total afectada por país ---
...

--- Consulta 2: Evolución de la incidencia media por enfermedad y año ---
...

--- Consulta 3: Comparativa anual de Mortalidad vs Recuperación ---
...
```

---
