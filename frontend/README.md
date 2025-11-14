# Airzone Frontend

Next.js 14 frontend application for the Airzone WiFi-triggered NFT distribution and EC shop platform.

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Blockchain**: @mysten/dapp-kit (Sui)
- **Payments**: @stripe/react-stripe-js
- **Code Quality**: ESLint, Prettier

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
├── components/             # React components
│   ├── auth/              # Authentication components
│   ├── captive/           # Captive portal components
│   ├── layout/            # Layout components (Header, Footer)
│   ├── nft/               # NFT display components
│   ├── shop/              # E-commerce components
│   └── ui/                # Reusable UI components
├── lib/                   # Utility functions and API clients
│   ├── api/               # API service functions
│   └── api-client.ts      # Base API client
├── stores/                # Zustand state stores
│   ├── auth-store.ts      # Authentication state
│   ├── cart-store.ts      # Shopping cart state
│   └── nft-store.ts       # NFT state
├── types/                 # TypeScript type definitions
└── public/                # Static assets

```

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Install dependencies:

```bash
npm install
```

2. Copy environment variables:

```bash
cp .env.local.example .env.local
```

3. Update `.env.local` with your configuration values

### Development

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build

Build for production:

```bash
npm run build
```

### Linting and Formatting

```bash
# Run ESLint
npm run lint

# Format code with Prettier
npm run format

# Check formatting
npm run format:check
```

## Environment Variables

See `.env.local.example` for required environment variables:

- `NEXT_PUBLIC_API_URL`: Backend API URL
- `NEXT_PUBLIC_SUI_NETWORK`: Sui blockchain network (testnet/mainnet)
- `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`: Stripe publishable key
- `NEXT_PUBLIC_GOOGLE_CLIENT_ID`: Google OAuth client ID

## Features

- Google OAuth authentication
- Automatic Sui wallet creation
- NFT display and management
- NFT-gated e-commerce shop
- Stripe payment integration
- Responsive design
- Server-side rendering (SSR)

## License

Proprietary
