# Airzone Components

このディレクトリには、Airzone アプリケーションで使用される React コンポーネントが含まれています。

## ディレクトリ構造

```
components/
├── layout/          # レイアウトコンポーネント
├── ui/              # 再利用可能な UI コンポーネント
├── auth/            # 認証関連コンポーネント
├── captive/         # キャプティブポータルコンポーネント
├── nft/             # NFT 関連コンポーネント
└── shop/            # EC ショップコンポーネント
```

## Layout Components

### Header
ナビゲーションバー、ユーザーメニュー、カートアイコンを含むヘッダーコンポーネント。

```tsx
import { Header } from '@/components/layout';

<Header />
```

### Footer
サイトフッター（リンク、著作権情報など）。

```tsx
import { Footer } from '@/components/layout';

<Footer />
```

### Layout
ヘッダーとフッターを含む基本レイアウトラッパー。

```tsx
import { Layout } from '@/components/layout';

<Layout>
  <YourPageContent />
</Layout>
```

## UI Components

### Button
カスタマイズ可能なボタンコンポーネント。

```tsx
import { Button } from '@/components/ui';

<Button variant="primary" size="md" onClick={handleClick}>
  クリック
</Button>

<Button variant="outline" isLoading>
  処理中
</Button>
```

**Props:**
- `variant`: 'primary' | 'secondary' | 'danger' | 'outline'
- `size`: 'sm' | 'md' | 'lg'
- `isLoading`: boolean
- `fullWidth`: boolean

### Card
コンテンツカードコンポーネント。

```tsx
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui';

<Card padding="md" hover>
  <CardHeader>
    <CardTitle>タイトル</CardTitle>
  </CardHeader>
  <CardContent>
    <p>コンテンツ</p>
  </CardContent>
  <CardFooter>
    <Button>アクション</Button>
  </CardFooter>
</Card>
```

**Props:**
- `padding`: 'none' | 'sm' | 'md' | 'lg'
- `hover`: boolean

### Loading
ローディングインジケーター。

```tsx
import { Loading, LoadingSpinner, LoadingDots } from '@/components/ui';

// フルスクリーンローディング
<Loading fullScreen text="読み込み中..." />

// インラインローディング
<Loading size="md" />

// スピナーのみ
<LoadingSpinner />

// ドットアニメーション
<LoadingDots />
```

**Props:**
- `size`: 'sm' | 'md' | 'lg'
- `text`: string
- `fullScreen`: boolean

### Toast
通知トーストコンポーネント。

```tsx
import { useToast, ToastContainer } from '@/components/ui';

function MyComponent() {
  const toast = useToast();

  const handleSuccess = () => {
    toast.success('成功しました！');
  };

  const handleError = () => {
    toast.error('エラーが発生しました');
  };

  return (
    <>
      <Button onClick={handleSuccess}>成功</Button>
      <Button onClick={handleError}>エラー</Button>
      <ToastContainer toasts={toast.toasts} onRemove={toast.removeToast} />
    </>
  );
}
```

**Toast Types:**
- `success`: 成功メッセージ
- `error`: エラーメッセージ
- `warning`: 警告メッセージ
- `info`: 情報メッセージ

## スタイリング

すべてのコンポーネントは Tailwind CSS を使用してスタイリングされています。カスタムスタイルを追加する場合は、`className` prop を使用してください。

```tsx
<Button className="mt-4">カスタムマージン</Button>
```

## レスポンシブデザイン

コンポーネントはモバイル、タブレット、デスクトップに対応したレスポンシブデザインになっています。

- モバイル: デフォルト
- タブレット: `md:` プレフィックス
- デスクトップ: `lg:` プレフィックス
