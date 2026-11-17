// INTENTIONALLY INSECURE - Checkmarx One IaC demo only.
param adminPassword string = 'P@ssw0rd1234'
resource sa 'Microsoft.Storage/storageAccounts@2021-04-01' = {
  name: 'cxobicepstore'
  location: 'eastus'
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
  properties: { supportsHttpsTrafficOnly: false, allowBlobPublicAccess: true, minimumTlsVersion: 'TLS1_0' }
}
resource kv 'Microsoft.KeyVault/vaults@2021-04-01-preview' = {
  name: 'cxokv'
  location: 'eastus'
  properties: { tenantId: 'x', sku: { family: 'A', name: 'standard' }, enableSoftDelete: false, accessPolicies: [] }
}
