targetScope = 'subscription'

@description('The name of the resource group')
param resourceGroupName string = 'rg-volvo-dmc-generator'

@description('The location for all resources')
param location string = 'East US'

@description('The name of the App Service')
param appServiceName string = 'volvo-dmc-generator'

@description('The Docker image to deploy')
param dockerImage string = 'ghcr.io/god-fathel2/volvo-dmc-generator/volvo-dmc-generator:latest'

@description('Environment name for tagging')
param environmentName string = 'production'

// Create resource group
resource resourceGroup 'Microsoft.Resources/resourceGroups@2023-07-01' = {
  name: resourceGroupName
  location: location
  tags: {
    environment: environmentName
    project: 'volvo-dmc-generator'
    'azd-env-name': environmentName
  }
}

// Deploy App Service
module appService 'app-service.bicep' = {
  name: 'app-service-deployment'
  scope: resourceGroup
  params: {
    appServiceName: appServiceName
    location: location
    dockerImage: dockerImage
    environmentName: environmentName
  }
}

// Outputs
output resourceGroupName string = resourceGroup.name
output appServiceUrl string = appService.outputs.appServiceUrl
output appServiceName string = appService.outputs.appServiceName
output dockerImage string = appService.outputs.dockerImage
