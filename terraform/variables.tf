variable "aws_region" {
  type    = string
  default = "us-east-1"
}
variable "github_repository" {
  description = "GitHub owner/repo, e.g. octocat/cloud-resume-portfolio"
  type        = string
}
variable "resource_prefix" {
  type    = string
  default = "kj-cloud-resume"
}
