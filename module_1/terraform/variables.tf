variable "credentials" {
  description = "Project credentials"
  default     = "./keys/my-creds.json"
}

variable "project" {
  description = "Project name"
  default     = "black-nucleus-412511"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}

variable "location" {
  description = "Project location"
  default     = "US"
}


variable "bg_dataset_name" {
  description = "My bigquery dataset name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "My storage bucket name"
  default     = "black-nucleus-412511-terra-bucket"
}

variable "gsc_storage_class" {
  description = "Bucket storage class"
  default     = "STANDARD"
}