# Package the Lambda code
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "../lambda"
  output_path = "lambda_function.zip"
}

# Update existing Lambda function
resource "aws_lambda_function" "bot_update" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = data.aws_lambda_function.existing_bot.function_name
  role            = data.aws_lambda_function.existing_bot.role
  handler         = "main.lambda_handler"
  runtime         = "python3.9"
  timeout         = 30
  memory_size     = 256

  environment {
    variables = {
      DYNAMODB_TABLE = aws_dynamodb_table.shopping_list.name
      USERS_TABLE    = aws_dynamodb_table.users.name
    }
  }
}
