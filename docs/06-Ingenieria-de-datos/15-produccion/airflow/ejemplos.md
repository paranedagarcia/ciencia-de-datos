---
id: airflow-ejemplos
title: "Ejemplos de Airflow"
sidebar_label: "Ejemplos"
description: "Ejemplos de uso práctico de Airflow"
---




### Ejemplo 1: DAG ETL completo 
**(Extract → Transform → Load → Checks → Notify)**

```python showLineNumbers
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator

default_args = {
    "owner": "data-team",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

def extract(**context):
    # Simulación: bajar datos desde API
    raw_path = "/tmp/raw_sales.json"
    with open(raw_path, "w") as f:
        f.write('{"status":"ok","rows":123}')
    context["ti"].xcom_push(key="raw_path", value=raw_path)

def transform(**context):
    raw_path = context["ti"].xcom_pull(key="raw_path")
    processed_path = "/tmp/sales_clean.parquet"
    # Simulación: transformar
    with open(processed_path, "w") as f:
        f.write("processed")
    context["ti"].xcom_push(key="processed_path", value=processed_path)

def load(**context):
    processed_path = context["ti"].xcom_pull(key="processed_path")
    # Simulación: cargar a DWH
    print(f"Loading {processed_path} to warehouse...")

def quality_checks():
    # Simulación: chequeo
    rows_loaded = 123
    if rows_loaded <= 0:
        raise ValueError("No rows loaded!")

with DAG(
    dag_id="etl_sales_daily",
    start_date=datetime(2025, 1, 1),
    schedule="0 2 * * *",   # 02:00 AM
    catchup=False,
    default_args=default_args,
    tags=["etl", "sales"],
) as dag:

    t1 = PythonOperator(task_id="extract", python_callable=extract)
    t2 = PythonOperator(task_id="transform", python_callable=transform)
    t3 = PythonOperator(task_id="load", python_callable=load)
    t4 = PythonOperator(task_id="quality_checks", python_callable=quality_checks)

    notify = EmailOperator(
        task_id="notify_success",
        to="dataops@company.com",
        subject="ETL Sales OK",
        html_content="Pipeline completed successfully."
    )

    t1 >> t2 >> t3 >> t4 >> notify
```

**Qué muestra este ejemplo**

- DAG diario a las 02:00
- Reintentos y delay
- XCom para pasar paths
- Dependencias lineales
- Notificación final

### Ejemplo 2: Branching 
**(si no hay datos, no cargues)**

```python showLineNumbers
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator

def decide_branch(**context):
    n = 0  # simula cantidad de registros
    return "load" if n > 0 else "skip_load"

branch = BranchPythonOperator(
    task_id="branch_decision",
    python_callable=decide_branch
)

load = PythonOperator(task_id="load", python_callable=lambda: print("Loading..."))
skip = EmptyOperator(task_id="skip_load")

branch >> [load, skip]
```

#### Escenario: Pipeline de Procesamiento de Datos de Ventas

```python showLineNumbers
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.email_operator import EmailOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import pandas as pd
import logging

# Configuración del DAG
default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': ['alerts@company.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'max_active_runs': 1,
}

dag = DAG(
    'sales_data_pipeline',
    default_args=default_args,
    description='Pipeline diario de procesamiento de datos de ventas',
    schedule_interval='0 2 * * *',  # 2 AM diariamente
    catchup=False,
    tags=['sales', 'etl', 'production'],
)

# 1. Extracción de datos desde PostgreSQL
def extract_sales_data(**context):
    """Extrae datos de ventas del día anterior"""
    execution_date = context['execution_date']
    previous_day = execution_date - timedelta(days=1)
    
    hook = PostgresHook(postgres_conn_id='production_db')
    sql = f"""
        SELECT 
            order_id,
            customer_id,
            product_id,
            quantity,
            amount,
            order_date
        FROM sales
        WHERE DATE(order_date) = '{previous_day.strftime("%Y-%m-%d")}'
    """
    
    df = hook.get_pandas_df(sql)
    
    # Guardar datos extraídos temporalmente
    file_path = f'/tmp/sales_{previous_day.strftime("%Y%m%d")}.csv'
    df.to_csv(file_path, index=False)
    
    # Pasar la ruta del archivo al siguiente task
    context['ti'].xcom_push(key='extracted_file', value=file_path)
    
    logging.info(f'Extraídos {len(df)} registros de ventas')
    return file_path

# 2. Transformación de datos
def transform_sales_data(**context):
    """Aplica transformaciones y enriquecimiento de datos"""
    ti = context['ti']
    input_file = ti.xcom_pull(task_ids='extract_data', key='extracted_file')
    
    # Leer datos
    df = pd.read_csv(input_file)
    
    # Aplicar transformaciones
    df['amount_usd'] = df['amount'] * 1.1  # Conversión a USD
    df['order_month'] = pd.to_datetime(df['order_date']).dt.month
    df['order_weekday'] = pd.to_datetime(df['order_date']).dt.day_name()
    
    # Calcular métricas agregadas
    daily_summary = df.groupby('product_id').agg({
        'quantity': 'sum',
        'amount_usd': 'sum'
    }).reset_index()
    
    # Guardar resultados transformados
    output_file = f'/tmp/sales_transformed_{datetime.now().strftime("%Y%m%d")}.csv'
    daily_summary.to_csv(output_file, index=False)
    
    # Subir a S3
    s3_hook = S3Hook(aws_conn_id='aws_default')
    s3_key = f'sales-transformed/{datetime.now().strftime("%Y/%m/%d")}/daily_summary.csv'
    s3_hook.load_file(
        filename=output_file,
        key=s3_key,
        bucket_name='company-data-lake',
        replace=True
    )
    
    context['ti'].xcom_push(key='transformed_s3_key', value=s3_key)
    return output_file

# 3. Carga a Data Warehouse
def load_to_warehouse(**context):
    """Carga datos transformados a Redshift"""
    ti = context['ti']
    s3_key = ti.xcom_pull(task_ids='transform_data', key='transformed_s3_key')
    
    copy_sql = f"""
        COPY sales_daily_summary
        FROM 's3://company-data-lake/{s3_key}'
        IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftCopyRole'
        FORMAT AS CSV
        DELIMITER ','
        IGNOREHEADER 1
        TIMEFORMAT 'auto'
    """
    
    redshift_hook = PostgresHook(postgres_conn_id='redshift_dw')
    redshift_hook.run(copy_sql)
    
    logging.info('Datos cargados exitosamente a Redshift')

# 4. Generación de reporte
def generate_daily_report(**context):
    """Genera reporte diario de métricas clave"""
    ti = context['ti']
    s3_key = ti.xcom_pull(task_ids='transform_data', key='transformed_s3_key')
    
    s3_hook = S3Hook(aws_conn_id='aws_default')
    file_content = s3_hook.read_key(
        key=s3_key,
        bucket_name='company-data-lake'
    )
    
    # Generar HTML report
    html_content = f"""
    <html>
    <body>
        <h1>Reporte Diario de Ventas</h1>
        <p>Fecha: {context['execution_date'].strftime('%Y-%m-%d')}</p>
        <pre>{file_content}</pre>
    </body>
    </html>
    """
    
    context['ti'].xcom_push(key='report_html', value=html_content)
    return html_content

# 5. Validación de calidad de datos
def validate_data_quality(**context):
    """Ejecuta validaciones de calidad de datos"""
    validation_checks = [
        BashOperator(
            task_id=f'validation_{i}',
            bash_command=f'python /scripts/validate_{i}.py',
            dag=dag
        )
        for i in range(1, 4)
    ]
    return validation_checks

# Definición de Tasks
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_sales_data,
    provide_context=True,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_sales_data,
    provide_context=True,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_to_warehouse,
    provide_context=True,
    dag=dag,
)

report_task = PythonOperator(
    task_id='generate_report',
    python_callable=generate_daily_report,
    provide_context=True,
    dag=dag,
)

notification_task = EmailOperator(
    task_id='send_daily_report',
    to='sales-team@company.com',
    subject='Reporte Diario de Ventas - {{ ds }}',
    html_content="{{ ti.xcom_pull(task_ids='generate_report', key='report_html') }}",
    dag=dag,
)

cleanup_task = BashOperator(
    task_id='cleanup_temporary_files',
    bash_command='rm -f /tmp/sales_*.csv',
    dag=dag,
)

# Definición de dependencias
extract_task >> transform_task >> load_task
transform_task >> report_task >> notification_task
load_task >> cleanup_task

# Branching condicional
def check_data_volume(**context):
    """Decide si ejecutar validaciones basado en volumen de datos"""
    ti = context['ti']
    file_path = ti.xcom_pull(task_ids='extract_data')
    
    df = pd.read_csv(file_path)
    if len(df) > 1000:
        return 'run_full_validations'
    else:
        return 'run_basic_validations'

branch_task = BranchPythonOperator(
    task_id='check_volume',
    python_callable=check_data_volume,
    provide_context=True,
    dag=dag,
)

basic_val_task = PythonOperator(
    task_id='run_basic_validations',
    python_callable=lambda: print('Running basic validations'),
    dag=dag,
)

full_val_task = PythonOperator(
    task_id='run_full_validations',
    python_callable=lambda: print('Running full validations'),
    dag=dag,
)

extract_task >> branch_task >> [basic_val_task, full_val_task] >> transform_task
```
**Estructura de DAG Resultante:**

```raw
                          extract_data
                                │
                                ▼
                          check_volume
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
         run_basic_validations   run_full_validations
                    └───────────┬───────────┘
                                ▼
                         transform_data
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
               load_data              generate_report
                    │                       │
                    ▼                       ▼
            cleanup_temporary_files   send_daily_report
```