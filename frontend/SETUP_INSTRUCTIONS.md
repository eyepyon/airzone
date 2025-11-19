# セットアップ手順

## 必要なパッケージのインストール

以下のコマンドを実行して、必要なパッケージをインストールしてください：

```bash
cd frontend
npm install js-cookie qrcode
npm install --save-dev @types/js-cookie @types/qrcode
```

## インストールされるパッケージ

- `js-cookie`: クッキーの読み書きを簡単に行うライブラリ
- `qrcode`: QRコードを生成するライブラリ
- `@types/js-cookie`: js-cookieの型定義
- `@types/qrcode`: qrcodeの型定義

## 新機能

### 1. 商品タイプ
- **NFT**: デジタルNFT
- **グッズ**: 物理的な商品
- **公演NFTチケット**: イベントチケット（抽選）

### 2. 配送方法（グッズの場合）
- **現地受け取り**: QRコードで会場で受け取り
- **配送**: 住所を入力して宅配便で受け取り

### 3. 購入制限
- **現地参加者のみ**: OpenNDS経由（クッキー: `airzone_onsite`）
- **現地参加者と紹介者**: 専用クッキー（`airzone_referral`）
- **NFT保有者のみ**: 指定のNFTを保有している必要がある
- **誰でも購入可**: 制限なし

## 使用方法

### 購入制限のチェック

```typescript
import { canPurchaseProduct } from '@/lib/purchase-restrictions';

const result = canPurchaseProduct(product, userNFTs, isAuthenticated);
if (result.canPurchase) {
  // 購入可能
} else {
  console.log(result.reason); // 購入できない理由
}
```

### 配送先住所フォーム

```typescript
import ShippingAddressForm from '@/components/shop/ShippingAddressForm';

<ShippingAddressForm
  onSubmit={(address) => {
    // 住所を保存
  }}
  onCancel={() => {
    // キャンセル処理
  }}
/>
```

### 受け取りQRコード

```typescript
import PickupQRCode from '@/components/shop/PickupQRCode';

<PickupQRCode
  orderId={order.id}
  orderItemId={item.id}
  productName={product.name}
/>
```
