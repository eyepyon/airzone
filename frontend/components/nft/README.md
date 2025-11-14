# NFT Components

This directory contains components for displaying and managing NFTs in the Airzone application.

## Components

### NFTCard

A card component that displays a single NFT with its image, metadata, and status.

**Props:**
- `nft: NFT` - The NFT object to display
- `onClick?: (nft: NFT) => void` - Optional callback when the card is clicked

**Features:**
- Displays NFT image with fallback for loading/error states
- Shows status badge (pending, minting, completed, failed)
- Displays NFT name, description, and object ID
- Links to Sui Explorer for completed NFTs
- Shows error messages for failed mints

### NFTGallery

A gallery component that displays a collection of NFTs in a responsive grid layout.

**Props:**
- `nfts: NFT[]` - Array of NFTs to display
- `loading?: boolean` - Loading state
- `onNFTClick?: (nft: NFT) => void` - Callback when an NFT is clicked
- `emptyMessage?: string` - Custom message when no NFTs are found

**Features:**
- Responsive grid layout (1-4 columns based on screen size)
- Filter by status (all, completed, minting, pending, failed)
- Sort by date (newest/oldest first)
- Shows NFT count
- Empty state with helpful message
- Loading state

## Pages

### /nfts

NFT list page that displays all NFTs owned by the current user.

**Features:**
- Displays user's wallet address
- "Mint New NFT" button
- Uses NFTGallery component
- Requires authentication
- Auto-fetches NFTs on mount

### /nfts/[id]

NFT detail page that shows comprehensive information about a single NFT.

**Features:**
- Large image display
- Complete metadata display
- Status information
- Transaction details with link to Sui Explorer
- Error details for failed mints
- Back navigation to NFT list
- Requires authentication

## Usage Example

```tsx
import NFTCard from '@/components/nft/NFTCard';
import NFTGallery from '@/components/nft/NFTGallery';
import { useNFTStore } from '@/stores/nft-store';

function MyNFTs() {
  const { nfts, loading } = useNFTStore();
  
  return (
    <NFTGallery
      nfts={nfts}
      loading={loading}
      onNFTClick={(nft) => router.push(`/nfts/${nft.id}`)}
    />
  );
}
```

## Status Display

NFTs can have the following statuses:
- **pending**: NFT mint request has been queued
- **minting**: NFT is currently being minted on the blockchain
- **completed**: NFT has been successfully minted
- **failed**: NFT minting failed (error message displayed)

## Integration

These components integrate with:
- `useNFTStore` - Zustand store for NFT state management
- `useAuthStore` - Zustand store for authentication
- NFT API functions from `lib/api/nfts.ts`
- Card and Loading UI components

## Requirements Satisfied

- **Requirement 1.3**: Wallet management and NFT display
- **Requirement 3.4**: NFT listing and status display
