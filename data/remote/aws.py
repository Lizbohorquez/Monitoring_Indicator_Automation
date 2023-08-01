import boto3

AWS_METRIC_NAMES = ['CPUUtilization', 'HealthyHostCount', 'DatabaseConnections', 'Requests', '4XXError', '5XXError',
                    'Invocations', 'ProcessedBytes', 'Count']
AWS_NAMESPACES = ["AWS/ApiGateway", "AWS/RDS", "AWS/NetworkELB", "AWS/CloudFront", "AWS/ECS", "AWS/Lambda"]


class CloudWatch:
    """
    This class provides methods to interact with AWS CloudWatch and retrieve metrics data.
    Attributes:
    - cloudwatch: The boto3 CloudWatch client for making API calls to AWS CloudWatch.
    """

    def __init__(self):
        """
        Initializes the CloudWatch client using boto3.
        """
        self.cloudwatch = boto3.client('cloudwatch')

    def get_services(self):
        """
        Returns a list of AWS services that have metrics with names in AWS_METRIC_NAMES.
        Return: A list of AWS service names.
        """
        services = list()
        cloudwatch = self.cloudwatch.get_paginator('list_metrics')
        [[services.append(f"{j['Namespace']}") for j in i['Metrics'] if
          j['MetricName'] in AWS_METRIC_NAMES and j['Namespace'] in AWS_NAMESPACES] for i in cloudwatch.paginate()]

        return services

    def get_dimensions(self, service):
        """
        Returns a list of dimensions available for a specific service.
        Param service: The name of the AWS service for which dimensions are to be retrieved.
        Return: A list of dimensions for the specified service.
        """
        dimensions = list()
        cloudwatch = self.cloudwatch.get_paginator('list_metrics')
        [[dimensions.append(f"{j['Dimensions']}") for j in i['Metrics'] if
          j['MetricName'] in AWS_METRIC_NAMES and j['Namespace'] in AWS_NAMESPACES] for i in
         cloudwatch.paginate(Namespace=f"AWS/{service}")]
        return dimensions

    def get_query(self, namespace, metric_name, dimensions, start_time, end_time, period, statistic):
        """
        Executes a query to retrieve metric statistics for a given namespace, metric name, dimensions, and time range.
        Params:
            -namespace: The namespace of the metric.
            -metric_name: The name of the metric.
            -dimensions: The dimensions of the metric (if applicable).
            -start_time: The start time of the time range for the query.
            -end_time: The end time of the time range for the query.
            -period: The granularity, in seconds, for the returned data.
            -statistic: The type of statistic to retrieve (e.g., 'SampleCount', 'Average', 'Sum', 'Minimum', 'Maximum').
        Return: The result of the CloudWatch query containing metric statistics.
        """
        try:
            return self.cloudwatch.get_metric_statistics(
                Namespace=namespace,
                MetricName=metric_name,
                Dimensions=dimensions,
                StartTime=start_time,
                EndTime=end_time,
                Period=period,
                Statistics=statistic,
                # ExtendedStatistics=[
                #     'string',
                # ],
                # Unit='Seconds' | 'Microseconds' | 'Milliseconds' | 'Bytes' | 'Kilobytes' | 'Megabytes' | 'Gigabytes' | 'Terabytes' | 'Bits' | 'Kilobits' | 'Megabits' | 'Gigabits' | 'Terabits' | 'Percent' | 'Count' | 'Bytes/Second' | 'Kilobytes/Second' | 'Megabytes/Second' | 'Gigabytes/Second' | 'Terabytes/Second' | 'Bits/Second' | 'Kilobits/Second' | 'Megabits/Second' | 'Gigabits/Second' | 'Terabits/Second' | 'Count/Second' | 'None'
            )
        except:
            return "Error executing query"
