variable "aws_region" {
  description = "The AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "s3_bucket_name" {
  description = "The name of the S3 bucket"
  type        = string
  default     = "clean-energy-bucket" # Change to a unique name
}

variable "lambda_function_name" {
  description = "The name of the Lambda function"
  type        = string
  default     = "clean-energy-lambda"
}

variable "lambda_handler" {
  description = "The Lambda function handler"
  type        = string
  default     = "clean-energy.lambda_handler"
}

variable "lambda_runtime" {
  description = "The runtime environment for the Lambda function"
  type        = string
  default     = "nodejs18.x"
}

variable "lambda_filename" {
  description = "The filename of the Lambda deployment package"
  type        = string
  default     = "lambda_function_payload.zip"
}

variable "cloudwatch_log_retention" {
  description = "The retention period for CloudWatch logs (in days)"
  type        = number
  default     = 7
}

# Lambda Specific

variable "openweather_api_key" {
  description = "API key for OpenWeatherMap"
  type        = string
  sensitive   = true
  default     = " "
}

variable "nrel_api_key" {
  description = "API key for NREL"
  type        = string
  sensitive   = true
  default     = " "
}
