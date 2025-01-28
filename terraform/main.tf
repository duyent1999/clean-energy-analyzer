locals {
  # Retrieve the secret from AWS Secrets Manager
  clean_energy_secrets = jsondecode(data.aws_secretsmanager_secret_version.clean_energy_secrets.secret_string)

  # Extract the API keys from the secret
  openweather_api_key = local.clean_energy_secrets["OPENWEATHER_API_KEY"]
  nrel_api_key         = local.clean_energy_secrets["NREL_API_KEY"]
}

# Data source to fetch the secret from AWS Secrets Manager
data "aws_secretsmanager_secret_version" "clean_energy_secrets" {
  secret_id = "clean-energy-secrets"
}

# Create an IAM role for the Lambda function
resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}


resource "aws_iam_policy" "lambda_policy" {
  name        = "lambda_policy"
  description = "Policy for Lambda to access S3, CloudWatch, ECR, and Secrets Manager"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      # S3 Permissions
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Resource = [
          "arn:aws:s3:::clean-energy-bucket",
          "arn:aws:s3:::clean-energy-bucket/*"
        ]
      },
      # CloudWatch Logs Permissions
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      },
      # Secrets Manager Permissions
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = "arn:aws:secretsmanager:us-east-1:423623854900:secret:clean-energy-secrets-eYxXmC"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Attach the IAM Policy to the IAM Role
resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}


# Create the Lambda function
resource "aws_lambda_function" "clean_energy_lambda" {
  function_name = "clean_energy_lambda"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "clean-energy.lambda_handler"
  runtime       = "python3.9"

  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  timeout = 900

  environment {
    variables = {
      OPENWEATHER_API_KEY = local.openweather_api_key
      NREL_API_KEY = local.nrel_api_key
    }

  }

  depends_on = [data.archive_file.lambda_zip]
}


# CloudWatch Log Group for Lambda
resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.clean_energy_lambda.function_name}"
  retention_in_days = var.cloudwatch_log_retention
}