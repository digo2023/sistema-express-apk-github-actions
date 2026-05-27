[app]
# Nome visível do aplicativo
name = Sistema Express

# Pacote Android
package.name = sistemaexpress
package.domain = br.com.expresscolorado

# Arquivo principal Kivy
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,txt,md,sh,pdf,csv,xlsx,db
source.exclude_dirs = .git,__pycache__,bin,build,.buildozer

# Versão interna do APK
version = 1.0

# Requisitos Python do APK
requirements = python3,kivy,rich==13.7.1,openpyxl==3.1.5,pypdf==5.1.0,reportlab==4.2.2

# Ícone
icon.filename = icon.png

# Orientação
orientation = portrait
fullscreen = 0

# Android
android.api = 35
android.minapi = 23
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a

# Permissões para importar/exportar arquivos quando o Android permitir
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# Manter app ativo durante operações longas
android.wakelock = True

# Pasta privada do app será usada para dados, backups e relatórios
# As pastas de importação ficam dentro do armazenamento privado do aplicativo.

[buildozer]
log_level = 2
warn_on_root = 1

