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

  # OIDC Configuration
  assume_role_with_web_identity {
    role_arn = var.oidc_role_arn
    token_file = "/var/run/secrets/kubernetes.io/serviceaccount/token"
    web_identity_provider = var.oidc_provider_url
  }
}