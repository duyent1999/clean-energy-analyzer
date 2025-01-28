#Install Dependencies

resource "null_resource" "install_dependencies" {
  provisioner "local-exec" {
    command = <<EOT
      pip install -r lambda_function/requirements.txt -t lambda_function/
    EOT
  }

  triggers = {
    always_run = "${timestamp()}"
  }
}


#Zip Lambda Function

data "archive_file" "lambda_zip" {
  depends_on = [null_resource.install_dependencies]

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
