setlocal
set HERE=%~dp0

set CMDPATH=%DWODS42_TOOLS_PATH%\cmd\JPN
pushd %HERE%

set CSV_DIR=%HERE%test_count

set HOST_NAME=qareport
set PORT_NUM=6001
set DB_NAME=slt



rem summary
rem 日付+ファイル名をキーにアップデートロードする。
rem call %CMDPATH%\dwtab_import "%HOST_NAME%" %PORT_NUM% "Administrator" "" "%DB_NAME%" "slt_summary" "VTB_ROOT" "slt_summary" "%CSV_DIR%\summary.csv" "" 0 3 2 "pk"
call %CMDPATH%\dwtab_import "%HOST_NAME%" %PORT_NUM% "Administrator" "" "%DB_NAME%" "slt_summary" "VTB_ROOT" "slt_summary" "%CSV_DIR%\summary.csv" "" 0 2 2

rem detail
rem call %CMDPATH%\dwtab_delete "%HOST_NAME%" %PORT_NUM% "Administrator" "" "%DB_NAME%" "slt_detail" ""
rem call %CMDPATH%\dwtab_rebuild "%HOST_NAME%" %PORT_NUM% "Administrator" "" "%DB_NAME%" "slt_detail" 0 0 0
rem for /R %CSV_DIR% %%i in (*.test.csv) do %CMDPATH%\dwtab_import "%HOST_NAME%" %PORT_NUM% "Administrator" "" "%DB_NAME%" "slt_detail" "VTB_ROOT" "slt_detail" "%%i" "" 0 2 2

popd
endlocal