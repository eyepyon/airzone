# Captive Portal Components

This directory contains components for the WiFi captive portal experience.

## Components

### WelcomeScreen

A component that displays the welcome screen after successful WiFi authentication and shows NFT minting status.

**Props:**
- `userName` (string): The authenticated user's name
- `walletAddress` (string): The user's Sui wallet address
- `mintingTaskId` (string | null): The task ID for NFT minting
- `onContinue` (function): Callback when user clicks continue button

**Features:**
- Real-time NFT minting status updates
- Visual progress indicators for WiFi connection, wallet creation, and NFT minting
- Display of wallet address
- NFT holder benefits information
- Error handling for failed minting

## Pages

### /captive

The main captive portal page that handles:
- WiFi connection authentication flow
- Google OAuth login integration
- Terms of service acceptance
- WiFi session creation
- Automatic NFT minting trigger
- Redirect to welcome screen after successful connection

**Query Parameters:**
- `mac` (optional): MAC address from OpenNDS
- `ip` (optional): IP address from OpenNDS

## Usage

The captive portal is automatically displayed when users connect to the WiFi network through OpenNDS. The flow is:

1. User connects to WiFi
2. OpenNDS redirects to `/captive?mac=XX:XX:XX:XX:XX:XX&ip=192.168.1.100`
3. User sees login screen with benefits and terms
4. User accepts terms and logs in with Google
5. WiFi session is created in the backend
6. NFT minting is automatically triggered
7. User sees welcome screen with minting status
8. User can continue to shop or dashboard

## Integration with Backend

The captive portal integrates with the following backend APIs:

- `POST /api/v1/auth/google` - Google OAuth authentication
- `POST /api/v1/wifi/connect` - Create WiFi session
- `POST /api/v1/nfts/mint` - Request NFT minting
- `GET /api/v1/nfts/status/{task_id}` - Check minting status

## State Management

Uses Zustand stores:
- `useAuthStore` - Authentication state and user info
- `useNFTStore` - NFT minting status and NFT list

## Styling

Components use Tailwind CSS with a gradient background (blue to indigo) and consistent card-based UI matching the rest of the application.
