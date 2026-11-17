# INTENTIONALLY INSECURE - Checkmarx One IaC demo only.
provider "azurerm" { features {} }

resource "azurerm_storage_account" "sa" {
  name                      = "cxodemostorage"
  resource_group_name       = "rg"
  location                  = "eastus"
  account_tier              = "Standard"
  account_replication_type  = "LRS"
  enable_https_traffic_only = false
  min_tls_version           = "TLS1_0"
  allow_blob_public_access  = true
}
resource "azurerm_network_security_rule" "ssh" {
  name = "ssh" priority = 100 direction = "Inbound" access = "Allow" protocol = "Tcp"
  source_port_range = "*" destination_port_range = "22" source_address_prefix = "*" destination_address_prefix = "*"
  resource_group_name = "rg" network_security_group_name = "nsg"
}
resource "azurerm_sql_server" "sql" {
  name = "cxosql" resource_group_name = "rg" location = "eastus" version = "12.0"
  administrator_login = "sqladmin" administrator_login_password = "P@ssw0rd1234"
}
resource "azurerm_sql_firewall_rule" "all" { name = "all" resource_group_name = "rg" server_name = "cxosql" start_ip_address = "0.0.0.0" end_ip_address = "255.255.255.255" }
resource "azurerm_key_vault" "kv" { name = "kv" location = "eastus" resource_group_name = "rg" tenant_id = "t" sku_name = "standard" purge_protection_enabled = false soft_delete_retention_days = 7 }
resource "azurerm_kubernetes_cluster" "aks" {
  name = "aks" location = "eastus" resource_group_name = "rg" dns_prefix = "aks"
  role_based_access_control { enabled = false }
  default_node_pool { name = "d" node_count = 1 vm_size = "Standard_D2_v2" }
}
resource "azurerm_app_service" "app" { name = "a" location = "eastus" resource_group_name = "rg" app_service_plan_id = "p" https_only = false site_config { min_tls_version = "1.0" } }
