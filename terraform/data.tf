#Zip Lambda Function

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "../lambda_function"  
  output_path = "./lambda_function.zip"
}

# AMI

data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}
