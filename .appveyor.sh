appveyor DownloadFile https://github.com/cayleygraph/cayley/releases/download/v0.7.0/cayley_0.7.0_windows_amd64.zip -Timeout 5000
7z x cayley_0.7.0_windows_amd64.zip cayley_0.7.0_windows_amd64
cd /?
cd cayley_0.7.0_windows_amd64
cd /?
dir /a
cayley.exe http --dbpath=30kmoviedata.nq.gz &
sleep 2
