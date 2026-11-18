$PSVersionTable.PSVersion

$jobs = 1..8 | ForEach-Object {
    Start-Job -ScriptBlock { curl http://localhost:8080/api/task }
}
$jobs | Wait-Job | Receive-Job

