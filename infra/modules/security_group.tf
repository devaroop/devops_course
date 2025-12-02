#Create Security Groups
resource "aws_security_group" "devops_course_sg" {
    vpc_id = aws_vpc.devops_course_vpc.id # Ensure the security group is created in the same VPC
    name = "devops_course_sg"
    description = "devops_course_sg"
    ingress {
        description = "HTTP"
        from_port = 80
        to_port = 80
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"] # Allow traffic from anywhere
    }
    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
    tags = {
        Name = "devops_course_sg"
    }
}