import os
from score import Score

if __name__ == "__main__":
    """
    Main entry point of the program.
    Initializes an instance of the Score class and calculates the infrastructure score for the organization "Vehículos".
    The infrastructure score is related to monitored services in Grafana and AWS CloudWatch.
    Note: The method get_infra_score() in the Score class is responsible for calculating the infrastructure score.
    """

    try:
        score = Score('Vehículos')
        print(score.get_infra_score())
        # print(score.dashboard_scoring("VC_RpqOqq77z"))

    except:
        print('Error grafana function')


def lambda_handler(event, context):
    """
    Lambda function for AWS.
    This function is used when the program is deployed as an AWS Lambda function.
    The implementation of this function may vary depending on specific needs for handling events and contexts in Lambda.
    """
    print("Lambda working...")
