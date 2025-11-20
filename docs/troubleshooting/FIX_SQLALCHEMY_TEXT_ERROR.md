# SQLAlchemy text() エラーの修正

## 問題

バックエンドで以下のエラーが発生していました：

```
[2025-11-20 03:51:17] ERROR routes.escrow: Error getting campaigns: 
Textual SQL expression '\n SELECT * FRO...' should be explicitly declared as text('\n SELECT * FRO...')
```

エンドポイント: `GET /api/v1/escrow/campaigns`

## 原因

SQLAlchemy 2.0では、生のSQL文字列を直接 `execute()` に渡すことができなくなりました。
すべての生SQL文字列は `text()` 関数でラップする必要があります。

これはSQLインジェクション攻撃を防ぐためのセキュリティ強化です。

## 修正内容

### 1. `backend/routes/escrow.py`

#### インポートの追加

```python
from sqlalchemy import text
```

#### SQL文の修正

**修正前:**
```python
campaigns = g.db.execute(
    """
    SELECT * FROM escrow_campaigns 
    WHERE is_active = TRUE 
    AND start_date <= NOW() 
    AND end_date >= NOW()
    ORDER BY created_at DESC
    """
).fetchall()
```

**修正後:**
```python
campaigns = g.db.execute(
    text("""
    SELECT * FROM escrow_campaigns 
    WHERE is_active = TRUE 
    AND start_date <= NOW() 
    AND end_date >= NOW()
    ORDER BY created_at DESC
    """)
).fetchall()
```

#### パラメータ付きクエリの修正

**修正前:**
```python
campaign = g.db.execute(
    "SELECT * FROM escrow_campaigns WHERE id = :id AND is_active = TRUE",
    {'id': campaign_id}
).fetchone()
```

**修正後:**
```python
campaign = g.db.execute(
    text("SELECT * FROM escrow_campaigns WHERE id = :id AND is_active = TRUE"),
    {'id': campaign_id}
).fetchone()
```

#### UPDATE文の修正

**修正前:**
```python
g.db.execute(
    "UPDATE escrow_campaigns SET current_participants = current_participants + 1 WHERE id = :id",
    {'id': campaign_id}
)
```

**修正後:**
```python
g.db.execute(
    text("UPDATE escrow_campaigns SET current_participants = current_participants + 1 WHERE id = :id"),
    {'id': campaign_id}
)
```

### 2. `backend/services/escrow_campaign_service.py`

#### インポートの追加

```python
from sqlalchemy import text
```

#### SQL文の修正

**修正前:**
```python
escrows = self.db_session.execute(
    """
    SELECT * FROM escrow_stakes 
    WHERE status = 'active' 
    AND finish_after <= :now
    """,
    {'now': now}
).fetchall()
```

**修正後:**
```python
escrows = self.db_session.execute(
    text("""
    SELECT * FROM escrow_stakes 
    WHERE status = 'active' 
    AND finish_after <= :now
    """),
    {'now': now}
).fetchall()
```

**修正前:**
```python
campaign = self.db_session.execute(
    "SELECT * FROM escrow_campaigns WHERE id = :id",
    {'id': campaign_id}
).fetchone()
```

**修正後:**
```python
campaign = self.db_session.execute(
    text("SELECT * FROM escrow_campaigns WHERE id = :id"),
    {'id': campaign_id}
).fetchone()
```

## SQLAlchemy 2.0 の変更点

### なぜ text() が必要なのか

1. **セキュリティ強化** - SQLインジェクション攻撃を防ぐ
2. **明示的な意図** - 生SQLを使用していることを明確にする
3. **型安全性** - パラメータの型チェックを強化

### 使用パターン

#### パターン1: 単純なクエリ

```python
from sqlalchemy import text

result = db.execute(text("SELECT * FROM users"))
```

#### パターン2: パラメータ付きクエリ

```python
from sqlalchemy import text

result = db.execute(
    text("SELECT * FROM users WHERE id = :user_id"),
    {'user_id': user_id}
)
```

#### パターン3: 複数行クエリ

```python
from sqlalchemy import text

result = db.execute(
    text("""
        SELECT u.*, w.address 
        FROM users u
        LEFT JOIN wallets w ON u.id = w.user_id
        WHERE u.is_active = TRUE
    """)
)
```

## 注意事項

### text() が不要なケース

以下の場合は `text()` は不要です：

1. **SQLAlchemy ORM使用時**
```python
# ORM - text()不要
users = db.query(User).filter(User.is_active == True).all()
```

2. **直接MySQLカーソル使用時**
```python
# 直接カーソル - text()不要
cursor.execute("SELECT * FROM users")
```

3. **SQLAlchemy Core使用時**
```python
# Core - text()不要
from sqlalchemy import select
stmt = select(users_table).where(users_table.c.is_active == True)
result = db.execute(stmt)
```

### text() が必要なケース

1. **生SQL文字列を execute() に渡す時**
```python
# 必須
db.execute(text("SELECT * FROM users"))
```

2. **パラメータ付き生SQL**
```python
# 必須
db.execute(text("SELECT * FROM users WHERE id = :id"), {'id': user_id})
```

## 本番環境での重要な原則

1. **SQLインジェクション対策** - 必ず `text()` とパラメータバインディングを使用
2. **ORMの優先** - 可能な限りSQLAlchemy ORMを使用
3. **生SQLの最小化** - 複雑なクエリのみ生SQLを使用

## テスト方法

### 1. エンドポイントのテスト

```bash
# キャンペーン一覧取得
curl -X GET https://api.airz.one/api/v1/escrow/campaigns

# 期待される結果: 200 OK
# エラーなし
```

### 2. ログの確認

```bash
# バックエンドログを確認
tail -f /var/log/apache2/error.log

# エラーがないことを確認
# "Textual SQL expression" エラーが出ないこと
```

## 影響範囲

この修正により、以下のエンドポイントが正常に動作するようになります：

- ✅ `GET /api/v1/escrow/campaigns` - キャンペーン一覧取得
- ✅ `POST /api/v1/escrow/stake` - ステーク作成
- ✅ `GET /api/v1/escrow/my-stakes` - 自分のステーク一覧

## 関連ファイル

- `backend/routes/escrow.py` - Escrowルート
- `backend/services/escrow_campaign_service.py` - Escrowキャンペーンサービス

## 今後の開発

新しいSQLクエリを実装する際は：

1. **ORMを優先** - 可能な限りSQLAlchemy ORMを使用
2. **生SQLは text() でラップ** - 必ず `text()` 関数を使用
3. **パラメータバインディング** - 直接文字列連結は禁止

### 良い例

```python
from sqlalchemy import text

# 良い例1: text()使用
result = db.execute(
    text("SELECT * FROM users WHERE email = :email"),
    {'email': email}
)

# 良い例2: ORM使用
user = db.query(User).filter(User.email == email).first()
```

### 悪い例

```python
# 悪い例1: text()なし
result = db.execute("SELECT * FROM users")  # エラー

# 悪い例2: 文字列連結（SQLインジェクション脆弱性）
result = db.execute(f"SELECT * FROM users WHERE email = '{email}'")  # 危険
```

## 追加修正: mappings() の使用

### 問題

`text()` を使用した後、さらに別のエラーが発生しました：

```
tuple indices must be integers or slices, not str
```

### 原因

SQLAlchemyの `text()` を使用した場合、結果はデフォルトでタプルとして返されます。
ディクショナリとしてアクセスするには、結果を `mappings()` でラップする必要があります。

### 修正方法

**修正前:**
```python
campaigns = g.db.execute(
    text("SELECT * FROM escrow_campaigns WHERE is_active = TRUE")
).fetchall()

# エラー: c['id'] はタプルには使えない
for c in campaigns:
    print(c['id'])
```

**修正後:**
```python
result = g.db.execute(
    text("SELECT * FROM escrow_campaigns WHERE is_active = TRUE")
)
campaigns = result.mappings().all()  # mappings()を使用

# 正常動作: ディクショナリとしてアクセス可能
for c in campaigns:
    print(c['id'])
```

### パターン別の修正

#### パターン1: fetchall()

```python
# 修正前
campaigns = db.execute(text("SELECT * FROM table")).fetchall()

# 修正後
result = db.execute(text("SELECT * FROM table"))
campaigns = result.mappings().all()
```

#### パターン2: fetchone()

```python
# 修正前
campaign = db.execute(text("SELECT * FROM table WHERE id = :id"), {'id': id}).fetchone()

# 修正後
result = db.execute(text("SELECT * FROM table WHERE id = :id"), {'id': id})
campaign = result.mappings().fetchone()
```

## 修正日時

2024年11月20日

## 関連ドキュメント

- [SQLAlchemy 2.0 Migration Guide](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html)
- [SQLAlchemy Result Objects](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.mappings)
- [401エラー無限ループの修正](./FIX_401_INFINITE_LOOP.md)
- [APIドメイン問題の修正](./FIX_API_DOMAIN_ISSUE.md)
