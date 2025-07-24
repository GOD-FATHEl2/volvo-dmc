@description('Specifies the name of the environment')
param environmentName string

@description('Specifies the Azure location where the resource should be created')
param location string = resourceGroup().location

@description('Prefix for resource names to ensure uniqueness')
param resourceGroupName string

@description('Environment variables for the Container App')
param containerAppEnvironmentVariables object = {
  FLASK_ENV: 'production'
  PYTHONPATH: '/app/backend:/app'
}

// Generate unique resource token based on resource group ID
var resourceToken = toLower(uniqueString(subscription().id, resourceGroup().id, environmentName))

// Resource names following Azure naming conventions
var containerRegistryName = 'cr${resourceToken}'
var logAnalyticsName = 'log-${resourceToken}'
var applicationInsightsName = 'ai-${resourceToken}'
var keyVaultName = 'kv-${resourceToken}'
var containerAppEnvironmentName = 'cae-${resourceToken}'
var containerAppName = 'ca-volvo-dmc-${resourceToken}'

// Log Analytics Workspace for monitoring
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: logAnalyticsName
  location: location
  tags: {
    'azd-env-name': environmentName
    project: 'volvo-dmc-generator'
  }
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
    features: {
      searchVersion: 1
      legacy: 0
      enableLogAccessUsingOnlyResourcePermissions: true
    }
  }
}

// Application Insights for application monitoring
resource applicationInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: applicationInsightsName
  location: location
  tags: {
    'azd-env-name': environmentName
    project: 'volvo-dmc-generator'
  }
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
    IngestionMode: 'LogAnalytics'
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
}

// Key Vault for storing secrets
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: keyVaultName
  location: location
  tags: {
    'azd-env-name': environmentName
    project: 'volvo-dmc-generator'
  }
  properties: {
    tenantId: subscription().tenantId
    sku: {
      family: 'A'
      name: 'standard'
    }
    accessPolicies: []
    enabledForDeployment: false
    enabledForDiskEncryption: false
    enabledForTemplateDeployment: false
    enableSoftDelete: true
    softDeleteRetentionInDays: 7
    enableRbacAuthorization: true
    publicNetworkAccess: 'Enabled'
    networkAcls: {
      defaultAction: 'Allow'
      bypass: 'AzureServices'
    }
  }
}

// Container Registry for storing container images
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: containerRegistryName
  location: location
  tags: {
    'azd-env-name': environmentName
    project: 'volvo-dmc-generator'
  }
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: true
    policies: {
      quarantinePolicy: {
        status: 'disabled'
      }
      trustPolicy: {
        type: 'Notary'
        status: 'disabled'
      }
      retentionPolicy: {
        days: 7
        status: 'disabled'
      }
      exportPolicy: {
        status: 'enabled'
      }
    }
    encryption: {
      status: 'disabled'
    }
    dataEndpointEnabled: false
    publicNetworkAccess: 'Enabled'
    networkRuleBypassOptions: 'AzureServices'
    zoneRedundancy: 'Disabled'
  }
}

// Managed Identity for Container App
resource managedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'id-${resourceToken}'
  location: location
  tags: {
    'azd-env-name': environmentName
    project: 'volvo-dmc-generator'
  }
}

// Role assignment for Container Registry access
resource acrPullRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(containerRegistry.id, managedIdentity.id, 'AcrPull')
  scope: containerRegistry
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d') // AcrPull
    principalId: managedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// Container Apps Environment
resource containerAppEnvironment 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: containerAppEnvironmentName
  location: location
  tags: {
    'azd-env-name': environmentName
    project: 'volvo-dmc-generator'
  }
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: logAnalytics.listKeys().primarySharedKey
      }
    }
    zoneRedundant: false
  }
}

// Container App for VOLVO DMC Generator
resource containerApp 'Microsoft.App/containerApps@2024-03-01' = {
  name: containerAppName
  location: location
  tags: {
    'azd-env-name': environmentName
    'azd-service-name': 'volvo-dmc-app'
    project: 'volvo-dmc-generator'
  }
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${managedIdentity.id}': {}
    }
  }
  properties: {
    environmentId: containerAppEnvironment.id
    configuration: {
      activeRevisionsMode: 'Single'
      ingress: {
        external: true
        targetPort: 8000
        transport: 'http'
        allowInsecure: false
        corsPolicy: {
          allowedOrigins: ['*']
          allowedMethods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
          allowedHeaders: ['*']
          allowCredentials: false
        }
      }
      registries: [
        {
          server: containerRegistry.properties.loginServer
          identity: managedIdentity.id
        }
      ]
      secrets: []
    }
    template: {
      containers: [
        {
          name: 'volvo-dmc-app'
          image: 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
          env: [
            {
              name: 'FLASK_ENV'
              value: containerAppEnvironmentVariables.FLASK_ENV
            }
            {
              name: 'PYTHONPATH'
              value: containerAppEnvironmentVariables.PYTHONPATH
            }
            {
              name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
              value: applicationInsights.properties.ConnectionString
            }
          ]
          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
          probes: [
            {
              type: 'Readiness'
              httpGet: {
                path: '/'
                port: 8000
                scheme: 'HTTP'
              }
              initialDelaySeconds: 30
              periodSeconds: 10
              timeoutSeconds: 5
              failureThreshold: 3
            }
            {
              type: 'Liveness'
              httpGet: {
                path: '/'
                port: 8000
                scheme: 'HTTP'
              }
              initialDelaySeconds: 60
              periodSeconds: 30
              timeoutSeconds: 10
              failureThreshold: 3
            }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 10
        rules: [
          {
            name: 'http-scaling'
            http: {
              metadata: {
                concurrentRequests: '10'
              }
            }
          }
        ]
      }
    }
  }
  dependsOn: [
    acrPullRole
  ]
}

// Outputs for reference and deployment verification
@description('The name of the Container App')
output containerAppName string = containerApp.name

@description('The FQDN of the Container App')
output containerAppFQDN string = containerApp.properties.configuration.ingress.fqdn

@description('The name of the Container Registry')
output containerRegistryName string = containerRegistry.name

@description('The login server of the Container Registry')
output containerRegistryLoginServer string = containerRegistry.properties.loginServer

@description('The name of the Container Apps Environment')
output containerAppEnvironmentName string = containerAppEnvironment.name

@description('The name of the Log Analytics workspace')
output logAnalyticsWorkspaceName string = logAnalytics.name

@description('The name of the Application Insights component')
output applicationInsightsName string = applicationInsights.name

@description('The name of the Key Vault')
output keyVaultName string = keyVault.name

@description('The name of the Managed Identity')
output managedIdentityName string = managedIdentity.name

@description('The Application Insights Connection String for monitoring')
output applicationInsightsConnectionString string = applicationInsights.properties.ConnectionString

@description('The URL of the deployed application')
output applicationUrl string = 'https://${containerApp.properties.configuration.ingress.fqdn}'

@description('Resource group ID')
output RESOURCE_GROUP_ID string = resourceGroup().id

@description('The container registry endpoint')
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = containerRegistry.properties.loginServer
