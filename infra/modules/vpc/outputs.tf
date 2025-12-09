output "vpc_id" {
    description = "ID of the VPC"
    value       = aws_vpc.devops_course_vpc.id
}

output "vpc_cidr_block" {
    description = "CIDR block of the VPC"
    value       = aws_vpc.devops_course_vpc.cidr_block
}

output "public_subnet_id" {
    description = "ID of the public subnet"
    value       = aws_subnet.devops_course_public_subnet.id
}

