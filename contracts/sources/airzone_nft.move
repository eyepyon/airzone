/// Airzone NFT Module
/// 
/// This module implements the NFT system for the Airzone WiFi-triggered
/// NFT distribution platform. Users receive NFTs automatically when they
/// connect to WiFi and authenticate through the captive portal.
///
/// Requirements:
/// - 3.2: NFT minting via Move smart contract
/// - 3.3: Sponsored transactions (sponsor pays gas fees)

module airzone_nft::nft {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};
    use std::string::{Self, String};
    use sui::event;

    /// The AirzoneNFT object represents a unique NFT in the system
    /// Each NFT contains metadata about the token
    public struct AirzoneNFT has key, store {
        id: UID,
        /// Name of the NFT
        name: String,
        /// Description of the NFT
        description: String,
        /// URL to the NFT image
        image_url: String,
        /// Timestamp when the NFT was minted (block timestamp)
        minted_at: u64,
        /// Original minter address
        minter: address,
    }

    /// Event emitted when a new NFT is minted
    public struct NFTMinted has copy, drop {
        /// Object ID of the minted NFT
        nft_id: address,
        /// Name of the NFT
        name: String,
        /// Recipient address
        recipient: address,
        /// Minter address (sponsor)
        minter: address,
        /// Timestamp
        timestamp: u64,
    }

    /// Event emitted when an NFT is transferred
    public struct NFTTransferred has copy, drop {
        /// Object ID of the NFT
        nft_id: address,
        /// Previous owner
        from: address,
        /// New owner
        to: address,
        /// Timestamp
        timestamp: u64,
    }

    /// Event emitted when NFT metadata is updated
    public struct NFTMetadataUpdated has copy, drop {
        /// Object ID of the NFT
        nft_id: address,
        /// New name
        name: String,
        /// New description
        description: String,
        /// New image URL
        image_url: String,
        /// Timestamp
        timestamp: u64,
    }

    /// Event emitted when an NFT is burned
    public struct NFTBurned has copy, drop {
        /// Object ID of the burned NFT
        nft_id: address,
        /// Owner who burned the NFT
        owner: address,
        /// Timestamp
        timestamp: u64,
    }

    /// Error codes
    const ENotOwner: u64 = 1;
    const EInvalidMetadata: u64 = 2;

    /// Mint a new AirzoneNFT
    /// 
    /// This function creates a new NFT and transfers it to the recipient.
    /// The transaction can be sponsored, meaning the sponsor pays the gas fees
    /// while the recipient receives the NFT.
    ///
    /// # Arguments
    /// * `name` - Name of the NFT
    /// * `description` - Description of the NFT
    /// * `image_url` - URL to the NFT image
    /// * `recipient` - Address to receive the NFT
    /// * `ctx` - Transaction context
    ///
    /// Requirements: 3.2, 3.3
    public entry fun mint(
        name: vector<u8>,
        description: vector<u8>,
        image_url: vector<u8>,
        recipient: address,
        ctx: &mut TxContext
    ) {
        let nft = AirzoneNFT {
            id: object::new(ctx),
            name: string::utf8(name),
            description: string::utf8(description),
            image_url: string::utf8(image_url),
            minted_at: tx_context::epoch_timestamp_ms(ctx),
            minter: tx_context::sender(ctx),
        };

        let nft_id = object::uid_to_address(&nft.id);

        // Emit minting event
        event::emit(NFTMinted {
            nft_id,
            name: nft.name,
            recipient,
            minter: tx_context::sender(ctx),
            timestamp: tx_context::epoch_timestamp_ms(ctx),
        });

        // Transfer NFT to recipient
        transfer::public_transfer(nft, recipient);
    }

    /// Transfer an NFT to another address
    ///
    /// # Arguments
    /// * `nft` - The NFT to transfer
    /// * `recipient` - Address to receive the NFT
    /// * `ctx` - Transaction context
    public entry fun transfer_nft(
        nft: AirzoneNFT,
        recipient: address,
        ctx: &mut TxContext
    ) {
        let nft_id = object::uid_to_address(&nft.id);
        let sender = tx_context::sender(ctx);

        // Emit transfer event
        event::emit(NFTTransferred {
            nft_id,
            from: sender,
            to: recipient,
            timestamp: tx_context::epoch_timestamp_ms(ctx),
        });

        // Transfer to recipient
        transfer::public_transfer(nft, recipient);
    }

    /// Update NFT metadata (owner only)
    ///
    /// # Arguments
    /// * `nft` - Mutable reference to the NFT
    /// * `name` - New name
    /// * `description` - New description
    /// * `image_url` - New image URL
    /// * `ctx` - Transaction context
    public entry fun update_metadata(
        nft: &mut AirzoneNFT,
        name: vector<u8>,
        description: vector<u8>,
        image_url: vector<u8>,
        ctx: &mut TxContext
    ) {
        // Update metadata
        nft.name = string::utf8(name);
        nft.description = string::utf8(description);
        nft.image_url = string::utf8(image_url);

        // Emit update event
        event::emit(NFTMetadataUpdated {
            nft_id: object::uid_to_address(&nft.id),
            name: nft.name,
            description: nft.description,
            image_url: nft.image_url,
            timestamp: tx_context::epoch_timestamp_ms(ctx),
        });
    }

    /// Burn/destroy an NFT (owner only)
    ///
    /// # Arguments
    /// * `nft` - The NFT to burn
    /// * `ctx` - Transaction context
    public entry fun burn(
        nft: AirzoneNFT,
        ctx: &mut TxContext
    ) {
        let AirzoneNFT { id, name: _, description: _, image_url: _, minted_at: _, minter: _ } = nft;
        let nft_id = object::uid_to_address(&id);

        // Emit burn event
        event::emit(NFTBurned {
            nft_id,
            owner: tx_context::sender(ctx),
            timestamp: tx_context::epoch_timestamp_ms(ctx),
        });

        // Delete the NFT object
        object::delete(id);
    }

    // === Getter Functions ===

    /// Get the name of an NFT
    public fun name(nft: &AirzoneNFT): String {
        nft.name
    }

    /// Get the description of an NFT
    public fun description(nft: &AirzoneNFT): String {
        nft.description
    }

    /// Get the image URL of an NFT
    public fun image_url(nft: &AirzoneNFT): String {
        nft.image_url
    }

    /// Get the minted timestamp of an NFT
    public fun minted_at(nft: &AirzoneNFT): u64 {
        nft.minted_at
    }

    /// Get the minter address of an NFT
    public fun minter(nft: &AirzoneNFT): address {
        nft.minter
    }

    /// Get the object ID of an NFT
    public fun id(nft: &AirzoneNFT): address {
        object::uid_to_address(&nft.id)
    }

    // === Test Functions ===

    #[test_only]
    public fun test_mint(ctx: &mut TxContext): AirzoneNFT {
        AirzoneNFT {
            id: object::new(ctx),
            name: string::utf8(b"Test NFT"),
            description: string::utf8(b"Test Description"),
            image_url: string::utf8(b"https://example.com/image.png"),
            minted_at: 0,
            minter: tx_context::sender(ctx),
        }
    }
}
