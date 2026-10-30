# Kevin John | AWS Cloud Resume Portfolio

Deployable personal website with About, Experience, Projects, and downloadable original resume. Private S3 + CloudFront OAC, Terraform, and GitHub Actions OIDC-based CD. All site infrastructure is managed by Terraform; website contents are uploaded through CI/CD or AWS CLI.

## Preview locally

```bash
cd site
python3 -m http.server 8000
# open http://localhost:8000
```

## Deploy first time

**Prerequisites:** AWS CLI credentials with permissions to create S3 buckets, CloudFront distributions, IAM roles and OIDC providers; Terraform >= 1.5; a GitHub repository whose default branch is `main`. Use a personal sandbox account, not a corporate production account.

1. Copy this folder into a GitHub repo. Do not upload your Terraform state or other secrets.
2. Run:

```bash
cd terraform
terraform init
terraform apply -var='github_repository=EpicCoder71/cloud-resume'
terraform output
```

3. Upload site files:

```bash
aws s3 sync ../site/ s3://$(terraform output -raw site_bucket)/ --delete
aws cloudfront create-invalidation --distribution-id "$(terraform output -raw cloudfront_distribution_id)" --paths '/*'
```

4. Open `terraform output -raw website_url` (CloudFront may take several minutes to deploy).
5. In your GitHub repo **Settings → Secrets and variables → Actions → Variables**, add:
   - `AWS_DEPLOY_ROLE_ARN` = `terraform output -raw github_deploy_role_arn`
   - `AWS_SITE_BUCKET` = `terraform output -raw site_bucket`
   - `AWS_CLOUDFRONT_ID` = `terraform output -raw cloudfront_distribution_id`
6. On subsequent pushes to `main` affecting `site/`, GitHub Actions tests the site and deploys it using OIDC without AWS keys.

## Destroy

```bash
cd terraform
terraform destroy -var='github_repository=EpicCoder71/cloud-resume'
```

**IMPORTANT:** Keep `terraform.tfstate` securely backed up while the site exists. This low-cost first version uses local Terraform state; for team automation or GitHub-based Terraform apply/destroy, move state into a separate S3 backend with locking. The destroy operation also deletes the public website bucket and its resume file. If your AWS account already has GitHub's OIDC provider, import/reuse it instead of creating a duplicate.

## Privacy & content

- Contact uses a `mailto:` link; no collection of site visitor data.
- `site/assets/Kevin-John-Resume.pdf` contains the original resume with contact information and is intended to be publicly downloadable. Review it before publishing.
- Projects are labeled planned until completed. Update the `projects` section when repos/case studies are ready.
- No custom domain is needed; CloudFront provides a generated HTTPS domain. No always-on EC2/EKS/NAT/ALB.
- S3 `force_destroy=true` makes `terraform destroy` delete objects.
- CloudFront distribution deletion takes time and must complete before teardown exits.

## Cloud Resume Challenge next steps

Add a DynamoDB + Lambda + API Gateway visitor counter, automated API tests, a custom domain, and a technical blog post when ready.
