@echo off
rem �w��t�H���_�z���̃t�@�C�����ċA�I�ɍ폜����
setlocal
set HERE=%~dp0


pushd %HERE%

for /R ..\test_ea %%i in (*.test_res)  do echo %%i

popd
endlocal