provider "aws" {
  version = "~> 3.0"
  region  = "ap-southeast-1"
  profile = "personal"
}

terraform {
  backend "s3" {
    bucket = "ry-terraform-state"
    key    = "sg-psi-bot/terraform.tfstate"
    region = "ap-southeast-1"
  }
}