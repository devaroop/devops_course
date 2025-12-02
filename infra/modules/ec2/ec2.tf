resource "aws_instance" "devops_course_ec2_instance" {
    ami = "ami-0d176f79571d18a8f"
    instance_type = "t3.micro"
    associate_public_ip_address = true
    vpc_security_group_ids = [aws_security_group.devops_course_sg.id]
}