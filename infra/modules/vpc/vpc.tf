#Create the VPC Block
resource "aws_vpc" "devops_course_vpc" {
    cidr_block = var.vpc_cidr
    enable_dns_support = true
    enable_dns_hostnames = true
    tags = {
        Name = "devops_course_vpc"
    }
}