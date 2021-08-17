import opsgenie_sdk
from pprint import pprint
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
            pprint(list_response)
            return list_response
        except ApiException as err:
            print("Exception when calling AlertApi->list_alerts: %s\n" % err)

    def count_alerts(self):
        try:
            count_response = self.alert_api.count_alerts()
            pprint(count_response)
            return count_response
        except ApiException as err:
            print("Exception when calling AlertApi->count__alerts: %s\n" % err)


a=Alert('3b5d25f3-8983-48ff-9154-137b6ac0a23d')
a.list_alerts()
a.count_alerts()