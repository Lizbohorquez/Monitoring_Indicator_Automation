import os

from data.remote.grafana import Grafana
from data.remote.aws import CloudWatch, AWS_METRIC_NAMES
from datetime import datetime, timedelta
from dashboard import Dashboard

grafana_url = os.getenv('GRAFANA_URL')
grafana_token = os.getenv('GRAFANA_TOKEN')


class Score:
    """
    This class represents the Score module, which is responsible for calculating different scores related to
    monitoring and service quality.
    """
    tags = ['ApiGateway', 'CloudFront', 'ECS', 'Lambda', 'NetworkELB', 'RDS']
    infra_score = 0
    proactive_score = 0
    realtime_score = 0
    total_score = 0

    def __init__(self, org_name):
        """
        Initializes an instance of the Score class.
        Param org_name: The name of the organization for which the infrastructure score will be calculated.
        """
        self.cloudwatch = CloudWatch()
        self.grafana = Grafana(grafana_url, grafana_token)
        self.org_name = org_name

    # 0 - 100 grade range
    def get_dashboard_score(self, resource, uid):
        """
        Calculates the score (0-100) for a specific dashboard in Grafana based on its panels and associated
        AWS CloudWatch metrics.
        Param resource: The resource type associated with the dashboard (e.g., 'RDS', 'ApiGateway', 'ECS').
        Param uid: The unique identifier (UID) of the dashboard in Grafana.
        Return: The calculated score for the dashboard (currently a placeholder, always returns 100).
        """
        score = 0
        dash = self.grafana.get_dashboard(uid).json()['dashboard']
        panels = dash['panels']
        template = dash['templating']
        start_time = datetime.now() - timedelta(minutes=20)
        end_time = datetime.now()
        if resource in ['RDS', 'ApiGateway', 'ECS']:
            for panel in panels:
                try:
                    if 'targets' in panel:
                        target = panel['targets'][0]
                        metric_name = target['metricName']
                        if metric_name not in AWS_METRIC_NAMES:
                            continue
                        namespace = target['namespace']
                        statistic = [target['statistic']]
                        # dimensions = target['dimensions']
                        # if target['period']
                        period = 60 * 5 if target['period'] == '' else int(target['period'])
                        print(metric_name, namespace, statistic, period)
                        response = self.cloudwatch.get_query(
                            namespace=namespace,
                            metric_name=metric_name,
                            # dimensions=dimensions,
                            start_time=start_time,
                            end_time=end_time,
                            period=period,
                            statistic=statistic
                        )
                        # print(response)
                except:
                    pass

        return 100

    def get_infra_score(self):
        """
        Calculates the infrastructure score for the organization.
        Return: The calculated infrastructure score (0-100) related to monitored services.
        """
        folders = dict()
        grafana_services = dict()
        dashboard = Dashboard(cloudwatch=self.cloudwatch, grafana=self.grafana)
        for i in self.grafana.list_folders().json():
            folders[i['title']] = i['id']
        # get dashboards in grafana
        dashboards = self.grafana.list_dashboards(folders[self.org_name]).json()
        monitored_services = [i for i in dashboards if
                              len(set(self.tags).intersection(i for i in i['tags'])) > 0]
        for service in monitored_services:
            uid = service['uid']
            resource = list(dict.fromkeys(set(self.tags).intersection(service['tags'])))[0]
            grafana_services[resource] = {'uid': uid, 'score': dashboard.get_score(resource, uid)}
        print(grafana_services)
        monitored_score = sum(i[1]['score'] for i in grafana_services.items())
        aws_services = [serv.replace('AWS/', '') for serv in list(dict.fromkeys(self.cloudwatch.get_services()))]
        self.infra_score = monitored_score / len(aws_services)

        return self.infra_score

    def get_proactive_score(self):
        """
        Returns the proactive score (currently a placeholder).
        Return: The calculated proactive score (0-100) related to proactive monitoring.
        """
        return self.proactive_score

    def get_realtime_score(self):
        """
        Returns the real-time score (currently a placeholder).
        Return: The calculated real-time score (0-100) related to real-time monitoring.
        """
        return self.realtime_score

    def calc_total_score(self):
        """
        Calculates the total score (currently a placeholder).
        Return: The calculated total score (0-100) combining different scores.
        """
        return self.total_score
