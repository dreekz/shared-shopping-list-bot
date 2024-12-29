terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
    region = "us-east-1"

    # Configuration for local environment
    # access_key = var.aws_access_key
    # secret_key = var.aws_secret_key

     # Configuration for Github Actions/OIDC
     assume_role_with_web_identity {
        role_arn = var.oidc_role_arn
        web_identity_token = "/var/run/secrets/kubernetes.io/serviceaccount/token"
        }

}