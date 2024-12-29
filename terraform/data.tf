# Get existing Lambda function
data "aws_lambda_function" "existing_bot" {
  function_name = "shopping-list-bot-handler"
}

# Get the IAM role from the Lambda function's role ARN
data "aws_iam_role" "lambda_role" {
  name = split("/", data.aws_lambda_function.existing_bot.role)[1]
}