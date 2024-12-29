terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Local provider configuration
provider "aws" {
  region = "us-east-1"
  
  # This configuration will be used when running locally
  dynamic "assume_role_with_web_identity" {
    for_each = var.is_github_actions ? [1] : []
    content {
      role_arn           = var.oidc_role_arn
      web_identity_token = var.web_identity_token
    }
  }
}
