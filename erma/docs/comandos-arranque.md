# Comandos para encender ERMA

Esta guia es para levantar ERMA rapido sin tener que recordar todos los pasos.

## En mi PC Windows

Desde PowerShell:

```powershell
cd C:\proyectos\ermainfinity
.\scripts\dev.cmd
```

Si quedo algo viejo ocupando puertos:

```powershell
cd C:\proyectos\ermainfinity
.\scripts\dev.cmd -StopExisting
```

Si es la primera vez o queres reinstalar dependencias:

```powershell
cd C:\proyectos\ermainfinity
.\scripts\dev.cmd -Install
```

Abrir en el navegador de la PC:

```text
http://127.0.0.1:5173
```

Apagar ERMA en la PC:

```powershell
cd C:\proyectos\ermainfinity
.\scripts\stop.cmd
```

## En la Raspberry

Entrar por SSH desde la PC:

```powershell
ssh gianni@192.168.1.27
```

Levantar ERMA en la Raspberry:

```bash
cd ~/ermainfinity
./scripts/dev.sh
```

Si aparece `Permission denied`, dar permisos de ejecucion:

```bash
cd ~/ermainfinity
chmod +x scripts/dev.sh scripts/stop.sh
./scripts/dev.sh
```

Alternativa sin cambiar permisos:

```bash
cd ~/ermainfinity
bash scripts/dev.sh
```

Si queres actualizar desde GitHub y reiniciar limpio:

```bash
cd ~/ermainfinity
git pull
./scripts/dev.sh --stop-existing
```

Si es la primera vez o queres reinstalar dependencias:

```bash
cd ~/ermainfinity
./scripts/dev.sh --install
```

Abrir desde otra maquina de la red:

```text
http://192.168.1.27:5173
```

Apagar ERMA en la Raspberry:

```bash
cd ~/ermainfinity
./scripts/stop.sh
```

## Abrir ERMA en el display de la Raspberry

Si estas en la terminal de la Raspberry o por SSH:

```bash
DISPLAY=:0 xdg-open http://127.0.0.1:5173
```

Abrir en Chromium:

```bash
DISPLAY=:0 chromium-browser http://127.0.0.1:5173
```

Abrir en pantalla completa tipo kiosk:

```bash
DISPLAY=:0 chromium-browser --kiosk http://127.0.0.1:5173
```

Si el comando `chromium-browser` no existe:

```bash
DISPLAY=:0 chromium --kiosk http://127.0.0.1:5173
```

## Verificar que ERMA responde

Backend:

```bash
curl http://127.0.0.1:8000/state
```

Frontend:

```bash
curl http://127.0.0.1:5173
```

## Puertos usados

```text
Frontend: 5173
Backend:  8000
```
