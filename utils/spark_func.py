# coding: utf-8
__author__ = 'ila'

import json

from flask import current_app as app
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.sql import SparkSession


def spark_read_mysql(sql, json_filename):
    '''
    排序
    :param sql:
    :param json_filename:
    :return:
    '''
    df = app.spark.read.format("jdbc").options(url=app.jdbc_url,
                                               dbtable=sql).load()
    count = df.count()
    df_data = df.toPandas().to_dict()
    json_data = []
    for i in range(count):
        temp = {}
        for k, v in df_data.items():
            temp[k] = v.get(i)
        json_data.append(temp)
    with open(json_filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(json_data, indent=4, ensure_ascii=False))


def linear(table_name):
    '''
    回归
    :param table_name:
    :return:
    '''

    spark = SparkSession.builder.appName("flask").getOrCreate()

    training = spark.read.format("libsvm").table(table_name)

    lr = LinearRegression(maxIter=20, regParam=0.01, elasticNetParam=0.6)
    lrModel = lr.fit(training)

    trainingSummary = lrModel.summary
    print("numIterations: %d" % trainingSummary.totalIterations)
    print("objectiveHistory: %s" % str(trainingSummary.objectiveHistory))
    trainingSummary.residuals.show()
    print("RMSE: %f" % trainingSummary.rootMeanSquaredError)
    print("r2: %f" % trainingSummary.r2)

    result = trainingSummary.residuals.toJSON()
    spark.stop()
    return result


def cluster(table_name):
    '''
    聚类
    :param table_name:
    :return:
    '''

    spark = SparkSession.builder.appName("flask").getOrCreate()
    dataset = spark.read.format("libsvm").table(table_name)

    kmeans = KMeans().setK(2).setSeed(1)
    model = kmeans.fit(dataset)

    centers = model.clusterCenters()
    for center in centers:
        print(center)

    return centers


def selector(table_name, Cols):
    '''
    分类
    :return:
    '''
    spark = SparkSession.builder.appName("flask").getOrCreate()

    data = spark.read.table(table_name)

    assembler = VectorAssembler(inputCols=Cols, outputCol="features")
    data = assembler.transform(data).select("features", "label")

    train_data, test_data = data.randomSplit([0.7, 0.3], seed=0)

    lr = LogisticRegression(featuresCol="features", labelCol="label")

    model = lr.fit(train_data)

    predictions = model.transform(test_data)

    return predictions.toJSON()
