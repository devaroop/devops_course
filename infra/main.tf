terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.23.0"
    }
  }
  
  # Optimize parallelism for faster plan/apply
  # Default is 10, increasing can help with multiple resources
  # Reduce if you hit AWS API rate limits
}

provider "aws" {
  region = "ap-south-1" # Select your desired region
  
  # Optimize provider settings for better performance
  default_tags {
    tags = {
      ManagedBy = "Terraform"
    }
  }
}

module "vpc" {
  source = "./modules/vpc"
  
  vpc_cidr = var.vpc_cidr
}

module "security_group" {
  source = "./modules/security_group"
  
  vpc_id = module.vpc.vpc_id
  
  depends_on = [module.vpc]
}