# AI開発ツールのセットアップガイド

## 目次
1. [GitHub Copilot](#github-copilot)
2. [その他のAI拡張機能](#その他のai拡張機能)
3. [Kiroとの併用](#kiroとの併用)
4. [使い分けのコツ](#使い分けのコツ)

---

## GitHub Copilot

### 1. インストール方法

#### ステップ1: GitHub Copilotのサブスクリプション
1. [GitHub Copilot](https://github.com/features/copilot)にアクセス
2. "Start my free trial" または "Buy GitHub Copilot" をクリック
3. 料金プラン:
   - **個人**: $10/月 または $100/年
   - **ビジネス**: $19/ユーザー/月
   - **学生・教育者**: 無料（GitHub Student Developer Packで）

#### ステップ2: VS Code（Kiro IDE）に拡張機能をインストール
1. Kiro IDEを開く
2. 拡張機能パネルを開く（`Ctrl+Shift+X` または `Cmd+Shift+X`）
3. "GitHub Copilot" を検索
4. "Install" をクリック
5. "GitHub Copilot Chat" も一緒にインストール（推奨）

#### ステップ3: GitHubアカウントでサインイン
1. インストール後、右下に通知が表示される
2. "Sign in to GitHub" をクリック
3. ブラウザでGitHubにログイン
4. 認証を許可

### 2. 基本的な使い方

#### コード補完
```typescript
// 関数名を書き始めると、Copilotが自動的に提案
function calculateTotal

// Tabキーで提案を受け入れる
// Escキーで提案を拒否
```

#### コメントからコード生成
```typescript
// ユーザーの年齢を計算する関数
// 誕生日から現在の年齢を計算し、整数で返す

// ↑ このコメントを書くと、Copilotが関数を提案
```

#### 複数の提案を見る
- `Alt+]` または `Option+]`: 次の提案
- `Alt+[` または `Option+[`: 前の提案
- `Ctrl+Enter`: 提案パネルを開く（複数の提案を一覧表示）

### 3. GitHub Copilot Chat の使い方

#### チャットパネルを開く
- `Ctrl+Shift+I` または `Cmd+Shift+I`
- サイドバーのチャットアイコンをクリック

#### 便利なコマンド

```
# コードの説明を求める
/explain このコードは何をしていますか？

# コードの修正を依頼
/fix このバグを修正してください

# テストコードを生成
/tests この関数のテストを書いてください

# コードの最適化
/optimize このコードをパフォーマンス改善してください

# ドキュメントを生成
/doc この関数のJSDocを書いてください
```

#### インラインチャット
1. コードを選択
2. `Ctrl+I` または `Cmd+I` を押す
3. 質問や指示を入力
4. Copilotが選択範囲を編集

### 4. 設定のカスタマイズ

#### settings.json に追加
```json
{
  // Copilotを有効化
  "github.copilot.enable": {
    "*": true,
    "yaml": true,
    "plaintext": false,
    "markdown": true
  },
  
  // インライン提案を有効化
  "github.copilot.inlineSuggest.enable": true,
  
  // 提案のトリガー
  "editor.inlineSuggest.enabled": true,
  
  // Copilot Chat の設定
  "github.copilot.chat.localeOverride": "ja",
  
  // 特定のファイルで無効化
  "github.copilot.advanced": {
    "excludedLanguages": []
  }
}
```

### 5. ショートカットキー

| 機能 | Windows/Linux | Mac |
|------|---------------|-----|
| 提案を受け入れる | `Tab` | `Tab` |
| 提案を拒否 | `Esc` | `Esc` |
| 次の提案 | `Alt+]` | `Option+]` |
| 前の提案 | `Alt+[` | `Option+[` |
| 提案パネルを開く | `Ctrl+Enter` | `Cmd+Enter` |
| インラインチャット | `Ctrl+I` | `Cmd+I` |
| チャットパネル | `Ctrl+Shift+I` | `Cmd+Shift+I` |

---

## その他のAI拡張機能

### 1. Tabnine
- **特徴**: オフラインでも動作、プライバシー重視
- **料金**: 無料プランあり、Pro版 $12/月
- **インストール**: 拡張機能で "Tabnine" を検索

### 2. Codeium
- **特徴**: 完全無料、多言語対応
- **料金**: 無料
- **インストール**: 拡張機能で "Codeium" を検索

### 3. Amazon CodeWhisperer
- **特徴**: AWS統合、セキュリティスキャン
- **料金**: 個人利用は無料
- **インストール**: 拡張機能で "AWS Toolkit" を検索

### 4. Cursor（別のエディタ）
- **特徴**: AI統合エディタ、GPT-4対応
- **料金**: 無料プランあり、Pro版 $20/月
- **URL**: https://cursor.sh/

---

## Kiroとの併用

### Kiro と GitHub Copilot の違い

| 機能 | Kiro | GitHub Copilot |
|------|------|----------------|
| **コード補完** | ❌ | ✅ 優秀 |
| **コード生成** | ✅ 優秀 | ✅ 優秀 |
| **ファイル操作** | ✅ 自動実行 | ❌ 手動 |
| **プロジェクト理解** | ✅ 全体把握 | ⚠️ 限定的 |
| **複数ファイル編集** | ✅ 一度に可能 | ❌ 1ファイルずつ |
| **デバッグ支援** | ✅ | ⚠️ 限定的 |
| **チャット形式** | ✅ | ✅ |

### 推奨される使い分け

#### Kiroを使う場面
```
✅ 新機能の実装（複数ファイルにまたがる）
✅ バグ修正（関連ファイルを自動で特定）
✅ リファクタリング（プロジェクト全体の変更）
✅ ファイル作成・削除
✅ プロジェクト構造の理解
✅ ドキュメント生成
```

#### GitHub Copilotを使う場面
```
✅ リアルタイムのコード補完
✅ 関数の実装（単一ファイル内）
✅ コメントからコード生成
✅ 定型的なコードの記述
✅ テストコードの生成
✅ 小規模な修正
```

### 併用の実例

#### 例1: 新機能の実装

```
1. Kiroに依頼:
   「商品購入時にNFTを自動ミントする機能を実装してください」
   → Kiro が複数ファイルを作成・編集

2. 細かい調整は Copilot:
   → 関数内のロジックを Copilot で補完
   → エラーハンドリングを Copilot で追加
```

#### 例2: バグ修正

```
1. Kiroに依頼:
   「購入制限のチェックが正しく動作しません。修正してください」
   → Kiro が問題を特定し、関連ファイルを修正

2. テストコードは Copilot:
   → Copilot でテストケースを生成
```

#### 例3: 日常的なコーディング

```
1. ファイル構造は Kiro:
   「新しいコンポーネントを作成してください」
   → Kiro がファイルを作成

2. 実装は Copilot:
   → Copilot のリアルタイム補完で実装
   → コメントを書いて Copilot に提案させる
```

---

## 使い分けのコツ

### 1. タスクの規模で判断

```
小規模（1ファイル、数行）
→ GitHub Copilot
  例: 関数の実装、バリデーションの追加

中規模（複数ファイル、関連する変更）
→ Kiro
  例: 新機能の追加、リファクタリング

大規模（プロジェクト全体）
→ Kiro
  例: アーキテクチャの変更、大規模なリファクタリング
```

### 2. 作業フローで判断

```
設計・計画フェーズ
→ Kiro
  「このような機能を実装したいのですが、
   どのようなファイル構成が良いですか？」

実装フェーズ
→ Copilot（リアルタイム補完）
→ Kiro（複雑な実装）

レビュー・修正フェーズ
→ Kiro
  「このコードをレビューして、
   改善点を教えてください」
```

### 3. 具体的な使用例

#### 朝の作業開始時
```typescript
// 1. Kiroに今日のタスクを相談
「今日は商品購入機能を実装します。
 どこから始めるべきですか？」

// 2. Kiroが提案したファイルを開く

// 3. Copilotでコーディング
function purchaseProduct(productId: string) {
  // Copilotが自動補完
}
```

#### 新機能の実装
```typescript
// 1. Kiroに全体像を依頼
「配送先住所入力フォームを作成してください」
→ コンポーネントファイル、型定義、バリデーションを作成

// 2. 細部はCopilotで調整
// 都道府県リストを追加
const PREFECTURES = [
  // Copilotが自動補完
];
```

#### バグ修正
```typescript
// 1. Kiroに問題を報告
「購入ボタンをクリックしてもカートに追加されません」
→ Kiroが原因を特定し、修正案を提示

// 2. Copilotでテストを追加
describe('購入機能', () => {
  // Copilotがテストケースを提案
});
```

---

## 設定ファイルの例

### .vscode/settings.json
```json
{
  // Kiro の設定
  "kiro.enabled": true,
  
  // GitHub Copilot の設定
  "github.copilot.enable": {
    "*": true
  },
  "github.copilot.inlineSuggest.enable": true,
  "editor.inlineSuggest.enabled": true,
  
  // 両方を効果的に使うための設定
  "editor.quickSuggestions": {
    "other": true,
    "comments": true,
    "strings": true
  },
  
  // Copilot の提案を表示するタイミング
  "editor.quickSuggestionsDelay": 10,
  
  // インライン提案の表示
  "editor.suggest.preview": true,
  
  // Copilot Chat の言語設定
  "github.copilot.chat.localeOverride": "ja"
}
```

---

## トラブルシューティング

### Copilotが動作しない

#### 1. サインイン状態を確認
```
1. 右下のステータスバーで Copilot アイコンを確認
2. クリックして "Sign in to GitHub" を選択
3. ブラウザで認証
```

#### 2. サブスクリプションを確認
```
1. https://github.com/settings/copilot にアクセス
2. サブスクリプションが有効か確認
```

#### 3. 拡張機能を再インストール
```
1. 拡張機能パネルで "GitHub Copilot" を検索
2. "Uninstall" をクリック
3. VS Code を再起動
4. 再度インストール
```

### Copilotの提案が表示されない

#### 設定を確認
```json
{
  "github.copilot.enable": {
    "*": true
  },
  "editor.inlineSuggest.enabled": true
}
```

#### ファイルタイプを確認
```
一部のファイルタイプでは Copilot が無効になっている可能性
→ settings.json で有効化
```

---

## まとめ

### 最適な組み合わせ

```
日常的なコーディング:
├─ リアルタイム補完: GitHub Copilot
├─ 複雑な実装: Kiro
└─ プロジェクト管理: Kiro

新機能開発:
├─ 設計・計画: Kiro
├─ ファイル作成: Kiro
├─ コード実装: Copilot + Kiro
└─ テスト作成: Copilot

バグ修正:
├─ 問題特定: Kiro
├─ 修正実装: Copilot
└─ テスト追加: Copilot
```

### 推奨ワークフロー

1. **朝**: Kiroに今日のタスクを相談
2. **実装**: Copilotでリアルタイム補完
3. **複雑な処理**: Kiroに依頼
4. **レビュー**: Kiroにコードレビューを依頼
5. **ドキュメント**: Kiroにドキュメント生成を依頼

両方を使いこなすことで、開発効率が大幅に向上します！🚀
