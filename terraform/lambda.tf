resource "aws_iam_role" "lambda_role" {
    name = "lambda_role"
    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
        {
            Action = "sts:AssumeRole"
            Principal = {
            Service = "lambda.amazonaws.com"
            }
            Effect = "Allow"
        },
        ]
    })
}

resource "aws_iam_policy" "lambda_policy" {
  name = "lambda_policy"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = ["logs:CreateLogGroup",
                  "logs:CreateLogStream",
                  "logs:PutLogEvents"
        ],
        Effect   = "Allow",
        Resource = "arn:aws:logs:*:*:*"
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  policy_arn = aws_iam_policy.lambda_policy.arn
  role       = aws_iam_role.lambda_role.name
}

data "archive_file" "lambda_zip" {
  type = "zip"
  source_dir  = "../lambda"
  output_path = "lambda_function.zip"
}

resource "aws_lambda_function" "shopping_bot" {
  filename      = data.archive_file.lambda_zip.output_path
  function_name = "shopping_bot"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.lambda_handler"
  runtime       = "python3.9"
}