# XRPL実装検証ドキュメント

## 概要

このドキュメントは、AirzoneプラットフォームがXRPL（XRP Ledger）ブロックチェーンを**実際に**使用していることを証明します。

**重要な原則:**
- ダミーデータやモックは使用しない
- すべてのブロックチェーン操作は実際のXRPLに対して実行される
- データベースだけでブロックチェーンデータを管理しない

## XRPL統合の実装

### 1. XRPLクライアント (`backend/clients/xrpl_client.py`)

#### 実装内容

```python
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import NFTokenMint, Payment, EscrowCreate, EscrowFinish
from xrpl.transaction import submit_and_wait
from xrpl.models.requests import AccountNFTs, AccountInfo
```

#### 実際のブロックチェーン接続

```python
# Testnet接続
self.client = JsonRpcClient("https://s.altnet.rippletest.net:51234")

# Mainnet接続
self.client = JsonRpcClient("https://xrplcluster.com")
```

これらは**実際のXRPLノード**への接続です。

### 2. 実装されている機能

#### 2.1 ウォレット生成

```python
def generate_wallet(self) -> Tuple[str, str]:
    """
    Generate a new XRPL wallet with address and seed.
    実際のXRPLウォレットを生成（ダミーではない）
    """
    wallet = Wallet.create()
    address = wallet.classic_address
    seed = wallet.seed
    return (address, seed)
```

**検証方法:**
- 生成されたアドレスは `r` で始まる25-35文字
- XRPLエクスプローラーで確認可能: https://testnet.xrpl.org/

#### 2.2 NFTミント

```python
def mint_nft(
    self,
    recipient_address: str,
    nft_uri: str,
    transfer_fee: int = 0,
    flags: int = 8
) -> Dict:
    """
    Mint an NFT on the XRPL blockchain.
    実際のXRPLブロックチェーン上でNFTをミント
    """
    # NFTokenMintトランザクションを作成
    mint_tx = NFTokenMint(
        account=issuer_wallet.classic_address,
        uri=xrpl.utils.str_to_hex(nft_uri),
        flags=flags,
        transfer_fee=transfer_fee,
        nftoken_taxon=0
    )
    
    # 実際のブロックチェーンに送信
    response = submit_and_wait(mint_tx, self.client, issuer_wallet)
    
    # トランザクションハッシュを返す
    return {
        'nft_token_id': nft_token_id,
        'transaction_hash': tx_hash,
        'issuer': issuer_wallet.classic_address
    }
```

**検証方法:**
- トランザクションハッシュでXRPLエクスプローラーで確認
- NFT Token IDでNFTの存在を確認
- `get_account_nfts()` で実際のブロックチェーンから取得

#### 2.3 残高確認

```python
def get_wallet_balance(self, address: str) -> int:
    """
    Get the XRP balance for a wallet address.
    実際のXRPLブロックチェーンから残高を取得
    """
    account_info = AccountInfo(account=address)
    response = self.client.request(account_info)
    
    if response.is_successful():
        balance = int(response.result['account_data']['Balance'])
        return balance
    return 0
```

**検証方法:**
- XRPLエクスプローラーで同じアドレスの残高を確認
- 値が一致することを確認

#### 2.4 NFT所有権確認

```python
def verify_nft_ownership(self, wallet_address: str, nft_token_id: str) -> bool:
    """
    Verify if a wallet owns a specific NFT.
    実際のXRPLブロックチェーンでNFT所有権を確認
    """
    nfts = self.get_account_nfts(wallet_address)
    
    for nft in nfts:
        if nft.get('NFTokenID') == nft_token_id:
            return True
    
    return False
```

**検証方法:**
- XRPLエクスプローラーでNFT所有権を確認
- 結果が一致することを確認

#### 2.5 Escrow（ステーキング）

```python
def create_escrow(
    self,
    sender_wallet_seed: str,
    recipient_address: str,
    amount_drops: int,
    finish_after: int
) -> Dict:
    """
    Escrowを作成（XRPをロック）
    実際のXRPLブロックチェーン上でEscrowを作成
    """
    escrow_tx = EscrowCreate(
        account=sender_wallet.classic_address,
        destination=recipient_address,
        amount=str(amount_drops),
        finish_after=finish_after
    )
    
    response = submit_and_wait(escrow_tx, self.client, sender_wallet)
    
    return {
        'transaction_hash': tx_hash,
        'escrow_sequence': escrow_sequence
    }
```

**検証方法:**
- XRPLエクスプローラーでEscrowトランザクションを確認
- Escrow Sequenceで状態を確認

#### 2.6 バッチ送金（Batch Transactions）

```python
def batch_send_xrp(
    self,
    sender_wallet_seed: str,
    recipients: list,
    memo: Optional[str] = None
) -> Dict:
    """
    XRPLのBatch Transactions機能を使って複数のユーザーに一括でXRPを送信
    
    参考: https://xrpl.org/docs/concepts/transactions/batch-transactions
    """
    # Step 1: Ticketを作成
    ticket_create_tx = TicketCreate(
        account=sender_wallet.classic_address,
        ticket_count=num_recipients
    )
    
    ticket_response = submit_and_wait(ticket_create_tx, self.client, sender_wallet)
    
    # Step 2: 各受取人へのPaymentトランザクションを並列送信
    for recipient, ticket_seq in zip(recipients, ticket_sequences):
        payment_tx = Payment(
            account=sender_wallet.classic_address,
            destination=recipient['address'],
            amount=str(amount_drops),
            ticket_sequence=ticket_seq,
            sequence=0
        )
        
        signed_tx = autofill_and_sign(payment_tx, self.client, sender_wallet)
        tx_response = send_reliable_submission(signed_tx, self.client)
```

**検証方法:**
- 各トランザクションハッシュでXRPLエクスプローラーで確認
- Ticket Sequenceで並列実行を確認

## テスト方法

### 1. XRPL統合テストの実行

```bash
cd backend
python tests/test_xrpl_integration.py
```

このテストは以下を確認します：
- ✅ XRPLへの接続
- ✅ ウォレット生成
- ✅ 残高確認（実際のブロックチェーン問い合わせ）
- ✅ NFT問い合わせ（実際のブロックチェーン問い合わせ）
- ✅ スポンサーウォレットの健全性

### 2. 手動検証

#### ステップ1: ウォレット生成

```bash
cd backend
python -c "from clients.xrpl_client import XRPLClient; client = XRPLClient('testnet'); address, seed = client.generate_wallet(); print(f'Address: {address}')"
```

#### ステップ2: XRPLエクスプローラーで確認

生成されたアドレスをXRPLエクスプローラーで検索：
- Testnet: https://testnet.xrpl.org/
- Mainnet: https://livenet.xrpl.org/

#### ステップ3: NFTミント後の確認

NFTミント後、トランザクションハッシュでXRPLエクスプローラーを確認：

```
https://testnet.xrpl.org/transactions/{transaction_hash}
```

## XRPLJapanサンプルコードとの互換性

参考: https://github.com/XRPLJapan/xrpl-sample-code

### 使用しているXRPL Python SDK

```python
# requirements.txt
xrpl-py>=2.0.0
```

### 実装パターン

XRPLJapanのサンプルコードと同じパターンを使用：

1. **クライアント初期化**
```python
from xrpl.clients import JsonRpcClient
client = JsonRpcClient("https://s.altnet.rippletest.net:51234")
```

2. **ウォレット生成**
```python
from xrpl.wallet import Wallet
wallet = Wallet.create()
```

3. **トランザクション送信**
```python
from xrpl.transaction import submit_and_wait
response = submit_and_wait(transaction, client, wallet)
```

4. **アカウント情報取得**
```python
from xrpl.models.requests import AccountInfo
account_info = AccountInfo(account=address)
response = client.request(account_info)
```

## ダミーデータを使用していないことの証明

### 1. データベースとブロックチェーンの分離

```python
# NFTサービス (backend/services/nft_service.py)

def mint_nft_for_order(self, order_id: str) -> Dict:
    """
    注文に対してNFTをミント
    """
    # Step 1: データベースからデータを取得
    order = self.order_repo.find_by_id(order_id)
    wallet = self.wallet_repo.find_by_user_id(order.user_id)
    
    # Step 2: 実際のXRPLブロックチェーンでNFTをミント
    result = self.xrpl_client.mint_nft(
        recipient_address=wallet.address,
        nft_uri=nft_uri,
        transfer_fee=0,
        flags=8
    )
    
    # Step 3: ブロックチェーンの結果をデータベースに保存
    nft_mint = self.nft_repo.create(
        user_id=order.user_id,
        wallet_address=wallet.address,
        nft_object_id=result['nft_token_id'],  # ブロックチェーンから取得
        transaction_digest=result['transaction_hash'],  # ブロックチェーンから取得
        status='completed',
        metadata=nft_metadata
    )
    
    return result
```

### 2. NFT所有権確認

```python
def verify_nft_requirement(self, user_id: str, required_nft_id: str) -> bool:
    """
    NFT所有権を確認（実際のブロックチェーンで確認）
    """
    wallet = self.wallet_repo.find_by_user_id(user_id)
    
    # データベースではなく、実際のXRPLブロックチェーンで確認
    owns_nft = self.xrpl_client.verify_nft_ownership(
        wallet.address,
        required_nft_id
    )
    
    return owns_nft
```

### 3. 残高確認

```python
def get_wallet_balance(self, user_id: str) -> int:
    """
    ウォレット残高を取得（実際のブロックチェーンから）
    """
    wallet = self.wallet_repo.find_by_user_id(user_id)
    
    # データベースではなく、実際のXRPLブロックチェーンから取得
    balance = self.xrpl_client.get_wallet_balance(wallet.address)
    
    return balance
```

## トラブルシューティング

### 問題: トランザクションが失敗する

**確認事項:**
1. スポンサーウォレットの残高を確認
```bash
python tests/test_xrpl_integration.py
```

2. XRPLネットワークの状態を確認
- Testnet: https://xrpl.org/xrp-testnet-faucet.html
- Status: https://status.xrpl.org/

### 問題: NFTが表示されない

**確認事項:**
1. トランザクションハッシュでXRPLエクスプローラーを確認
2. NFT Token IDが正しいか確認
3. ウォレットアドレスが正しいか確認

### 問題: 残高が0

**Testnetの場合:**
```bash
# Faucetから資金を取得
# https://xrpl.org/xrp-testnet-faucet.html
# スポンサーアドレスを入力
```

## 本番環境での注意事項

### 1. ネットワーク設定

```python
# .env
XRPL_NETWORK=mainnet  # 本番環境
XRPL_SPONSOR_SEED=sXXXXXXXXXXXXXXXXXXXXXXXXXXXX  # 本番用シード
```

### 2. セキュリティ

- スポンサーシードは絶対に公開しない
- 環境変数で管理
- 定期的にバックアップ

### 3. モニタリング

```python
# スポンサーウォレットの健全性を定期的にチェック
health = xrpl_client.check_sponsor_health()
if not health['healthy']:
    # アラートを送信
    send_alert(health['warnings'])
```

## まとめ

Airzoneプラットフォームは、以下の方法で**実際のXRPLブロックチェーン**を使用しています：

1. ✅ **実際のXRPLノードに接続** - ダミーサーバーではない
2. ✅ **実際のトランザクションを送信** - モックではない
3. ✅ **実際のブロックチェーンデータを取得** - データベースだけではない
4. ✅ **XRPLエクスプローラーで検証可能** - すべてのトランザクションが確認可能
5. ✅ **XRPLJapanのサンプルコードと互換** - 標準的な実装パターン

すべてのブロックチェーン操作は、実際のXRPL上で実行され、トランザクションハッシュで検証可能です。

## 関連ドキュメント

- [XRPL公式ドキュメント](https://xrpl.org/)
- [XRPLJapanサンプルコード](https://github.com/XRPLJapan/xrpl-sample-code)
- [XRPL Python SDK](https://xrpl-py.readthedocs.io/)
- [XRPLエクスプローラー](https://livenet.xrpl.org/)
