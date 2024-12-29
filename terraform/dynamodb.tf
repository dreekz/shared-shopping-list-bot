# DynamoDB Tables
resource "aws_dynamodb_table" "shopping_list" {
  name           = "ShoppingList"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "list_id"
  attribute {
    name = "list_id"
    type = "S"
  }
  tags = {
    Environment = "production"
    Project     = "shopping-list-bot"
  }
}

resource "aws_dynamodb_table" "users" {
  name           = "lists_users"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "user_id"
  attribute {
    name = "user_id"
    type = "S"
  }
  tags = {
    Environment = "production"
    Project     = "shopping-list-bot"
  }
}

# Add DynamoDB permissions to existing Lambda role
resource "aws_iam_role_policy" "dynamodb_policy" {
  name = "dynamodb_policy"
  role = data.aws_iam_role.lambda_role.name
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:DeleteItem",
          "dynamodb:Scan",
          "dynamodb:Query",
          "dynamodb:UpdateItem"
        ]
        Resource = [
          aws_dynamodb_table.shopping_list.arn,
          aws_dynamodb_table.users.arn
        ]
      }
    ]
  })
}
