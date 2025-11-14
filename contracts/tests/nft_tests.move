#[test_only]
module airzone_nft::nft_tests {
    use airzone_nft::nft::{Self, AirzoneNFT};
    use sui::test_scenario::{Self as ts, Scenario};
    use sui::test_utils;
    use std::string;

    // Test addresses
    const ADMIN: address = @0xAD;
    const USER1: address = @0xB0B;
    const USER2: address = @0xC0C;

    #[test]
    fun test_mint_nft() {
        let mut scenario = ts::begin(ADMIN);
        
        // Mint NFT to USER1
        {
            let ctx = ts::ctx(&mut scenario);
            nft::mint(
                b"Test NFT",
                b"A test NFT for Airzone",
                b"https://example.com/nft.png",
                USER1,
                ctx
            );
        };
        
        // Check USER1 received the NFT
        ts::next_tx(&mut scenario, USER1);
        {
            let nft = ts::take_from_sender<AirzoneNFT>(&scenario);
            
            // Verify NFT properties
            assert!(nft::name(&nft) == string::utf8(b"Test NFT"), 0);
            assert!(nft::description(&nft) == string::utf8(b"A test NFT for Airzone"), 1);
            assert!(nft::image_url(&nft) == string::utf8(b"https://example.com/nft.png"), 2);
            assert!(nft::minter(&nft) == ADMIN, 3);
            
            ts::return_to_sender(&scenario, nft);
        };
        
        ts::end(scenario);
    }

    #[test]
    fun test_transfer_nft() {
        let mut scenario = ts::begin(ADMIN);
        
        // Mint NFT to USER1
        {
            let ctx = ts::ctx(&mut scenario);
            nft::mint(
                b"Transfer Test NFT",
                b"Testing NFT transfer",
                b"https://example.com/transfer.png",
                USER1,
                ctx
            );
        };
        
        // USER1 transfers NFT to USER2
        ts::next_tx(&mut scenario, USER1);
        {
            let nft = ts::take_from_sender<AirzoneNFT>(&scenario);
            let ctx = ts::ctx(&mut scenario);
            
            nft::transfer_nft(nft, USER2, ctx);
        };
        
        // Check USER2 received the NFT
        ts::next_tx(&mut scenario, USER2);
        {
            let nft = ts::take_from_sender<AirzoneNFT>(&scenario);
            
            // Verify NFT is the same
            assert!(nft::name(&nft) == string::utf8(b"Transfer Test NFT"), 0);
            
            ts::return_to_sender(&scenario, nft);
        };
        
        ts::end(scenario);
    }

    #[test]
    fun test_update_metadata() {
        let mut scenario = ts::begin(ADMIN);
        
        // Mint NFT to USER1
        {
            let ctx = ts::ctx(&mut scenario);
            nft::mint(
                b"Original Name",
                b"Original Description",
                b"https://example.com/original.png",
                USER1,
                ctx
            );
        };
        
        // USER1 updates metadata
        ts::next_tx(&mut scenario, USER1);
        {
            let mut nft = ts::take_from_sender<AirzoneNFT>(&scenario);
            let ctx = ts::ctx(&mut scenario);
            
            nft::update_metadata(
                &mut nft,
                b"Updated Name",
                b"Updated Description",
                b"https://example.com/updated.png",
                ctx
            );
            
            // Verify metadata was updated
            assert!(nft::name(&nft) == string::utf8(b"Updated Name"), 0);
            assert!(nft::description(&nft) == string::utf8(b"Updated Description"), 1);
            assert!(nft::image_url(&nft) == string::utf8(b"https://example.com/updated.png"), 2);
            
            ts::return_to_sender(&scenario, nft);
        };
        
        ts::end(scenario);
    }

    #[test]
    fun test_burn_nft() {
        let mut scenario = ts::begin(ADMIN);
        
        // Mint NFT to USER1
        {
            let ctx = ts::ctx(&mut scenario);
            nft::mint(
                b"Burn Test NFT",
                b"This NFT will be burned",
                b"https://example.com/burn.png",
                USER1,
                ctx
            );
        };
        
        // USER1 burns the NFT
        ts::next_tx(&mut scenario, USER1);
        {
            let nft = ts::take_from_sender<AirzoneNFT>(&scenario);
            let ctx = ts::ctx(&mut scenario);
            
            nft::burn(nft, ctx);
        };
        
        // Verify NFT no longer exists
        ts::next_tx(&mut scenario, USER1);
        {
            assert!(!ts::has_most_recent_for_sender<AirzoneNFT>(&scenario), 0);
        };
        
        ts::end(scenario);
    }

    #[test]
    fun test_multiple_nfts() {
        let mut scenario = ts::begin(ADMIN);
        
        // Mint multiple NFTs to USER1
        {
            let ctx = ts::ctx(&mut scenario);
            
            nft::mint(
                b"NFT 1",
                b"First NFT",
                b"https://example.com/1.png",
                USER1,
                ctx
            );
        };
        
        ts::next_tx(&mut scenario, ADMIN);
        {
            let ctx = ts::ctx(&mut scenario);
            
            nft::mint(
                b"NFT 2",
                b"Second NFT",
                b"https://example.com/2.png",
                USER1,
                ctx
            );
        };
        
        ts::next_tx(&mut scenario, ADMIN);
        {
            let ctx = ts::ctx(&mut scenario);
            
            nft::mint(
                b"NFT 3",
                b"Third NFT",
                b"https://example.com/3.png",
                USER1,
                ctx
            );
        };
        
        // USER1 should have 3 NFTs
        // Note: In a real scenario, you'd query the blockchain for owned objects
        // This test just verifies the minting doesn't fail
        
        ts::end(scenario);
    }

    #[test]
    fun test_sponsored_mint() {
        let mut scenario = ts::begin(ADMIN);
        
        // ADMIN (sponsor) mints NFT for USER1
        // The sponsor pays gas, but NFT goes to USER1
        {
            let ctx = ts::ctx(&mut scenario);
            nft::mint(
                b"Sponsored NFT",
                b"This NFT was minted with sponsored transaction",
                b"https://example.com/sponsored.png",
                USER1,
                ctx
            );
        };
        
        // Verify USER1 received the NFT (not ADMIN)
        ts::next_tx(&mut scenario, USER1);
        {
            let nft = ts::take_from_sender<AirzoneNFT>(&scenario);
            
            // Verify minter is ADMIN (sponsor)
            assert!(nft::minter(&nft) == ADMIN, 0);
            
            ts::return_to_sender(&scenario, nft);
        };
        
        // Verify ADMIN doesn't have the NFT
        ts::next_tx(&mut scenario, ADMIN);
        {
            assert!(!ts::has_most_recent_for_sender<AirzoneNFT>(&scenario), 0);
        };
        
        ts::end(scenario);
    }
}
