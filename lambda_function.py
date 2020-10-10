from lambda_model import LambdaModel

def lambda_handler(event, context):
    my_lambda = LambdaModel(event)
    return my_lambda.handler()