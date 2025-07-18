# Azure App Service Docker Deployment Configuration
# This Bicep template creates an Azure App Service with container support for the VOLVO DMC Generator

@description('The name of the App Service')
param appServiceName string = 'volvo-dmc-generator'

@description('The location for all resources')
param location string = resourceGroup().location

@description('The Docker image to deploy')
param dockerImage string = 'ghcr.io/god-fathel2/volvo-dmc-generator/volvo-dmc-generator:latest'

@description('The SKU for the App Service Plan')
param appServicePlanSku string = 'B1'

@description('Environment name for tagging')
param environmentName string = 'production'

// App Service Plan for hosting the container
resource appServicePlan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: '${appServiceName}-plan'
  location: location
  kind: 'linux'
  properties: {
    reserved: true // Required for Linux plans
  }
  sku: {
    name: appServicePlanSku
  }
  tags: {
    environment: environmentName
    project: 'volvo-dmc-generator'
  }
}

// App Service for the Docker container
resource appService 'Microsoft.Web/sites@2023-01-01' = {
  name: appServiceName
  location: location
  kind: 'app,linux,container'
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'DOCKER|${dockerImage}'
      appSettings: [
        {
          name: 'WEBSITES_PORT'
          value: '8000'
        }
        {
          name: 'FLASK_ENV'
          value: 'production'
        }
        {
          name: 'FLASK_DEBUG'
          value: 'false'
        }
        {
          name: 'DOCKER_REGISTRY_SERVER_URL'
          value: 'https://ghcr.io'
        }
      ]
      alwaysOn: true
      httpLoggingEnabled: true
      logsDirectorySizeLimit: 35
      detailedErrorLoggingEnabled: true
      cors: {
        allowedOrigins: ['*']
        supportCredentials: false
      }
    }
  }
  tags: {
    environment: environmentName
    project: 'volvo-dmc-generator'
  }
}

// Output the important values
output appServiceUrl string = 'https://${appService.properties.defaultHostName}'
output appServiceName string = appService.name
output resourceGroupName string = resourceGroup().name
output dockerImage string = dockerImage
