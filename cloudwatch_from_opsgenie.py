import opsgenie_sdk
import boto3
import json
from datetime import datetime, timedelta
class Alert:
    def __init__(self, opsgenie_api_key):
        self.conf = self.conf = opsgenie_sdk.configuration.Configuration()
        self.conf.api_key['Authorization'] = opsgenie_api_key

        self.api_client = opsgenie_sdk.api_client.ApiClient(configuration=self.conf)
        self.alert_api = opsgenie_sdk.AlertApi(api_client=self.api_client)

    def list_alerts(self):
        query = 'status=open'
        try:
            list_response = self.alert_api.list_alerts(query=query)
            return list_response
        except ApiException as err:
            print("Exception when calling AlertApi->list_alerts: %s\n" % err)

    def alert_tags(self):
        query = 'status=open'
        try:
            list_response = self.alert_api.list_alerts(query=query,sort='createdAt',order='asc')
            for alert_response in list_response.data:
                return alert_response.tags
        except ApiException as err:
            print("Exception when calling AlertApi->list_alerts: %s\n" % err)


def cloudwatch_metrics(Namespace,MetricName,InstanceId_Values):
    client = boto3.client('cloudwatch')
    response = client.get_metric_statistics(
        Namespace=Namespace,
        MetricName=MetricName,
        Dimensions=[{'Name': 'InstanceId', 'Value': InstanceId_Values}],
        StartTime=datetime.utcnow() - timedelta(minutes=10),
        EndTime=datetime.utcnow(),
        Period=60,
        Statistics=['Average'],
    )
    for cpu in response['Datapoints']:
        print(Namespace,MetricName,cpu)

#getting tags from opsgenie alerts
a=Alert('3b5d25f3-8983-48ff-9154-137b6ac0a23d')
tags=a.alert_tags()

#filtering instance id from tags
InstanceId_Values=""
for id in tags:
    if len(id)==19 and id[0]=='i':
        InstanceId_Values+=id
        break

#Importing json metric
with open('metric_json.json','r') as file:
    metrics = json.load(file)

#printing metrics
print(f"InstanceID is {InstanceId_Values}")
for Namespace in metrics.keys():
    for MetricName in metrics[Namespace]:
        cloudwatch_metrics(Namespace,MetricName,InstanceId_Values)