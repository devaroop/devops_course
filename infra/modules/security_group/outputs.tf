output "security_group_id" {
    description = "ID of the security group"
    value       = aws_security_group.devops_course_sg.id
}

