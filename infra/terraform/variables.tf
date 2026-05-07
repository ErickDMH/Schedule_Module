variable "db_password" {
  description = "Password for the schedule module database"
  type        = string
  sensitive   = true
}

variable "db_name" {
  description = "Name of the schedule module database"
  type        = string
  default     = "schedule_db"
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}
