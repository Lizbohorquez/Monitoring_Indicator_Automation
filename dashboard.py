from datetime import datetime, timedelta

from data.remote.aws import AWS_METRIC_NAMES


class Dashboard:
    """
    This class represents a dashboard in Grafana and is responsible for calculating its score.
    """
    tags = ['ApiGateway', 'CloudFront', 'ECS', 'Lambda', 'NetworkELB', 'RDS']

    def __init__(self, cloudwatch, grafana):
        """
        Initializes an instance of the Dashboard class.
        Param cloudwatch: An instance of the CloudWatch class for interacting with AWS CloudWatch.
        Param grafana: An instance of the Grafana class for interacting with Grafana.
        """
        self.cloudwatch = cloudwatch
        self.grafana = grafana

    def get_panels(self, uid):
        """
        Retrieves the panels of a dashboard based on its unique identifier (UID) in Grafana.
        Param uid: The unique identifier of the dashboard in Grafana.
        Return: A list of panels in the dashboard.
        """
        dash = self.grafana.get_dashboard(uid).json()['dashboard']
        return dash['panels']

    def get_score(self, resource, uid):
        """
        Calculates the score for a specific dashboard in Grafana.
        Param resource: The resource type associated with the dashboard (e.g., 'ApiGateway', 'ECS').
        Param uid: The unique identifier of the dashboard in Grafana.
        Return: The calculated score (currently a placeholder, always returns 100).
        """
        panels = self.get_panels(uid)
        start_time = datetime.now() - timedelta(hours=3)
        end_time = datetime.now()
        dimensions = []

        if resource in ['ApiGateway', 'ECS']:
            dimensions = self.cloudwatch.get_dimensions(resource)
            if not isinstance(dimensions, list):
                dimensions = []
            else:
                dimensions = dimensions[0]

        for panel in panels:
            try:
                if 'targets' in panel:
                    target = panel['targets'][0]
                    metric_name = target['metricName']
                    namespace = target['namespace']
                    statistic = [target['statistic']]
                    period = 60 * 5 if target['period'] == '' else int(target['period'])
                    if metric_name not in AWS_METRIC_NAMES:
                        continue
                    print(metric_name, namespace, statistic, period)
                    datapoints = self.cloudwatch.get_query(
                        namespace=namespace,
                        metric_name=metric_name,
                        dimensions=dimensions,
                        start_time=start_time,
                        end_time=end_time,
                        period=period,
                        statistic=statistic
                    )
                    print(namespace, datapoints)
            except:
                print(f"Error grading {panel}")
        return 100
