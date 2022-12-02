@echo off

rem �஢�ઠ �ࠢ
net session >nul 2>&1
    if %errorLevel% == 0 (
        echo [*] ���������� ���짮��⥫�
        net user /add ziem_user *
        net localgroup "���짮��⥫� DCOM" ziem_user /add
        net localgroup "���짮��⥫� ��ୠ��� �ந�����⥫쭮��" ziem_user /add
        net localgroup "���⥫� ��ୠ�� ᮡ�⨩" ziem_user /add

        echo [*] ����ன�� �࠭�����
        netsh advfirewall firewall add rule ^
            name="ZIEM-RPC-135" dir=in action=allow ^
            protocol=TCP localport=135 ^
            program="%SystemRoot%\system32\svchost.exe" enable=yes
        netsh advfirewall firewall add rule ^
            name="ZIEM-RPC-dynamic" dir=in action=allow ^
            protocol=TCP localport=RPC ^
            program="%SystemRoot%\system32\svchost.exe" enable=yes

        echo [*] ����ன�� �㤨�
        del C:\Windows\security\audit\audit.csv
        del C:\Windows\System32\GroupPolicy\Machine\Microsoft\WindowsNT\Audit\audit.csv
        del C:\Windows\System32\GroupPolicy\gpt.ini
        gpupdate /force

        echo �室 ��⭮� �����
        auditpol /set /subcategory:"��㣨� ᮡ��� �室� ����� ����ᥩ" /success:enable
        auditpol /set /subcategory:"�஢�ઠ ����� ������" /success:enable

        echo ���� �����
        auditpol /set /subcategory:"��ࠢ����� ���묨 �����ﬨ" /success:enable
        auditpol /set /subcategory:"��ࠢ����� ��㯯�� ������᭮��" /success:enable

        echo ���஡��� ��᫥�������
        auditpol /set /subcategory:"�������� �����" /success:enable

        echo �室/��室
        auditpol /set /subcategory:"�室 � ��⥬�" /success:enable /failure:enable
        auditpol /set /subcategory:"��㣨� ᮡ��� �室� � ��室�" /success:enable /failure:enable
        auditpol /set /subcategory:"���樠��� �室" /success:enable
        auditpol /set /subcategory:"��室 �� ��⥬�" /success:enable

        echo ����� � ��ꥪ⠬
        auditpol /set /subcategory:"�������� ��⥬�" /success:enable
        auditpol /set /subcategory:"��㣨� ᮡ��� ����㯠 � ��ꥪ��" /success:enable
        auditpol /set /subcategory:"������� ����� ��饣� ����㯠" /success:enable
        auditpol /set /subcategory:"��ꥪ�-�������" /success:enable

        echo ��������� ����⨪�
        auditpol /set /subcategory:"�㤨� ��������� ����⨪�" /success:enable
        auditpol /set /subcategory:"��������� ����⨪� �஢�ન ����������" /success:enable
        auditpol /set /subcategory:"��������� ����⨪� �ࠢ��� �஢�� MPSSVC" /success:enable

        echo ���⥬�
        auditpol /set /subcategory:"��������� ���ﭨ� ������᭮��" /success:enable
        auditpol /set /subcategory:"��㣨� ��⥬�� ᮡ���" /success:enable

    ) else (
        echo [-] �訡��: ������� �ਯ� � �ࠢ��� �����������
    )
    pause >nul
