# Repository model 属性エラーの修正

## 問題

バックエンドで以下のエラーが発生していました：

```
[2025-11-20 03:57:19] ERROR services.referral_service: 
Error generating referral code: 'UserRepository' object has no attribute 'model'
```

エンドポイント: `GET /api/v1/referral/code`

## 原因

`backend/services/referral_service.py` で `self.user_repo.model` を使用していましたが、
`BaseRepository` クラスでは属性名が `model_class` になっています。

### BaseRepository の実装

```python
class BaseRepository(Generic[T]):
    def __init__(self, model_class: Type[T], db_session: Session):
        self.model_class = model_class  # ← 正しい属性名
        self.db_session = db_session
```

### 誤った使用例

```python
# 間違い
existing = self.db_session.query(self.user_repo.model).filter_by(...)
```

## 修正内容

### `backend/services/referral_service.py`

#### 修正箇所1: 紹介コード生成時の重複チェック

**修正前:**
```python
# 既存チェック
existing = self.db_session.query(self.user_repo.model).filter_by(referral_code=code).first()
if not existing:
    break
```

**修正後:**
```python
# 既存チェック
existing = self.db_session.query(self.user_repo.model_class).filter_by(referral_code=code).first()
if not existing:
    break
```

#### 修正箇所2: 紹介者の検索

**修正前:**
```python
# 紹介者を検索
referrer = self.db_session.query(self.user_repo.model).filter_by(referral_code=referral_code).first()
if not referrer:
    raise ValueError(f"Invalid referral code: {referral_code}")
```

**修正後:**
```python
# 紹介者を検索
referrer = self.db_session.query(self.user_repo.model_class).filter_by(referral_code=referral_code).first()
if not referrer:
    raise ValueError(f"Invalid referral code: {referral_code}")
```

## Repository パターンの正しい使用方法

### BaseRepository の属性

```python
class BaseRepository(Generic[T]):
    def __init__(self, model_class: Type[T], db_session: Session):
        self.model_class = model_class  # ← モデルクラス
        self.db_session = db_session    # ← DBセッション
```

### 正しい使用例

#### パターン1: Repository のメソッドを使用（推奨）

```python
# 良い例 - Repositoryのメソッドを使用
user = self.user_repo.find_by_id(user_id)
users = self.user_repo.find_all(filters={'is_active': True})
```

#### パターン2: model_class を直接使用

```python
# 良い例 - model_classを使用
user = self.db_session.query(self.user_repo.model_class).filter_by(email=email).first()
```

### 間違った使用例

```python
# 悪い例 - model属性は存在しない
user = self.db_session.query(self.user_repo.model).filter_by(email=email).first()
```

## Repository パターンのベストプラクティス

### 1. Repository メソッドを優先

```python
# 推奨: Repositoryのメソッドを使用
user = self.user_repo.find_by_id(user_id)
users = self.user_repo.find_all(filters={'email': email})
```

### 2. カスタムメソッドを追加

複雑なクエリは Repository にメソッドを追加：

```python
class UserRepository(BaseRepository[User]):
    def find_by_referral_code(self, referral_code: str) -> Optional[User]:
        """紹介コードでユーザーを検索"""
        return self.db_session.query(self.model_class).filter_by(
            referral_code=referral_code
        ).first()
```

使用例：
```python
# 良い例
referrer = self.user_repo.find_by_referral_code(referral_code)
```

### 3. 直接クエリは最小限に

どうしても必要な場合のみ `model_class` を使用：

```python
# 許容される例（複雑なクエリ）
users = self.db_session.query(self.user_repo.model_class).join(
    Wallet
).filter(
    Wallet.balance > 1000
).all()
```

## 影響範囲

この修正により、以下のエンドポイントが正常に動作するようになります：

- ✅ `GET /api/v1/referral/code` - 紹介コード取得
- ✅ `POST /api/v1/referral/register` - 紹介経由登録
- ✅ `GET /api/v1/referral/stats` - 紹介統計取得

## テスト方法

### 1. 紹介コード取得のテスト

```bash
# 認証トークンを取得してから
curl -X GET https://api.airz.one/api/v1/referral/code \
  -H "Authorization: Bearer $TOKEN"

# 期待される結果: 200 OK
# {
#   "status": "success",
#   "data": {
#     "referral_code": "ABC12345",
#     "referral_link": "https://airz.one/register?ref=ABC12345",
#     ...
#   }
# }
```

### 2. ログの確認

```bash
# バックエンドログを確認
tail -f /var/log/apache2/error.log

# エラーがないことを確認
# "object has no attribute 'model'" エラーが出ないこと
```

## 関連ファイル

- `backend/services/referral_service.py` - 紹介サービス（修正）
- `backend/repositories/base.py` - ベースリポジトリ（参照）
- `backend/repositories/user_repository.py` - ユーザーリポジトリ（参照）

## 今後の開発

Repository を使用する際の注意点：

### DO（推奨）

```python
# ✅ Repositoryのメソッドを使用
user = user_repo.find_by_id(user_id)

# ✅ model_classを使用
user = db.query(user_repo.model_class).filter_by(email=email).first()

# ✅ カスタムメソッドを追加
class UserRepository(BaseRepository[User]):
    def find_by_email(self, email: str) -> Optional[User]:
        return self.db_session.query(self.model_class).filter_by(email=email).first()
```

### DON'T（非推奨）

```python
# ❌ 存在しない属性を使用
user = db.query(user_repo.model).filter_by(email=email).first()

# ❌ 直接SQLを多用
user = db.execute("SELECT * FROM users WHERE email = :email", {'email': email}).first()

# ❌ Repositoryを経由せずに直接モデルを使用
from models.user import User
user = db.query(User).filter_by(email=email).first()  # Repositoryを使うべき
```

## 本番環境での重要な原則

1. **Repository パターンの遵守** - データアクセスは Repository 経由で行う
2. **属性名の確認** - `model_class` が正しい属性名
3. **カスタムメソッドの追加** - 複雑なクエリは Repository にメソッドを追加

## 修正日時

2024年11月20日

## 関連ドキュメント

- [SQLAlchemy text() エラーの修正](./FIX_SQLALCHEMY_TEXT_ERROR.md)
- [401エラー無限ループの修正](./FIX_401_INFINITE_LOOP.md)
- [APIドメイン問題の修正](./FIX_API_DOMAIN_ISSUE.md)
