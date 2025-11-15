# 効果測定ダッシュボード

## 概要

管理パネルに効果測定機能を追加しました。DAU、MAU、ダウンロード数などの主要指標をリアルタイムで確認できます。

## 主要指標

### 1. DAU (Daily Active Users)
- **定義**: 本日ログインしたユニークユーザー数
- **計測方法**: `user_activities`テーブルの`login`アクティビティを集計
- **表示**: 本日の値

### 2. MAU (Monthly Active Users)
- **定義**: 今月ログインしたユニークユーザー数
- **計測方法**: `user_activities`テーブルの`login`アクティビティを集計
- **表示**: 今月の値

### 3. ダウンロード数
- **定義**: 商品のダウンロード回数
- **計測方法**: `user_activities`テーブルの`download`アクティビティを集計
- **表示**: 
  - 本日のダウンロード数
  - 総ダウンロード数

### 4. エンゲージメント率
- **定義**: DAU/MAU比率（%）
- **計算式**: `(DAU / MAU) × 100`
- **意味**: ユーザーの定着率を示す指標

## トレンドグラフ

### DAU推移
- 過去7日間のDAU推移を棒グラフで表示
- 日付とユーザー数を表示

### ダウンロード推移
- 過去7日間のダウンロード数推移を棒グラフで表示
- 日付とダウンロード数を表示

## データ収集

### バックエンドAPI

以下のエンドポイントで自動的にアクティビティを記録：

#### 1. ログイン
```
POST /api/v1/auth/google
```
- ログイン成功時に`login`アクティビティを記録
- IPアドレスとUser-Agentも保存

#### 2. ダウンロード
```
POST /api/v1/downloads/product/{product_id}
```
- 商品ダウンロード時に呼び出す
- `download`アクティビティを記録
- 商品IDをメタデータに保存

#### 3. 購入
```
POST /api/v1/orders
```
- 注文作成時に`purchase`アクティビティを記録
- 注文IDと金額をメタデータに保存

### フロントエンド実装例

```typescript
// ダウンロード時の実装例
async function downloadProduct(productId: string) {
  try {
    // ダウンロード処理
    const response = await fetch(`/api/v1/downloads/product/${productId}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
      },
    });
    
    if (response.ok) {
      // 実際のファイルダウンロード処理
      // ...
    }
  } catch (error) {
    console.error('Download failed:', error);
  }
}
```

## データベーススキーマ

```sql
CREATE TABLE user_activities (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    activity_type VARCHAR(255) NOT NULL,
    ip_address VARCHAR(255) NULL,
    user_agent VARCHAR(255) NULL,
    metadata JSON NULL,
    created_at TIMESTAMP NOT NULL,
    INDEX idx_user_created (user_id, created_at),
    INDEX idx_activity_created (activity_type, created_at)
);
```

## セットアップ

### 1. データベースマイグレーション

```bash
cd admin
php artisan migrate
```

### 2. バックエンド設定

`.env`ファイルにデータベース接続情報が設定されていることを確認：

```env
DB_HOST=localhost
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=airzone
```

### 3. 管理パネルアクセス

```
http://your-domain/admin
```

ログイン後、ダッシュボードに効果測定指標が表示されます。

## 今後の拡張案

- コンバージョン率の追加
- ユーザー属性別の分析
- リテンション率の計測
- ファネル分析
- A/Bテスト機能
- エクスポート機能（CSV/Excel）
- カスタム期間指定
- リアルタイム更新
