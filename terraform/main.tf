terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

resource "aws_db_instance" "schedule_db" {
  allocated_storage    = 20
  engine               = "postgres"
  engine_version       = "15"
  instance_class       = "db.t3.micro"
  db_name              = var.db_name
  username             = "postgres"
  password             = var.db_password
  parameter_group_name = "default.postgres15"
  skip_final_snapshot  = true
  publicly_accessible  = false
}

output "db_endpoint" {
  value = aws_db_instance.schedule_db.endpoint
}
