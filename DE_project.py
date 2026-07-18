# Databricks notebook source
# DBTITLE 1,import
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import pandas as pd
import numpy as np


# COMMAND ----------

spark = SparkSession.builder.appName("Pizza_sales").getOrCreate()
df = spark.read.csv("/Workspace/Users/haripriya13divi@gmail.com/DE_project_pizza/pizzanew.csv", header=True, inferSchema=True)
display(df)
df.printSchema()

# COMMAND ----------

# DBTITLE 1,Create or view
# Create temporary view from DataFrame first
df.createOrReplaceTempView("Pizza_sales")


# COMMAND ----------

# MAGIC %sql
# MAGIC select * from Pizza_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC select
# MAGIC order_id,
# MAGIC quantity,
# MAGIC date_format(order_date, 'MMM') as month_name,
# MAGIC date_format(order_date, 'EEEE') as day_name,
# MAGIC hour(order_time) as hour,
# MAGIC unit_price,
# MAGIC total_price
# MAGIC from Pizza_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC select  pizza_name,pizza_category,order_id,sum(total_price) as max_price 
# MAGIC from Pizza_sales 
# MAGIC group by order_id ,pizza_category, pizza_name order by max_price desc 
# MAGIC     
# MAGIC

# COMMAND ----------

# DBTITLE 1,Requirement 1: Identify the crowd favourite
# MAGIC %sql
# MAGIC
# MAGIC select pizza_category,sum(quantity) as total_order from Pizza_sales group by pizza_category order by total_order desc limit 1
# MAGIC

# COMMAND ----------

# DBTITLE 1,Management wants to know if they should discontinue the 'Small' size or push more 'Large' sizes.
# MAGIC %sql
# MAGIC select pizza_size, sum(total_price) as total_revenue from Pizza_sales group by pizza_size order by total_revenue asc 

# COMMAND ----------

# DBTITLE 1,Requirement 3: Find the largest single transaction
# MAGIC %sql
# MAGIC select order_id,sum(total_price) as total_spend from Pizza_sales group by order_id order by total_spend desc limit 1

# COMMAND ----------

# DBTITLE 1,Requirement 4: Analyze peak rush hour
# MAGIC %sql select  hour(order_time) as time_cal, sum(quantity) as total_orders from Pizza_sales group by time_cal order by total_orders desc

# COMMAND ----------

# DBTITLE 1,Requirement 5: Identify the "Low-Margin" items
# MAGIC %sql
# MAGIC select pizza_name,
# MAGIC sum(quantity) as total_sold ,
# MAGIC unit_price ,
# MAGIC pizza_size 
# MAGIC from Pizza_sales 
# MAGIC group by pizza_name, 
# MAGIC unit_price, 
# MAGIC pizza_size order by total_sold desc limit 5

# COMMAND ----------

# DBTITLE 1,Requirement 6: Uncover ingredient trends
# MAGIC %sql
# MAGIC SELECT 
# MAGIC     pizza_name, 
# MAGIC     SUM(total_price) AS total_revenue
# MAGIC FROM Pizza_sales
# MAGIC WHERE pizza_name LIKE '%Chicken%' 
# MAGIC GROUP BY pizza_name
# MAGIC ORDER BY total_revenue DESC;
# MAGIC