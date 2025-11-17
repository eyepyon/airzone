# XRPL Dependencies Fix

## Problem

```
ModuleNotFoundError: No module named 'websockets.asyncio'
```

This error occurs because the `websockets` package version is incompatible with `xrpl-py==2.5.0`.

## Solution

### Option 1: Update websockets (Recommended)

```bash
cd /var/www/airzone/backend
source venv/bin/activate
pip install --upgrade websockets
```

### Option 2: Reinstall all dependencies

```bash
cd /var/www/airzone/backend
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

### Option 3: Fresh install

```bash
cd /var/www/airzone/backend
source venv/bin/activate
pip uninstall -y xrpl-py websockets
pip install xrpl-py==2.5.0 websockets>=12.0
```

## Verify Installation

```bash
python3 -c "from xrpl.clients import JsonRpcClient; print('✓ XRPL client imported successfully')"
```

## Start Application

```bash
python3 app.py
```

## Alternative: Use xrpl-py 2.6.0

If the issue persists, try upgrading to the latest xrpl-py:

```bash
pip install --upgrade xrpl-py
```

Then update `requirements.txt`:
```
xrpl-py>=2.6.0
websockets>=12.0
```
