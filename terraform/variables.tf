variable "app_name" {
  type        = string
  description = "name of the app"
  default     = "carryoncarlos"
}

variable "location" {
  type        = string
  description = "Location of Resources"
  default     = "germanywestcentral"
}

variable "image_tag" {
  type        = string
  description = "Image tag with the commit sha"
}