# Airzone 運用マニュアル

## 概要

このドキュメントは、Airzone プラットフォームの日常的な運用、監視、トラブルシューティング、メンテナンスに関する手順を説明します。

## 目次

1. [日常運用](#日常運用)
2. [監視とアラート](#監視とアラート)
3. [バックアップとリストア](#バックアップとリストア)
4. [トラブルシューティング](#トラブルシューティング)
5. [メンテナンス](#メンテナンス)
6. [セキュリティ](#セキュリティ)
7. [スケーリング](#スケーリング)

---

## 日常運用

### サービスの起動・停止

#### バックエンドサービス

```bash
# 起動
sudo systemctl start airzone-backend

# 停止
sudo systemctl stop airzone-backend

# 再起動
sudo systemctl restart airzone-backend

# ステータス確認
sudo systemctl status airzone-backend

# ログ確認
sudo journalctl -u airzone-backend -f
```

#### フロントエンドサービス

```bash
# 起動
sudo systemctl start airzone-frontend

# 停止
sudo systemctl stop airzone-frontend

# 再起動
sudo systemctl restart airzone-frontend

# ステータス確認
sudo systemctl status airzone-frontend

# ログ確認
sudo journalctl -u airzone-frontend -f
```

#### Apache Web サーバー

```bash
# 起動
sudo systemctl start apache2

# 停止
sudo systemctl stop apache2

# 再起動
sudo systemctl restart apache2

# 設定リロード（ダウンタイムなし）
sudo systemctl reload apache2

# ステータス確認
sudo systemctl status apache2

# 設定テスト
sudo apache2ctl configtest
```

#### MySQL データベース

```bash
# 起動
sudo systemctl start mysql

# 停止
sudo systemctl stop mysql

# 再起動
sudo systemctl restart mysql

# ステータス確認
sudo systemctl status mysql

# 接続テスト
mysql -u airzone_user -p airzone
```

### ログの確認

#### アプリケーションログ

```bash
# バックエンドログ
tail -f /var/log/airzone/app.log

# エラーログのみ
grep ERROR /var/log/airzone/app.log

# 特定ユーザーのログ
grep "user_id: <uuid>" /var/log/airzone/app.log

# 日付範囲でフィルタ
grep "2024-01-01" /var/log/airzone/app.log
```

#### Apache ログ

```bash
# アクセスログ
tail -f /var/log/apache2/access.log

# エラーログ
tail -f /var/log/apache2/error.log

# 特定 IP のアクセス
grep "192.168.1.100" /var/log/apache2/access.log

# 4xx/5xx エラー
grep " 4[0-9][0-9] " /var/log/apache2/access.log
grep " 5[0-9][0-9] " /var/log/apache2/access.log
```

#### MySQL ログ

```bash
# エラーログ
tail -f /var/log/mysql/error.log

# スロークエリログ（有効化されている場合）
tail -f /var/log/mysql/slow-query.log
```

### ヘルスチェック

#### システムヘルスチェック

```bash
# CPU 使用率
top
htop

# メモリ使用率
free -h

# ディスク使用率
df -h

# ネットワーク接続
netstat -tuln
ss -tuln

# プロセス確認
ps aux | grep python
ps aux | grep node
```

#### アプリケーションヘルスチェック

```bash
# バックエンド API
curl http://localhost:5000/health

# フロントエンド
curl http://localhost:3000

# データベース接続
cd /var/www/airzone/backend
python verify_database.py

# スポンサーウォレット残高
python verify_sponsored_transactions.py
```

---

## 監視とアラート

### 重要な監視項目

#### 1. システムリソース

**CPU 使用率**
- **正常:** < 70%
- **警告:** 70-85%
- **危険:** > 85%

**メモリ使用率**
- **正常:** < 80%
- **警告:** 80-90%
- **危険:** > 90%

**ディスク使用率**
- **正常:** < 80%
- **警告:** 80-90%
- **危険:** > 90%

#### 2. アプリケーションメトリクス

**API レスポンスタイム**
- **正常:** < 200ms
- **警告:** 200-500ms
- **危険:** > 500ms

**エラー率**
- **正常:** < 1%
- **警告:** 1-5%
- **危険:** > 5%

**データベース接続プール**
- **正常:** < 80% 使用
- **警告:** 80-95% 使用
- **危険:** > 95% 使用

#### 3. ビジネスメトリクス

**NFT 発行成功率**
- **正常:** > 95%
- **警告:** 90-95%
- **危険:** < 90%

**決済成功率**
- **正常:** > 98%
- **警告:** 95-98%
- **危険:** < 95%

**スポンサーウォレット残高**
- **正常:** > 10 SUI
- **警告:** 5-10 SUI
- **危険:** < 5 SUI

### 監視スクリプト

#### システムリソース監視

```bash
#!/bin/bash
# /usr/local/bin/check_system_resources.sh

# CPU 使用率
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
if (( $(echo "$CPU_USAGE > 85" | bc -l) )); then
    echo "CRITICAL: CPU usage is ${CPU_USAGE}%"
    # アラート送信（メール、Slack など）
fi

# メモリ使用率
MEM_USAGE=$(free | grep Mem | awk '{print ($3/$2) * 100.0}')
if (( $(echo "$MEM_USAGE > 90" | bc -l) )); then
    echo "CRITICAL: Memory usage is ${MEM_USAGE}%"
fi

# ディスク使用率
DISK_USAGE=$(df -h / | tail -1 | awk '{print $5}' | cut -d'%' -f1)
if [ $DISK_USAGE -gt 90 ]; then
    echo "CRITICAL: Disk usage is ${DISK_USAGE}%"
fi
```

#### スポンサーウォレット残高監視

```bash
#!/bin/bash
# /usr/local/bin/check_sponsor_balance.sh

cd /var/www/airzone/backend
BALANCE=$(python -c "
from clients.sui_client import SuiClient
from config import Config
client = SuiClient(Config.SUI_NETWORK, Config.SUI_SPONSOR_PRIVATE_KEY)
balance = client.get_sponsor_balance() / 1_000_000_000
print(balance)
")

if (( $(echo "$BALANCE < 5" | bc -l) )); then
    echo "CRITICAL: Sponsor wallet balance is ${BALANCE} SUI"
    # アラート送信
elif (( $(echo "$BALANCE < 10" | bc -l) )); then
    echo "WARNING: Sponsor wallet balance is ${BALANCE} SUI"
fi
```

#### サービス死活監視

```bash
#!/bin/bash
# /usr/local/bin/check_services.sh

# バックエンド
if ! systemctl is-active --quiet airzone-backend; then
    echo "CRITICAL: Backend service is down"
    sudo systemctl start airzone-backend
fi

# フロントエンド
if ! systemctl is-active --quiet airzone-frontend; then
    echo "CRITICAL: Frontend service is down"
    sudo systemctl start airzone-frontend
fi

# MySQL
if ! systemctl is-active --quiet mysql; then
    echo "CRITICAL: MySQL service is down"
    sudo systemctl start mysql
fi

# Apache
if ! systemctl is-active --quiet apache2; then
    echo "CRITICAL: Apache service is down"
    sudo systemctl start apache2
fi
```

### Cron ジョブ設定

```bash
# /etc/crontab に追加

# 5分ごとにシステムリソース監視
*/5 * * * * root /usr/local/bin/check_system_resources.sh >> /var/log/airzone/monitoring.log 2>&1

# 10分ごとにスポンサーウォレット残高監視
*/10 * * * * root /usr/local/bin/check_sponsor_balance.sh >> /var/log/airzone/monitoring.log 2>&1

# 1分ごとにサービス死活監視
* * * * * root /usr/local/bin/check_services.sh >> /var/log/airzone/monitoring.log 2>&1
```

---

## バックアップとリストア

### データベースバックアップ

#### 手動バックアップ

```bash
# 完全バックアップ
mysqldump -u airzone_user -p airzone > /backup/airzone_$(date +%Y%m%d_%H%M%S).sql

# 圧縮バックアップ
mysqldump -u airzone_user -p airzone | gzip > /backup/airzone_$(date +%Y%m%d_%H%M%S).sql.gz

# 特定テーブルのみ
mysqldump -u airzone_user -p airzone users wallets > /backup/airzone_users_$(date +%Y%m%d).sql
```

#### 自動バックアップスクリプト

```bash
#!/bin/bash
# /usr/local/bin/backup_database.sh

BACKUP_DIR="/backup/mysql"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

# バックアップディレクトリ作成
mkdir -p $BACKUP_DIR

# データベースバックアップ
mysqldump -u airzone_user -p$(cat /root/.mysql_password) airzone | gzip > $BACKUP_DIR/airzone_$DATE.sql.gz

# 古いバックアップ削除
find $BACKUP_DIR -name "airzone_*.sql.gz" -mtime +$RETENTION_DAYS -delete

# バックアップ成功確認
if [ $? -eq 0 ]; then
    echo "Backup completed successfully: airzone_$DATE.sql.gz"
else
    echo "Backup failed!"
    exit 1
fi
```

#### Cron 設定（毎日午前3時）

```bash
# /etc/crontab
0 3 * * * root /usr/local/bin/backup_database.sh >> /var/log/airzone/backup.log 2>&1
```

### データベースリストア

#### 完全リストア

```bash
# 圧縮ファイルから直接リストア
gunzip < /backup/airzone_20240101_030000.sql.gz | mysql -u airzone_user -p airzone

# または2ステップ
gunzip /backup/airzone_20240101_030000.sql.gz
mysql -u airzone_user -p airzone < /backup/airzone_20240101_030000.sql
```

#### 特定テーブルのリストア

```bash
# テーブルを削除してからリストア
mysql -u airzone_user -p airzone -e "DROP TABLE IF EXISTS users;"
mysql -u airzone_user -p airzone < /backup/airzone_users_20240101.sql
```

### アプリケーションファイルバックアップ

```bash
#!/bin/bash
# /usr/local/bin/backup_application.sh

BACKUP_DIR="/backup/application"
DATE=$(date +%Y%m%d)

# バックアップディレクトリ作成
mkdir -p $BACKUP_DIR

# バックエンドファイル
tar -czf $BACKUP_DIR/backend_$DATE.tar.gz \
    -C /var/www/airzone \
    --exclude='backend/venv' \
    --exclude='backend/__pycache__' \
    --exclude='backend/*.pyc' \
    backend/

# フロントエンドファイル
tar -czf $BACKUP_DIR/frontend_$DATE.tar.gz \
    -C /var/www/airzone \
    --exclude='frontend/node_modules' \
    --exclude='frontend/.next' \
    frontend/

# 設定ファイル
tar -czf $BACKUP_DIR/config_$DATE.tar.gz \
    /var/www/airzone/backend/.env \
    /var/www/airzone/frontend/.env.local \
    /etc/apache2/sites-available/airzone.conf \
    /etc/systemd/system/airzone-*.service

echo "Application backup completed"
```

---
