# 支払いシステムガイド

## 概要

Airzoneでは、2つの支払い方法をサポートしています：
1. **Stripe** - クレジットカード決済
2. **XRPL** - XRP暗号通貨決済

## 実装されたコンポーネント

### 1. PaymentMethodSelector
支払い方法を選択するコンポーネント

**場所**: `frontend/components/shop/PaymentMethodSelector.tsx`

**機能**:
- Stripeとxrplの選択UI
- 各支払い方法の説明表示
- 選択状態の管理

### 2. XRPLPaymentForm
XRPL決済フォーム

**場所**: `frontend/components/shop/XRPLPaymentForm.tsx`

**機能**:
- XRP換算額の表示
- ウォレット情報の表示
- トランザクション詳細の表示
- XRP決済の実行

### 3. CheckoutForm（既存）
Stripe決済フォーム

**場所**: `frontend/components/shop/CheckoutForm.tsx`

**機能**:
- Stripe Elements統合
- クレジットカード決済
- 3Dセキュア対応

## 支払いフロー

### Stripe決済フロー

```
1. カートから注文確定
   ↓
2. 注文作成（Order作成）
   ↓
3. 支払い方法選択（Stripe）
   ↓
4. Payment Intent作成
   ↓
5. Stripe Elements表示
   ↓
6. カード情報入力
   ↓
7. 決済実行
   ↓
8. 注文完了ページへリダイレクト
   ↓
9. NFT自動ミント
```

### XRPL決済フロー

```
1. カートから注文確定
   ↓
2. 注文作成（Order作成）
   ↓
3. 支払い方法選択（XRPL）
   ↓
4. XRP換算額表示
   ↓
5. ウォレット確認
   ↓
6. XRP決済実行
   ↓
7. トランザクション送信
   ↓
8. 注文完了ページへリダイレクト
   ↓
9. NFT自動ミント
```

## バックエンドAPI実装（必要）

### XRPL決済エンドポイント

```php
// admin/routes/api.php
Route::post('/payments/xrpl', [PaymentController::class, 'processXRPLPayment']);
```

```php
// admin/app/Http/Controllers/PaymentController.php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Order;
use App\Models\Payment;
use App\Services\XRPLService;

class PaymentController extends Controller
{
    protected $xrplService;

    public function __construct(XRPLService $xrplService)
    {
        $this->xrplService = $xrplService;
    }

    public function processXRPLPayment(Request $request)
    {
        $validated = $request->validate([
            'order_id' => 'required|uuid',
            'wallet_address' => 'required|string',
            'amount_xrp' => 'required|numeric|min:0',
        ]);

        try {
            // 注文を取得
            $order = Order::findOrFail($validated['order_id']);

            // ユーザーの確認
            if ($order->user_id !== auth()->id()) {
                return response()->json([
                    'error' => '権限がありません'
                ], 403);
            }

            // XRP決済を処理
            $transaction = $this->xrplService->processPayment(
                $validated['wallet_address'],
                $validated['amount_xrp'],
                $order->id
            );

            // 支払いレコードを作成
            $payment = Payment::create([
                'order_id' => $order->id,
                'payment_method' => 'xrpl',
                'amount' => $order->total_amount,
                'currency' => 'JPY',
                'xrp_amount' => $validated['amount_xrp'],
                'transaction_hash' => $transaction['hash'],
                'status' => 'succeeded',
            ]);

            // 注文ステータスを更新
            $order->update(['status' => 'completed']);

            return response()->json([
                'success' => true,
                'payment' => $payment,
                'transaction' => $transaction,
            ]);

        } catch (\Exception $e) {
            \Log::error('XRPL Payment Error', [
                'error' => $e->getMessage(),
                'order_id' => $validated['order_id'],
            ]);

            return response()->json([
                'error' => 'XRP決済の処理に失敗しました',
                'message' => $e->getMessage(),
            ], 500);
        }
    }
}
```

### XRPLサービス

```php
// admin/app/Services/XRPLService.php
<?php

namespace App\Services;

use XRPL\Client;
use XRPL\Wallet;

class XRPLService
{
    protected $client;
    protected $sponsorWallet;

    public function __construct()
    {
        $network = config('xrpl.network', 'testnet');
        $this->client = new Client($network);
        
        // スポンサーウォレット（受取用）
        $this->sponsorWallet = new Wallet(
            config('xrpl.sponsor_seed')
        );
    }

    public function processPayment($fromAddress, $amountXRP, $orderId)
    {
        // XRPLトランザクションを作成
        $payment = [
            'TransactionType' => 'Payment',
            'Account' => $fromAddress,
            'Destination' => $this->sponsorWallet->address,
            'Amount' => $this->xrpToDrops($amountXRP),
            'Memos' => [
                [
                    'Memo' => [
                        'MemoType' => $this->stringToHex('order_id'),
                        'MemoData' => $this->stringToHex($orderId),
                    ]
                ]
            ]
        ];

        // トランザクションを送信
        $result = $this->client->submitTransaction($payment);

        if ($result['result']['meta']['TransactionResult'] !== 'tesSUCCESS') {
            throw new \Exception('Transaction failed: ' . $result['result']['meta']['TransactionResult']);
        }

        return [
            'hash' => $result['result']['hash'],
            'ledger_index' => $result['result']['ledger_index'],
            'validated' => $result['result']['validated'],
        ];
    }

    protected function xrpToDrops($xrp)
    {
        return (string)($xrp * 1000000);
    }

    protected function stringToHex($string)
    {
        return strtoupper(bin2hex($string));
    }
}
```

## データベーススキーマ

### payments テーブルの更新

```sql
ALTER TABLE payments ADD COLUMN payment_method VARCHAR(50) DEFAULT 'stripe';
ALTER TABLE payments ADD COLUMN xrp_amount DECIMAL(20, 6) NULL;
ALTER TABLE payments ADD COLUMN transaction_hash VARCHAR(255) NULL;
```

または新しいマイグレーション:

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up()
    {
        Schema::table('payments', function (Blueprint $table) {
            $table->string('payment_method', 50)->default('stripe')->after('order_id');
            $table->decimal('xrp_amount', 20, 6)->nullable()->after('amount');
            $table->string('transaction_hash')->nullable()->after('xrp_amount');
        });
    }

    public function down()
    {
        Schema::table('payments', function (Blueprint $table) {
            $table->dropColumn(['payment_method', 'xrp_amount', 'transaction_hash']);
        });
    }
};
```

## 設定

### 環境変数

```env
# .env

# Stripe
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# XRPL
XRPL_NETWORK=testnet
XRPL_SPONSOR_SEED=sXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XRPL_SPONSOR_ADDRESS=rXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# XRP/JPY レート（実際にはAPIから取得）
XRP_JPY_RATE=150
```

### フロントエンド環境変数

```env
# frontend/.env.local

NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
NEXT_PUBLIC_XRPL_NETWORK=testnet
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## テスト

### Stripe決済のテスト

テストカード番号:
- 成功: `4242 4242 4242 4242`
- 3Dセキュア: `4000 0027 6000 3184`
- 失敗: `4000 0000 0000 0002`

有効期限: 任意の未来の日付
CVC: 任意の3桁

### XRPL決済のテスト

1. Testnetウォレットを作成
2. Testnet Faucetから XRP を取得
   - https://xrpl.org/xrp-testnet-faucet.html
3. 決済をテスト

## トラブルシューティング

### Stripe決済が失敗する

**確認事項**:
1. Stripe APIキーが正しいか
2. Payment Intentが正しく作成されているか
3. ネットワークエラーがないか

**ログ確認**:
```bash
# Laravelログ
tail -f admin/storage/logs/laravel.log

# ブラウザコンソール
# F12 → Console タブ
```

### XRPL決済が失敗する

**確認事項**:
1. ウォレットに十分なXRPがあるか（最低10 XRP + 手数料）
2. ネットワーク接続が正常か
3. トランザクションハッシュが記録されているか

**デバッグ**:
```javascript
// ブラウザコンソールで
console.log('Wallet:', wallet);
console.log('Amount XRP:', amountXRP);
```

## セキュリティ

### Stripe
- APIキーは環境変数で管理
- Payment Intentは サーバーサイドで作成
- Webhook署名を検証

### XRPL
- 秘密鍵はサーバーサイドのみで管理
- トランザクションの検証
- メモフィールドで注文IDを記録

## まとめ

2つの支払い方法を実装することで、ユーザーは好みの方法で決済できます：

- **Stripe**: 従来のクレジットカード決済、使いやすい
- **XRPL**: 暗号通貨決済、低手数料、即時決済

両方の方法で、決済完了後に自動的にNFTがミントされます。
