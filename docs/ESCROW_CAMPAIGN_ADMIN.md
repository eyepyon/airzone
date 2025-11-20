# エスクローキャンペーン管理画面

## 概要

エスクローキャンペーンを管理するための管理画面を実装しました。

## 実装内容

### 1. コントローラー

**ファイル**: `admin/app/Http/Controllers/Admin/EscrowCampaignController.php`

以下の機能を実装：
- `index()` - キャンペーン一覧表示
- `create()` - 新規作成フォーム表示
- `store()` - キャンペーン作成処理
- `show($id)` - キャンペーン詳細表示（参加者一覧含む）
- `edit($id)` - 編集フォーム表示
- `update($id)` - キャンペーン更新処理
- `destroy($id)` - キャンペーン削除処理
- `stats()` - 統計情報表示

### 2. ビューファイル

#### キャンペーン一覧 (`index.blade.php`)
- キャンペーン一覧をテーブル表示
- 最小金額、ロック期間、NFT報酬、参加者数などを表示
- 新規作成、統計、詳細、編集、削除ボタン

#### 新規作成 (`create.blade.php`)
- キャンペーン名、説明
- 最小金額（XRP）、ロック期間（日）、最大参加者数
- 開始日時、終了日時
- NFT報酬（名前、説明、画像URL）
- ステータス（有効/無効）

#### 編集 (`edit.blade.php`)
- 作成フォームと同じ項目を編集可能

#### 詳細 (`show.blade.php`)
- キャンペーン情報の詳細表示
- NFT報酬情報（画像含む）
- 参加者一覧（ユーザー名、ウォレットアドレス、ステーク金額、ステータスなど）

#### 統計 (`stats.blade.php`)
- 総キャンペーン数、有効キャンペーン数
- 総ステーク数、アクティブステーク数、完了ステーク数
- 総ロック額（XRP）
- キャンペーン別統計（ステーク数、完了率、ロック中XRPなど）

### 3. ルート設定

**ファイル**: `admin/routes/web.php`

```php
Route::prefix('escrow-campaigns')->name('admin.escrow-campaigns.')->group(function () {
    Route::get('/', [EscrowCampaignController::class, 'index'])->name('index');
    Route::get('/create', [EscrowCampaignController::class, 'create'])->name('create');
    Route::post('/', [EscrowCampaignController::class, 'store'])->name('store');
    Route::get('/stats', [EscrowCampaignController::class, 'stats'])->name('stats');
    Route::get('/{id}', [EscrowCampaignController::class, 'show'])->name('show');
    Route::get('/{id}/edit', [EscrowCampaignController::class, 'edit'])->name('edit');
    Route::put('/{id}', [EscrowCampaignController::class, 'update'])->name('update');
    Route::delete('/{id}', [EscrowCampaignController::class, 'destroy'])->name('destroy');
});
```

### 4. ナビゲーションメニュー

**ファイル**: `admin/resources/views/admin/layout.blade.php`

- デスクトップメニューとモバイルメニューに「エスクロー」リンクを追加
- アイコン: `fa-lock`

## 使用方法

### キャンペーン作成

1. 管理画面にログイン
2. ナビゲーションメニューから「エスクロー」をクリック
3. 「新規作成」ボタンをクリック
4. 以下の情報を入力：
   - キャンペーン名（例: XRPステーキングキャンペーン）
   - 説明（例: 100 XRPを30日間ロックすると限定NFTがもらえる！）
   - 最小金額（XRP）（例: 100）
   - ロック期間（日）（例: 30）
   - 最大参加者数（オプション、例: 1000）
   - 開始日時
   - 終了日時
   - NFT報酬名（例: Airzone Staker NFT）
   - NFT報酬説明（例: XRPステーキングキャンペーン参加記念NFT）
   - NFT報酬画像URL（例: https://example.com/nft/staker.png）
   - ステータス（有効/無効）
5. 「作成」ボタンをクリック

### キャンペーン管理

- **一覧表示**: すべてのキャンペーンを一覧表示
- **詳細表示**: キャンペーン情報と参加者一覧を表示
- **編集**: キャンペーン情報を編集
- **削除**: キャンペーンを削除（注意: 参加者がいる場合は慎重に）
- **統計**: 全体統計とキャンペーン別統計を表示

### 統計情報

統計ページでは以下の情報を確認できます：

- **総キャンペーン数**: 登録されているキャンペーンの総数
- **有効キャンペーン数**: 現在有効なキャンペーン数
- **総ステーク数**: すべてのステークの総数
- **アクティブステーク数**: 現在アクティブなステーク数
- **完了ステーク数**: 完了したステーク数
- **総ロック額**: 現在ロックされているXRPの総額
- **キャンペーン別統計**: 各キャンペーンのステーク数、完了率、ロック中XRPなど

## データベーステーブル

### escrow_campaigns

キャンペーン情報を管理するテーブル：

- `id`: キャンペーンID（UUID）
- `name`: キャンペーン名
- `description`: 説明
- `min_amount_drops`: 最小金額（drops単位）
- `lock_days`: ロック期間（日）
- `nft_reward_name`: NFT報酬名
- `nft_reward_description`: NFT報酬説明
- `nft_reward_image_url`: NFT報酬画像URL
- `start_date`: 開始日時
- `end_date`: 終了日時
- `max_participants`: 最大参加者数
- `current_participants`: 現在の参加者数
- `is_active`: 有効フラグ

### escrow_stakes

ユーザーのステーク情報を管理するテーブル：

- `id`: ステークID（UUID）
- `user_id`: ユーザーID
- `campaign_id`: キャンペーンID
- `wallet_address`: ウォレットアドレス
- `amount_drops`: ステーク金額（drops単位）
- `lock_days`: ロック期間（日）
- `finish_after`: 完了予定日時
- `escrow_sequence`: Escrowシーケンス番号
- `transaction_hash`: トランザクションハッシュ
- `status`: ステータス（active/completed/cancelled）
- `nft_awarded`: NFT付与フラグ
- `nft_mint_id`: NFTミントID

## 注意事項

1. **最小金額の単位**: フォームではXRP単位で入力しますが、データベースにはdrops単位（1 XRP = 1,000,000 drops）で保存されます
2. **参加者数の更新**: ユーザーがステークを作成すると、`current_participants`が自動的に増加します
3. **キャンペーンの削除**: 参加者がいるキャンペーンを削除する場合は注意が必要です
4. **日時の形式**: 開始日時と終了日時は `datetime-local` 形式で入力します

## バックエンドAPI連携

フロントエンドからは以下のAPIエンドポイントを使用してキャンペーンにアクセスします：

- `GET /api/v1/escrow/campaigns` - アクティブなキャンペーン一覧取得
- `POST /api/v1/escrow/stake` - ステーク作成
- `GET /api/v1/escrow/my-stakes` - 自分のステーク一覧取得

詳細は `backend/routes/escrow.py` を参照してください。

## 完了

エスクローキャンペーン管理画面の実装が完了しました。管理画面から簡単にキャンペーンを作成・管理できます。
