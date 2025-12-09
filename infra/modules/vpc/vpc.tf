#Create the VPC Block
resource "aws_vpc" "devops_course_vpc" {
    cidr_block = var.vpc_cidr
    enable_dns_support = true
    enable_dns_hostnames = true
    tags = {
        Name = "devops_course_vpc"
    }
}

# Create Internet Gateway
resource "aws_internet_gateway" "devops_course_igw" {
    vpc_id = aws_vpc.devops_course_vpc.id
    tags = {
        Name = "devops_course_igw"
    }
}

# Create Public Subnet
resource "aws_subnet" "devops_course_public_subnet" {
    vpc_id = aws_vpc.devops_course_vpc.id
    cidr_block = cidrsubnet(var.vpc_cidr, 8, 0) # Creates a /24 subnet from the VPC CIDR
    availability_zone = data.aws_availability_zones.available.names[0]
    map_public_ip_on_launch = true
    tags = {
        Name = "devops_course_public_subnet"
    }
}

# Get available availability zones
data "aws_availability_zones" "available" {
    state = "available"
}

# Create Route Table
resource "aws_route_table" "devops_course_public_rt" {
    vpc_id = aws_vpc.devops_course_vpc.id
    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = aws_internet_gateway.devops_course_igw.id
    }
    tags = {
        Name = "devops_course_public_rt"
    }
}

# Associate Route Table with Public Subnet
resource "aws_route_table_association" "devops_course_public_rta" {
    subnet_id = aws_subnet.devops_course_public_subnet.id
    route_table_id = aws_route_table.devops_course_public_rt.id
}