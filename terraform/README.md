# Terraform — Demo Infra (EC2 + S3)

> **Atenção:** Infra de demonstração. Verifique custos e segurança (ports, keys) antes de usar em produção.

## Pré-requisitos
- Terraform >= 1.5
- Conta AWS configurada (AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY)
- VPC/Subnet existentes, AMI válida, KeyPair existente
- Imagem container publicada (ex.: `ghcr.io/SEU_USUARIO/bugsage:latest`)

## Uso
```bash
cd terraform
terraform init
terraform plan -var="s3_bucket_name=bugsage-bucket-demo" \
  -var="vpc_id=vpc-xxxxxxxx" \
  -var="subnet_id=subnet-xxxxxxxx" \
  -var="ec2_ami_id=ami-xxxxxxxx" \
  -var="ssh_key_name=meu-keypair" \
  -var="GOOGLE_API_KEY=SUACHAVEAQUI"
terraform apply
```

Ao finalizar:
```bash
terraform destroy
```
