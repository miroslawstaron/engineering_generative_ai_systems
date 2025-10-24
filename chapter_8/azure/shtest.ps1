$headers = @{
    "Content-Type"  = "application/json"
    "Authorization" = "YOUR TOKEN HERE"
}

$body = @{
    text = "int i = "
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "https://declberta-endpoint.canadacentral.inference.ml.azure.com/score" `
    -Method POST `
    -Headers $headers `
    -Body $body
