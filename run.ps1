Write-Host "🚀 Starting PriceHawk..."
docker compose up -d
Start-Sleep -Seconds 5
Start-Process "http://localhost:3000"
Write-Host "✅ PriceHawk running at http://localhost:3000"
