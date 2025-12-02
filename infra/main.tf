terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>6.23.0"
    }
  }
}

provider "aws" {
  region = "ap-south-1" # Select your desired region
}


module "vpc" {
  source = "./modules/vpc"
  vpc_cidr = "10.0.0.0/16"
}

module "security_group" {
  source = "./modules/security_group"
  vpc_id = module.vpc.vpc_id
}