$target = "x64"
$tools_version = "14.10.25017"
$winsdk_version = "10.0.15063.0"

$tools_root = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\2017\BuildTools\VC\Tools\MSVC\$tools_version"
$winsdk_lib_root = "${env:ProgramFiles(x86)}\Windows Kits\10\Lib\$winsdk_version"
$env:LIB = "$tools_root\lib\x64;$winsdk_lib_root\ucrt\$target;$winsdk_lib_root\um\$target"

$tools_bin = "$tools_root\bin\HostX64\$target"
$link = "$tools_bin\link.exe"

& $link /nologo /subsystem:console msvcrt.lib ucrt.lib $args
exit $LastExitCode
