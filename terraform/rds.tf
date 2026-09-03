# ==============================================================================
# Amazon RDS PostgreSQL (Multi-AZ, Encrypted, Private Subnets)
# ==============================================================================

resource "aws_db_subnet_group" "rds" {
  name        = "${var.project_name}-${var.environment}-rds-subnet-group"
  description = "Subnet group for ShalaConnect PostgreSQL in private subnets"
  subnet_ids  = aws_subnet.private[*].id

  tags = {
    Name = "${var.project_name}-rds-subnet-group"
  }
}

resource "aws_db_parameter_group" "pg16" {
  name        = "${var.project_name}-${var.environment}-pg16-params"
  family      = "postgres16"
  description = "Custom parameter group for PostgreSQL 16"

  parameter {
    name  = "log_connections"
    value = "1"
  }

  parameter {
    name  = "log_disconnections"
    value = "1"
  }

  parameter {
    name  = "timezone"
    value = "Asia/Kolkata" # Indian Standard Time (IST)
  }
}

resource "aws_db_instance" "postgres" {
  identifier        = "${var.project_name}-${var.environment}-db"
  engine            = "postgres"
  engine_version    = "16.2"
  instance_class    = "db.t4g.micro" # Cost-effective ARM Graviton
  allocated_storage = 20
  max_allocated_storage = 100
  storage_type      = "gp3"
  storage_encrypted = true

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  db_subnet_group_name   = aws_db_subnet_group.rds.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  parameter_group_name   = aws_db_parameter_group.pg16.name

  multi_az               = var.environment == "prod" ? true : false
  publicly_accessible    = false
  skip_final_snapshot    = var.environment == "prod" ? false : true
  final_snapshot_identifier = "${var.project_name}-${var.environment}-db-final-snapshot"
  deletion_protection    = var.environment == "prod" ? true : false

  backup_retention_period = 7
  backup_window           = "20:00-21:00" # 01:30 AM - 02:30 AM IST
  maintenance_window      = "Sun:21:00-Sun:22:00"

  tags = {
    Name = "${var.project_name}-rds-postgres"
  }
}
