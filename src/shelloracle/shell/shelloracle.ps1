Set-PSReadLineKeyHandler -Key Ctrl+f -ScriptBlock {
    $line = $null
    $cursor = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetBufferState([ref]$line, [ref]$cursor)
    $env:SHOR_DEFAULT_PROMPT = $line
    $env:SHOR_SHELL = "powershell"
    $output = & shor
    $env:SHOR_DEFAULT_PROMPT = $null
    $env:SHOR_SHELL = $null
    if ($LASTEXITCODE -eq 0) {
        [Microsoft.PowerShell.PSConsoleReadLine]::ReplaceLine($output)
        [Microsoft.PowerShell.PSConsoleReadLine]::EndOfLine()
    }
}
