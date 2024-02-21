# Dans le répertoire .env

Get-Content .env.dev | ForEach-Object {
    # Ignorer les lignes vides ou celles qui ne contiennent pas "="
    if ($_ -and $_ -contains '=') {
        $pair = $_ -split '=', 2
        [System.Environment]::SetEnvironmentVariable($pair[0], $pair[1], [System.EnvironmentVariableTarget]::Process)
    }
}

Get-Content .env.dev | ForEach-Object {
    if ($_ -and $_ -match '=') { # Vérifie si la ligne contient "="
        $pair = $_ -split '=', 2
        if ($pair[0] -ne $null -and $pair[0].Trim() -ne "") { # Assurez-vous que le nom de la variable n'est pas vide
            [System.Environment]::SetEnvironmentVariable($pair[0], $pair[1], [System.EnvironmentVariableTarget]::Process)
        }
    }
}
