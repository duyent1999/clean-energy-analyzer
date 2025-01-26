output "lambda_function_name" {
  description = "The name of the Lambda function"
  value       = aws_lambda_function.clean_energy_lambda.function_name
}

output "lambda_role_arn" {
  description = "The ARN of the IAM role for the Lambda function"
  value       = aws_iam_role.lambda_exec_role.arn
}

output "lambda_function_arn" {
  description = "The ARN of the Lambda function"
  value       = aws_lambda_function.clean_energy_lambda.arn
}