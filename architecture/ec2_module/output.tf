output "instance_ip_addr" {
	value = aws_instance.protectOne.public_ip
}