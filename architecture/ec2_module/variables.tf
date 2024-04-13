variable "ami" {
	default = "ami-0faab6bdbac9486fb"
}

variable "instance_type" {
	default = "t2.micro"
}

variable "security_group_id" {
	type = string 
}

variable "key_name" {
	default = "new_rsa" 
}


variable "subnet_id" {
	default = "subnet-0977cf3277542ac72" 
}
