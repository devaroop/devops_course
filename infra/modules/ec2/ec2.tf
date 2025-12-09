# Get the latest Amazon Linux 2023 AMI
data "aws_ami" "amazon_linux" {
    most_recent = true
    owners      = ["amazon"]
    
    filter {
        name   = "name"
        values = ["al2023-ami-*-x86_64"]
    }
    
    filter {
        name   = "virtualization-type"
        values = ["hvm"]
    }
}

resource "aws_instance" "devops_course_ec2_instance" {
    ami                    = var.ami_id != "" ? var.ami_id : data.aws_ami.amazon_linux.id
    instance_type          = var.instance_type
    subnet_id              = var.subnet_id
    vpc_security_group_ids = var.security_group_ids
    associate_public_ip_address = true
    
    # User data script to install Docker
    user_data = <<-EOF
        #!/bin/bash
        # Update system packages
        sudo yum update -y
        
        # Install Docker
        sudo yum install -y docker
        
        # Start Docker service
        sudo systemctl start docker
        sudo systemctl enable docker
        
        # Add ec2-user to docker group to run docker without sudo
        sudo usermod -aG docker ec2-user
        
        # Verify Docker installation
        sudo docker --version
        sudo docker run -d -p 8000:8000 ghcr.io/devaroop/devops_course:master
    EOF
    
    tags = {
        Name = "devops_course_ec2_instance"
    }
}