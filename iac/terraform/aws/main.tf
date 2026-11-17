# INTENTIONALLY INSECURE - Checkmarx One IaC demo only.
provider "aws" {
  region     = "us-east-1"
  access_key = "AKIAIOSFODNN7EXAMPLE"                       # hardcoded credentials
  secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
}

resource "aws_s3_bucket" "data" {                           # public, unencrypted, no versioning/logging
  bucket = "cxo-demo-public-bucket"
  acl    = "public-read-write"
}

resource "aws_security_group" "open" {
  name = "allow_all"
  ingress { from_port = 0 to_port = 65535 protocol = "tcp" cidr_blocks = ["0.0.0.0/0"] }  # open to world
  ingress { from_port = 22 to_port = 22 protocol = "tcp" cidr_blocks = ["0.0.0.0/0"] }    # SSH open
  egress  { from_port = 0 to_port = 0 protocol = "-1" cidr_blocks = ["0.0.0.0/0"] }
}

resource "aws_db_instance" "db" {
  engine              = "mysql"
  instance_class      = "db.t3.micro"
  username            = "admin"
  password            = "admin12345"                        # hardcoded password
  publicly_accessible = true
  storage_encrypted   = false
  skip_final_snapshot = true
  backup_retention_period = 0
}

resource "aws_instance" "web" {
  ami           = "ami-0abcdef1234567890"
  instance_type = "t3.micro"
  associate_public_ip_address = true
  metadata_options { http_tokens = "optional" }             # IMDSv1 allowed
  root_block_device { encrypted = false }
  user_data = "export DB_PASSWORD=admin12345"
}

resource "aws_iam_policy" "admin" {
  name   = "admin-star"
  policy = jsonencode({ Version = "2012-10-17", Statement = [{ Effect = "Allow", Action = "*", Resource = "*" }] })
}

resource "aws_ebs_volume" "v" { availability_zone = "us-east-1a" size = 10 encrypted = false }
resource "aws_cloudtrail" "t" { name = "t" s3_bucket_name = aws_s3_bucket.data.id enable_log_file_validation = false is_multi_region_trail = false }
resource "aws_kms_key" "k" { enable_key_rotation = false }
resource "aws_lb_listener" "http" { load_balancer_arn = "arn:aws:elasticloadbalancing:x" port = 80 protocol = "HTTP" default_action { type = "forward" target_group_arn = "arn:x" } }
resource "aws_sqs_queue" "q" { name = "q" }                 # unencrypted queue
resource "aws_sns_topic" "s" { name = "s" }                 # unencrypted topic
resource "aws_ecr_repository" "r" { name = "r" image_tag_mutability = "MUTABLE" image_scanning_configuration { scan_on_push = false } }
