variable "service" {
  type = object({
    name = string
  })
  default = {
    name = "sg-psi-bot"
  }
}

variable "stages" {
  type = list(string)
  default = ["dev", "prod"]
}