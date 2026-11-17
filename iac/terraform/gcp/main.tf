# INTENTIONALLY INSECURE - Checkmarx One IaC demo only.
resource "google_storage_bucket_iam_member" "public" { bucket = "cxo-demo" role = "roles/storage.objectViewer" member = "allUsers" }
resource "google_compute_firewall" "open" {
  name = "allow-all" network = "default" source_ranges = ["0.0.0.0/0"]
  allow { protocol = "tcp" ports = ["22", "3389", "0-65535"] }
}
resource "google_compute_instance" "vm" {
  name = "vm" machine_type = "e2-micro" zone = "us-central1-a"
  can_ip_forward = true
  metadata = { "block-project-ssh-keys" = "false", "serial-port-enable" = "true" }
  boot_disk { initialize_params { image = "debian-cloud/debian-11" } }
  network_interface { network = "default" access_config {} }
  service_account { email = "default" scopes = ["cloud-platform"] }
}
resource "google_sql_database_instance" "db" {
  name = "db" database_version = "MYSQL_8_0"
  settings { tier = "db-f1-micro" ip_configuration { ipv4_enabled = true authorized_networks { value = "0.0.0.0/0" } require_ssl = false } backup_configuration { enabled = false } }
}
resource "google_container_cluster" "gke" { name = "gke" location = "us-central1" enable_legacy_abac = true master_auth { username = "admin" password = "admin12345678901234567890" } }
resource "google_project_iam_member" "owner" { project = "p" role = "roles/owner" member = "allAuthenticatedUsers" }
