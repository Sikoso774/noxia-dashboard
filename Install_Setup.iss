; Fichier : NoxiaSetup.iss
[Setup]
AppName=Noxia Security Dashboard
AppVersion=1.0
DefaultDirName={autopf}\NoxiaDashboard
DefaultGroupName=Noxia Security
OutputBaseFilename=Setup_NoxiaDashboard
Compression=lzma2
SolidCompression=yes
; Optionnel : Ajoute une icône pour ton installeur si tu en as une dans tes assets
; SetupIconFile=assets\icon.ico

[Files]
; On lui dit de prendre TOUT le contenu du dossier main.dist généré par Nuitka
Source: "main.dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; On crée un raccourci dans le menu Démarrer
Name: "{group}\Noxia Dashboard"; Filename: "{app}\main.exe"
; On crée un raccourci sur le Bureau
Name: "{autodesktop}\Noxia Dashboard"; Filename: "{app}\main.exe"

[Run]
; Permet de lancer l'application directement à la fin de l'installation
Filename: "{app}\main.exe"; Description: "Lancer Noxia Security Dashboard"; Flags: nowait postinstall skipifsilent