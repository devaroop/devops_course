variable "subnet_id" {
    description = "ID of the subnet where the EC2 instance will be launched"
    type        = string
}

variable "security_group_ids" {
    description = "List of security group IDs to attach to the EC2 instance"
    type        = list(string)
}

variable "instance_type" {
    description = "EC2 instance type"
    type        = string
    default     = "t3.micro"
}

variable "ami_id" {
    description = "AMI ID for the EC2 instance (defaults to Amazon Linux 2023)"
    type        = string
    default     = "" # Will use data source if not provided
}
