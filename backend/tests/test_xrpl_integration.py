#!/usr/bin/env python3
"""
XRPL統合テスト - 実際のXRPLブロックチェーンとの接続を確認

このテストは、XRPLクライアントが実際にブロックチェーンと通信していることを確認します。
ダミーデータやモックではなく、実際のXRPL Testnetに接続します。

参考: https://github.com/XRPLJapan/xrpl-sample-code
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from clients.xrpl_client import XRPLClient
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_xrpl_connection():
    """XRPLへの接続をテスト"""
    print("=" * 80)
    print("XRPL接続テスト")
    print("=" * 80)
    
    try:
        # XRPLクライアントを初期化
        xrpl_client = XRPLClient(
            network=Config.XRPL_NETWORK,
            sponsor_seed=Config.XRPL_SPONSOR_SEED
        )
        
        print(f"✓ XRPLクライアント初期化成功")
        print(f"  ネットワーク: {Config.XRPL_NETWORK}")
        print(f"  スポンサーアドレス: {xrpl_client.sponsor_wallet.classic_address if xrpl_client.sponsor_wallet else 'なし'}")
        
        return True
    except Exception as e:
        print(f"✗ XRPLクライアント初期化失敗: {str(e)}")
        return False


def test_wallet_generation():
    """ウォレット生成をテスト"""
    print("\n" + "=" * 80)
    print("ウォレット生成テスト")
    print("=" * 80)
    
    try:
        xrpl_client = XRPLClient(network=Config.XRPL_NETWORK)
        
        # 新しいウォレットを生成
        address, seed = xrpl_client.generate_wallet()
        
        print(f"✓ ウォレット生成成功")
        print(f"  アドレス: {address}")
        print(f"  シード: {seed[:10]}... (セキュリティのため一部のみ表示)")
        
        # アドレスの形式を確認
        if not address.startswith('r'):
            raise Exception("無効なXRPLアドレス形式")
        
        if len(address) < 25 or len(address) > 35:
            raise Exception("XRPLアドレスの長さが不正")
        
        print(f"✓ アドレス形式検証成功")
        
        return True
    except Exception as e:
        print(f"✗ ウォレット生成失敗: {str(e)}")
        return False


def test_balance_check():
    """残高確認をテスト（実際のブロックチェーン問い合わせ）"""
    print("\n" + "=" * 80)
    print("残高確認テスト（実際のXRPLブロックチェーン問い合わせ）")
    print("=" * 80)
    
    try:
        xrpl_client = XRPLClient(
            network=Config.XRPL_NETWORK,
            sponsor_seed=Config.XRPL_SPONSOR_SEED
        )
        
        if not xrpl_client.sponsor_wallet:
            print("⚠ スポンサーウォレットが設定されていません")
            return False
        
        sponsor_address = xrpl_client.sponsor_wallet.classic_address
        
        print(f"スポンサーアドレス: {sponsor_address}")
        print(f"問い合わせ中...")
        
        # 実際のXRPLブロックチェーンに問い合わせ
        balance = xrpl_client.get_wallet_balance(sponsor_address)
        
        print(f"✓ 残高取得成功（実際のブロックチェーンから取得）")
        print(f"  残高: {balance:,} drops")
        print(f"  残高: {balance / 1_000_000:.6f} XRP")
        
        # 残高が0の場合は警告
        if balance == 0:
            print(f"⚠ 警告: 残高が0です")
            print(f"  テストネットの場合、以下のFaucetから資金を取得してください:")
            print(f"  https://xrpl.org/xrp-testnet-faucet.html")
            print(f"  アドレス: {sponsor_address}")
        
        return True
    except Exception as e:
        print(f"✗ 残高確認失敗: {str(e)}")
        return False


def test_nft_query():
    """NFT問い合わせをテスト（実際のブロックチェーン問い合わせ）"""
    print("\n" + "=" * 80)
    print("NFT問い合わせテスト（実際のXRPLブロックチェーン問い合わせ）")
    print("=" * 80)
    
    try:
        xrpl_client = XRPLClient(
            network=Config.XRPL_NETWORK,
            sponsor_seed=Config.XRPL_SPONSOR_SEED
        )
        
        if not xrpl_client.sponsor_wallet:
            print("⚠ スポンサーウォレットが設定されていません")
            return False
        
        sponsor_address = xrpl_client.sponsor_wallet.classic_address
        
        print(f"スポンサーアドレス: {sponsor_address}")
        print(f"問い合わせ中...")
        
        # 実際のXRPLブロックチェーンに問い合わせ
        nfts = xrpl_client.get_account_nfts(sponsor_address)
        
        print(f"✓ NFT取得成功（実際のブロックチェーンから取得）")
        print(f"  NFT数: {len(nfts)}")
        
        if len(nfts) > 0:
            print(f"\n  最初のNFT:")
            first_nft = nfts[0]
            print(f"    NFT ID: {first_nft.get('NFTokenID', 'N/A')}")
            print(f"    URI: {first_nft.get('URI', 'N/A')}")
            print(f"    Issuer: {first_nft.get('Issuer', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"✗ NFT問い合わせ失敗: {str(e)}")
        return False


def test_sponsor_health():
    """スポンサーウォレットの健全性をチェック"""
    print("\n" + "=" * 80)
    print("スポンサーウォレット健全性チェック")
    print("=" * 80)
    
    try:
        xrpl_client = XRPLClient(
            network=Config.XRPL_NETWORK,
            sponsor_seed=Config.XRPL_SPONSOR_SEED
        )
        
        health = xrpl_client.check_sponsor_health()
        
        if health['healthy']:
            print(f"✓ スポンサーウォレットは健全です")
        else:
            print(f"✗ スポンサーウォレットに問題があります")
        
        print(f"\n詳細:")
        print(f"  アドレス: {health.get('sponsor_address', 'N/A')}")
        print(f"  残高: {health.get('balance_xrp', 0):.6f} XRP")
        print(f"  ネットワーク: {health.get('network', 'N/A')}")
        
        if health.get('warnings'):
            print(f"\n警告:")
            for warning in health['warnings']:
                print(f"  - {warning}")
        
        if health.get('recommendations'):
            print(f"\n推奨事項:")
            for rec in health['recommendations']:
                print(f"  - {rec}")
        
        return health['healthy']
    except Exception as e:
        print(f"✗ 健全性チェック失敗: {str(e)}")
        return False


def main():
    """全テストを実行"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "XRPL統合テスト" + " " * 44 + "║")
    print("║" + " " * 15 + "実際のブロックチェーン接続確認" + " " * 32 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    results = {
        'connection': test_xrpl_connection(),
        'wallet_generation': test_wallet_generation(),
        'balance_check': test_balance_check(),
        'nft_query': test_nft_query(),
        'sponsor_health': test_sponsor_health(),
    }
    
    print("\n" + "=" * 80)
    print("テスト結果サマリー")
    print("=" * 80)
    
    for test_name, result in results.items():
        status = "✓ 成功" if result else "✗ 失敗"
        print(f"{test_name:.<50} {status}")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\n合計: {passed}/{total} テスト成功")
    
    if passed == total:
        print("\n✓ すべてのテストが成功しました！")
        print("  XRPLブロックチェーンとの接続が確認されました。")
        print("  ダミーデータではなく、実際のブロックチェーンを使用しています。")
        return 0
    else:
        print("\n✗ 一部のテストが失敗しました")
        print("  XRPLブロックチェーンとの接続を確認してください。")
        return 1


if __name__ == '__main__':
    sys.exit(main())
