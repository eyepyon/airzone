# Captive Portal Implementation

## Overview

The captive portal provides a WiFi authentication flow that automatically creates user accounts, generates Sui wallets, and mints NFTs upon successful login.

## Components

### 1. CaptivePortalPage (`/app/captive/page.tsx`)

The main captive portal page that users see when connecting to WiFi.

**Features:**
- Terms and conditions display with checkbox agreement
- Google OAuth login integration
- Automatic WiFi session creation upon authentication
- Error handling and loading states
- Responsive design for mobile and desktop

**Flow:**
1. User connects to WiFi and is redirected to captive portal
2. User reads and agrees to terms of service
3. User logs in with Google account
4. System automatically creates WiFi session
5. User is shown the WelcomeScreen

### 2. WelcomeScreen (`/components/captive/WelcomeScreen.tsx`)

Post-authentication welcome screen that handles NFT minting and displays user information.

**Features:**
- Displays user information and wallet address
- Automatically requests NFT minting if user has no NFTs
- Real-time NFT minting status with polling
- Visual feedback for minting states (requesting, minting, completed, failed)
- Navigation to shop and dashboard
- Informational content about service usage

**NFT Minting Flow:**
1. Check if user has existing NFTs
2. If no NFTs, automatically request minting
3. Poll backend every 3 seconds for minting status
4. Display appropriate status (requesting → minting → completed/failed)
5. Show success message when NFT is minted
6. Enable navigation buttons

**Minting States:**
- `idle`: Initial state
- `requesting`: Sending mint request to backend
- `minting`: NFT is being created on blockchain
- `completed`: NFT successfully minted
- `failed`: Minting failed with error message

## API Integration

### WiFi Session API
- `POST /api/v1/wifi/connect` - Creates WiFi session record

### NFT API
- `GET /api/v1/nfts` - Fetches user's NFTs
- `POST /api/v1/nfts/mint` - Requests NFT minting
- `GET /api/v1/nfts/status/{task_id}` - Checks minting task status

## State Management

Uses Zustand stores:
- `useAuthStore` - User authentication and wallet information
- `useNFTStore` - NFT data and minting operations

## Requirements Satisfied

### Requirement 2.1: WiFi Connection and Captive Portal
✅ OpenNDS redirects users to captive portal page
✅ Authentication flow integrated

### Requirement 2.5: User Experience
✅ Clear welcome screen with status information
✅ Terms of service agreement UI
✅ Responsive design for all devices

### Requirement 3.1: NFT Auto-Distribution
✅ Automatic NFT minting after WiFi authentication
✅ Real-time status updates with polling
✅ Error handling and retry mechanism
✅ Visual feedback for all minting states

## User Experience Flow

```
WiFi Connection
    ↓
Captive Portal Page
    ↓
Terms Agreement
    ↓
Google Login
    ↓
WiFi Session Created
    ↓
Welcome Screen
    ↓
Auto NFT Mint Request
    ↓
Poll Mint Status (every 3s)
    ↓
NFT Minted Successfully
    ↓
Navigate to Shop/Dashboard
```

## Styling

- Uses Tailwind CSS for responsive design
- Gradient background (blue-50 to indigo-100)
- Card-based layout for clean presentation
- Loading indicators for async operations
- Color-coded status messages (green for success, red for error, blue for info)

## Error Handling

- Network errors during login
- WiFi session creation failures
- NFT minting failures with retry option
- Graceful degradation with user-friendly messages

## Future Enhancements

- Add session timeout handling
- Implement offline detection
- Add analytics tracking
- Support for multiple NFT types
- Customizable terms and conditions
- Multi-language support
