# NFTミント条件の実装

## 概要

商品購入時のNFT自動ミント機能は、**NFTカテゴリの商品のみ**に適用されます。
グッズやチケットなどの他のカテゴリでは、NFTはミントされません。

## 実装内容

### 1. 商品詳細ページ (`frontend/app/shop/[id]/page.tsx`)

#### NFT購入特典メッセージの表示条件

**表示条件:**
- ユーザーがログインしている
- 商品が購入可能
- **商品カテゴリが `nft` である**

```typescript
{canPurchase && user && (product.category === 'nft' || product.product_type === 'nft') && (
  <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
    <div className="flex items-start">
      <svg className="w-5 h-5 text-blue-600 mt-0.5 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
        <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
      </svg>
      <div>
        <h3 className="text-sm font-semibold text-blue-900">🎁 購入特典</h3>
        <p className="text-xs text-blue-700 mt-1">
          この商品を購入すると、XRPL上でNFTが自動的にミントされ、あなたのウォレットに送信されます。
        </p>
      </div>
    </div>
  </div>
)}
```

### 2. 注文詳細ページ (`frontend/app/orders/[id]/page.tsx`)

#### NFT自動ミントの実行条件

**実行条件:**
- 決済が成功している (`payment=success`)
- 注文ステータスが `completed`
- ウォレットが接続されている
- **注文にNFTカテゴリの商品が含まれている**

```typescript
// Auto-mint NFT after successful payment - NFTカテゴリの商品のみ
useEffect(() => {
  const paymentSuccess = searchParams.get('payment') === 'success';
  
  // 注文にNFTカテゴリの商品が含まれているかチェック
  const hasNFTProduct = order?.items?.some(
    item => item.product?.category === 'nft' || item.product?.product_type === 'nft'
  );
  
  if (paymentSuccess && order && order.status === 'completed' && wallet && hasNFTProduct && !nftMinting && !nftMinted) {
    const autoMintNFT = async () => {
      try {
        setNftMinting(true);
        await mintNFTForOrder(order.id);
        setNftMinted(true);
      } catch (err) {
        console.error('NFT auto-mint failed:', err);
      } finally {
        setNftMinting(false);
      }
    };

    autoMintNFT();
  }
}, [order, wallet, searchParams, nftMinting, nftMinted]);
```

## 商品カテゴリ

### NFTカテゴリ (`nft`)

- NFTが自動的にミントされる
- XRPL上でNFTが作成される
- ユーザーのウォレットに送信される
- 購入特典メッセージが表示される

### グッズカテゴリ (`goods`)

- NFTはミントされない
- 物理的な商品
- 配送方法を選択可能
- 購入特典メッセージは表示されない

### チケットカテゴリ (`event_ticket`)

- NFTはミントされない
- イベント入場チケット
- QRコードが発行される
- 購入特典メッセージは表示されない

## データ構造

### Product型

```typescript
export type ProductType = 'nft' | 'goods' | 'event_ticket';

export interface Product {
  id: string;
  name: string;
  description: string | null;
  price: number;
  stock_quantity: number;
  image_url: string | null;
  category?: string; // 'goods', 'nft', 'ticket'
  product_type?: ProductType; // Optional for backward compatibility
  // ... その他のフィールド
}
```

### カテゴリチェックのロジック

```typescript
// NFTカテゴリかどうかをチェック
const isNFTProduct = product.category === 'nft' || product.product_type === 'nft';

// 注文にNFTカテゴリの商品が含まれているかチェック
const hasNFTProduct = order?.items?.some(
  item => item.product?.category === 'nft' || item.product?.product_type === 'nft'
);
```

## ユーザー体験

### NFTカテゴリの商品を購入する場合

1. **商品詳細ページ**
   - 「🎁 購入特典」メッセージが表示される
   - NFTが自動ミントされることが明示される

2. **決済完了後**
   - 注文詳細ページにリダイレクト
   - 「NFTをミント中...」メッセージが表示される
   - XRPLブロックチェーン上でNFTが作成される

3. **ミント完了後**
   - 「🎉 NFTミント完了！」メッセージが表示される
   - マイNFTページへのリンクが表示される
   - ウォレットにNFTが送信される

### グッズ/チケットカテゴリの商品を購入する場合

1. **商品詳細ページ**
   - NFT購入特典メッセージは表示されない
   - 配送方法や受け取り方法を選択

2. **決済完了後**
   - 注文詳細ページにリダイレクト
   - NFTミント処理は実行されない
   - 配送情報やQRコードが表示される

## バックエンド連携

### NFTミントAPI

```
POST /api/v1/nfts/mint-for-order
```

**リクエスト:**
```json
{
  "order_id": "uuid"
}
```

**処理:**
1. 注文の商品を確認
2. NFTカテゴリの商品のみミント
3. XRPLブロックチェーンでNFTを作成
4. ユーザーのウォレットに送信

## テスト方法

### 1. NFTカテゴリの商品をテスト

```bash
# 商品詳細ページにアクセス
https://airz.one/shop/{nft_product_id}

# 期待される動作:
# - 「🎁 購入特典」メッセージが表示される
# - 購入後、NFTが自動的にミントされる
```

### 2. グッズカテゴリの商品をテスト

```bash
# 商品詳細ページにアクセス
https://airz.one/shop/{goods_product_id}

# 期待される動作:
# - 「🎁 購入特典」メッセージは表示されない
# - 購入後、NFTはミントされない
```

### 3. 混合カートをテスト

```bash
# NFTとグッズを同時にカートに追加
# 購入後、NFTカテゴリの商品のみミントされる
```

## 注意事項

### 本番環境での重要な原則

1. **カテゴリの正確性** - 商品カテゴリは正確に設定する
2. **ブロックチェーン確認** - NFTミントは実際のXRPLで実行される
3. **エラーハンドリング** - ミント失敗時の適切な処理

### 今後の拡張

- カテゴリごとの特典の追加
- NFT以外のデジタル特典
- カスタマイズ可能な特典メッセージ

## 関連ファイル

- `frontend/app/shop/[id]/page.tsx` - 商品詳細ページ
- `frontend/app/orders/[id]/page.tsx` - 注文詳細ページ
- `frontend/types/index.ts` - 型定義
- `backend/services/nft_service.py` - NFTミントサービス

## 修正日時

2024年11月20日

## 関連ドキュメント

- [商品管理機能](../admin/PRODUCT_MANAGEMENT.md)
- [NFTシステム](./NFT_SYSTEM.md)
- [チェックアウトフロー](../frontend/components/shop/CHECKOUT_IMPLEMENTATION.md)
