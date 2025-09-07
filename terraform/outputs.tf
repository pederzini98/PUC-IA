# terraform/outputs.tf
output "streamlit_url" { description = "Public URL for Streamlit"; value = "http://${aws_instance.bugsage_ec2.public_ip}:8501" }
output "bucket_name"   { value = aws_s3_bucket.bugsage_bucket.bucket }
