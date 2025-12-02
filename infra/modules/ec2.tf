resource "aws_instance" "devops_course_ec2_instance" {
    depends_on = [aws_security_group.devops_course_sg, aws_subnet.devops_course_subnet]
    ami = "ami-0e86e20dae9224db8" 
    instance_type = "t2.micro"
    subnet_id = aws_subnet.devops_course_subnet.id
    associate_public_ip_address = true
    key_name = "devops_course_kp"
    vpc_security_group_ids = [aws_security_group.devops_course_sg.id]
}