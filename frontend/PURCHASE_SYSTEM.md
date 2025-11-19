# 購入システム実装ガイド

## 概要

Airzoneの購入システムは、3種類の商品タイプと4種類の購入制限をサポートしています。

## 商品タイプ

### 1. NFT (`product_type: 'nft'`)
- デジタルNFTの販売
- 購入後、自動的にXRPL上でミントされ、ユーザーのウォレットに送信
- 配送方法: `digital`

### 2. グッズ (`product_type: 'goods'`)
- 物理的な商品の販売
- 2つの配送方法を選択可能：
  - **現地受け取り** (`delivery_method: 'pickup'`)
    - 購入後、QRコードが生成される
    - 会場でQRコードを提示して商品を受け取る
  - **配送** (`delivery_method: 'shipping'`)
    - 配送先住所を入力
    - 宅配便で商品が届く
    - 配送希望時間帯を選択可能

### 3. 公演NFTチケット (`product_type: 'event_ticket'`)
- イベントチケットの抽選販売
- NFTとして発行される
- イベント日時と会場情報を含む
- 配送方法: `digital`

## 購入制限

### 1. 現地参加者のみ (`purchase_restriction: 'onsite_only'`)
- OpenNDS経由でWiFiに接続したユーザーのみ購入可能
- クッキー: `airzone_onsite`
- 使用例: 会場限定グッズ

### 2. 現地参加者と紹介者 (`purchase_restriction: 'onsite_and_referral'`)
- 現地参加者または紹介リンクから来たユーザーが購入可能
- クッキー: `airzone_onsite` または `airzone_referral`
- 使用例: 限定商品の販売拡大

### 3. NFT保有者のみ (`purchase_restriction: 'nft_holders'`)
- 指定のNFTを保有しているユーザーのみ購入可能
- `required_nft_id`で指定されたNFTをチェック
- 使用例: NFT保有者限定特典

### 4. 誰でも購入可 (`purchase_restriction: 'public'`)
- 制限なし、ログインしているユーザーなら誰でも購入可能
- 使用例: 一般販売商品

## データベーススキーマ

### products テーブル
```sql
CREATE TABLE products (
  id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  price DECIMAL(10, 2) NOT NULL,
  stock_quantity INTEGER NOT NULL DEFAULT 0,
  image_url TEXT,
  product_type VARCHAR(50) NOT NULL, -- 'nft', 'goods', 'event_ticket'
  delivery_method VARCHAR(50), -- 'pickup', 'shipping', 'digital'
  purchase_restriction VARCHAR(50) NOT NULL, -- 'onsite_only', 'onsite_and_referral', 'nft_holders', 'public'
  required_nft_id UUID, -- NFT保有者限定の場合に使用
  event_date TIMESTAMP, -- イベントチケットの場合
  venue TEXT, -- イベントチケットの場合
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### order_items テーブル
```sql
CREATE TABLE order_items (
  id UUID PRIMARY KEY,
  order_id UUID NOT NULL REFERENCES orders(id),
  product_id UUID NOT NULL REFERENCES products(id),
  quantity INTEGER NOT NULL,
  unit_price DECIMAL(10, 2) NOT NULL,
  subtotal DECIMAL(10, 2) NOT NULL,
  delivery_method VARCHAR(50), -- 'pickup', 'shipping', 'digital'
  shipping_address JSONB, -- 配送の場合の住所情報
  pickup_qr_code TEXT, -- 現地受け取りの場合のQRコード
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### shipping_address の構造
```json
{
  "recipient_name": "山田 太郎",
  "postal_code": "123-4567",
  "prefecture": "東京都",
  "city": "渋谷区",
  "address_line1": "道玄坂1-2-3",
  "address_line2": "〇〇ビル 101号室",
  "phone_number": "090-1234-5678",
  "delivery_time_preference": "午前中（8:00-12:00）"
}
```

## フロントエンド実装

### 購入フロー

#### 1. 商品選択
```typescript
// 商品カードで購入制限をチェック
const purchaseCheck = canPurchaseProduct(product, userNFTs, isAuthenticated);

if (!purchaseCheck.canPurchase) {
  // 購入不可の理由を表示
  alert(purchaseCheck.reason);
}
```

#### 2. カートに追加
```typescript
// グッズの場合、配送方法を選択
if (product.product_type === 'goods') {
  // ユーザーに配送方法を選択させる
  const deliveryMethod = await selectDeliveryMethod();
  
  if (deliveryMethod === 'shipping') {
    // 配送先住所を入力
    const address = await getShippingAddress();
    addToCart(product, quantity, deliveryMethod, address);
  } else {
    // 現地受け取り
    addToCart(product, quantity, 'pickup');
  }
} else {
  // NFTまたはチケット
  addToCart(product, quantity, 'digital');
}
```

#### 3. チェックアウト
```typescript
// 注文を作成
const order = await createOrder({
  items: cartItems.map(item => ({
    product_id: item.product.id,
    quantity: item.quantity,
    delivery_method: item.deliveryMethod,
    shipping_address: item.shippingAddress,
  })),
});

// 支払い処理
await processPayment(order.id);
```

#### 4. 注文完了後
```typescript
// NFTの場合: 自動ミント
if (product.product_type === 'nft' || product.product_type === 'event_ticket') {
  await mintNFTForOrder(order.id);
}

// 現地受け取りの場合: QRコード生成
if (item.delivery_method === 'pickup') {
  const qrCode = generatePickupQRCode(order.id, item.id);
  // QRコードを表示
}

// 配送の場合: 配送状況を追跡
if (item.delivery_method === 'shipping') {
  // 配送追跡情報を表示
}
```

## 管理画面での設定

### 商品作成時の設定項目

1. **基本情報**
   - 商品名
   - 説明
   - 価格
   - 在庫数
   - 画像

2. **商品タイプ**
   - NFT / グッズ / 公演NFTチケット

3. **配送方法**（グッズの場合のみ）
   - 現地受け取り / 配送

4. **購入制限**
   - 現地参加者のみ
   - 現地参加者と紹介者
   - NFT保有者のみ（NFT IDを指定）
   - 誰でも購入可

5. **イベント情報**（チケットの場合のみ）
   - イベント日時
   - 会場

## セキュリティ考慮事項

### クッキーの設定
```typescript
// OpenNDS経由でWiFi接続時
Cookies.set('airzone_onsite', 'true', {
  expires: 1, // 1日
  secure: true,
  sameSite: 'strict',
});

// 紹介リンクからアクセス時
Cookies.set('airzone_referral', referralCode, {
  expires: 30, // 30日
  secure: true,
  sameSite: 'strict',
});
```

### QRコードの検証
```typescript
// QRコードには以下の情報を含める
const qrData = {
  order_id: 'uuid',
  item_id: 'uuid',
  type: 'pickup',
  timestamp: Date.now(),
};

// 会場でスキャン時に検証
// - 注文IDとアイテムIDが一致するか
// - タイムスタンプが有効期間内か
// - すでに受け取り済みでないか
```

## テスト項目

### 購入制限のテスト
- [ ] 現地参加者のみ: クッキーなしで購入不可
- [ ] 現地参加者と紹介者: 両方のクッキーで購入可能
- [ ] NFT保有者のみ: NFTなしで購入不可
- [ ] 誰でも購入可: ログインユーザーなら購入可能

### 配送方法のテスト
- [ ] 現地受け取り: QRコード生成
- [ ] 配送: 住所入力フォーム表示
- [ ] NFT: 自動ミント

### エラーハンドリング
- [ ] 在庫切れ
- [ ] 購入制限違反
- [ ] 決済失敗
- [ ] NFTミント失敗
