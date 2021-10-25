call nssm.exe install wr_docs_portal "%cd%\run_server.bat"
rem call nssm.exe edit wr_docs_portal
call nssm.exe set wr_docs_portal AppStdout "%cd%\logs\wr_docs_portal.log"
call nssm.exe set wr_docs_portal AppStderr "%cd%\logs\wr_docs_portal.log"
nssm set wr_docs_portal AppRotateFiles 1
nssm set wr_docs_portal AppRotateOnline 1
nssm set wr_docs_portal AppRotateSeconds 86400
nssm set wr_docs_portal AppRotateBytes 104857600
call sc start wr_docs_portal