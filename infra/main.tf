provider "aws" {
  region = "us-east-1"
}

resource "aws_key_pair" "obsedo_key" {
  key_name   = "obsedo-key"
  public_key = file("${path.module}/obsedo_key.pem.pub")
}

resource "aws_security_group" "obsedo_sg" {
  name        = "obsedo-sg"
  description = "Allow SSH and HTTP"
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # SSH
  }

  ingress {
    from_port   = 5001
    to_port     = 5001
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Obsedo port
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "obsedo_instance" {
  ami           = "ami-0fc5d935ebf8bc3bc" # Ubuntu 22.04 in us-east-1
  instance_type = "t3.micro"
  key_name      = aws_key_pair.obsedo_key.key_name
  security_groups = [aws_security_group.obsedo_sg.name]

  tags = {
    Name = "obsedo-server"
  }
}
