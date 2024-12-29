variable "oidc_role_arn" {
  description = "The ARN of the IAM role to assume"
  type        = string
  default     = ""  # Empty default for local development
}

variable "web_identity_token" {
  description = "The web identity token for OIDC"
  type        = string
  default     = ""  # Empty default for local development
}

variable "is_github_actions" {
  description = "Boolean to determine if running in GitHub Actions"
  type        = bool
  default     = false  # Default to local development
}