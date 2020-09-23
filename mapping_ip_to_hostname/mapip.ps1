# mapip add             -ip ip[:port] -name name
# mapip getbyname       -name name
# mapip getbyip         -ip ip[:port]
# mapip removebyname    -name name
# mapip removebyip      -ip ip[:port]

[CmdletBinding()]
param (
    [string] $function,
    [string] $name=$null,
    [string] $ip=$null
)

$hosts_path = "$env:systemroot\system32\drivers\etc\hosts"
$ip_pattern = "(\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b)"

function Add {
    [CmdletBinding()]
    param ($ip, $name)

    if (!("$ip`t$name" -match "^\s*$ip_pattern\s+\w+\s*$")) {
        Write-Output "NOT a valid input"
        return
    }

    if((Get-Content -Path $hosts_path -Raw) -notmatch '(?<=\r\n)\z')
    {
       Add-Content -Value ([environment]::newline) -Path $hosts_path
    } 

    Write-Output "Mapping $ip to $name"
    Add-Content -Path $hosts_path -Value "$ip`t$name"
    ipconfig /flushdns
    Write-Output "Done! hosts content:"
    Write-Output (Get-Content -Path $hosts_path)
}

function GetByName {
    [CmdletBinding()]
    param ($name)
    
    Write-Output ((Select-String -Path $hosts_path -Pattern "^\s*$ip_pattern\s+$name\s*$").Line)
}

function GetByIp {
    [CmdletBinding()]
    param ($ip)

    $ip = $ip.Trim().Replace(".", "\.")

    Write-Output ((Select-String -Path $hosts_path -Pattern "^\s*$ip\s+\w+\s*$").Line)
}

function RemoveByName {
    [CmdletBinding()]
    param (
        [Parameter()]
        [string]
        $name
    )

    Write-Output "Removing $name"
    Set-Content -Path $hosts_path -Value (Select-String -Path $hosts_path -Pattern "^\s*$ip_pattern\s+$name\s*$" -NotMatch).Line
    ipconfig /flushdns
    Write-Output "Done! hosts content:"
    Write-Output (Get-Content -Path $hosts_path)
}

function RemoveByIp {
    [CmdletBinding()]
    param (
        [Parameter()]
        [string]
        $ip
    )

    Write-Output "Removing $ip"
    $ip = $ip.Trim().Replace(".", "\.")
    Set-Content -Path $hosts_path -Value (Select-String -Path $hosts_path -Pattern "^\s*$ip\s+\w+\s*$" -NotMatch).Line
    ipconfig /flushdns
    Write-Output "Done! hosts content:"
    Write-Output (Get-Content -Path $hosts_path)
}

switch ($function) {
    "add" {
        Add($ip, $name)
    }
    "getbyname" {
        GetByName($name)
    }
    "getbyip" {
        GetByIp($ip)
    }
    "removebyname" {
        RemoveByName($name)
    }
    "removebyip" {
        RemoveByIp($ip)
    }
    Default {}
}