# PowerShell script to delete GitHub workflow runs
# Replace YOUR_TOKEN with a GitHub Personal Access Token

$owner = "GOD-FATHEl2"
$repo = "volvo-dmc"
$token = "YOUR_GITHUB_TOKEN_HERE"  # You need to create this

$headers = @{
    "Authorization" = "token $token"
    "Accept" = "application/vnd.github.v3+json"
}

# Get all workflow runs
$response = Invoke-RestMethod -Uri "https://api.github.com/repos/$owner/$repo/actions/runs" -Headers $headers -Method Get

# Delete each workflow run
foreach ($run in $response.workflow_runs) {
    Write-Host "Deleting workflow run $($run.id)..."
    try {
        Invoke-RestMethod -Uri "https://api.github.com/repos/$owner/$repo/actions/runs/$($run.id)" -Headers $headers -Method Delete
        Write-Host "Deleted workflow run $($run.id)" -ForegroundColor Green
    }
    catch {
        Write-Host "Failed to delete workflow run $($run.id): $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "Workflow cleanup completed!"
