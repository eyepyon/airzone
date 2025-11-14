'use client';

import { useState, useMemo } from 'react';
import { NFT } from '../../types';
import NFTCard from './NFTCard';
import Loading from '../ui/Loading';

interface NFTGalleryProps {
  nfts: NFT[];
  loading?: boolean;
  onNFTClick?: (nft: NFT) => void;
  emptyMessage?: string;
}

export default function NFTGallery({
  nfts,
  loading = false,
  onNFTClick,
  emptyMessage = 'No NFTs found',
}: NFTGalleryProps) {
  const [filterStatus, setFilterStatus] = useState<NFT['status'] | 'all'>('all');
  const [sortBy, setSortBy] = useState<'newest' | 'oldest'>('newest');

  // Filter and sort NFTs
  const filteredAndSortedNFTs = useMemo(() => {
    let filtered = nfts;

    // Apply status filter
    if (filterStatus !== 'all') {
      filtered = filtered.filter((nft) => nft.status === filterStatus);
    }

    // Apply sorting
    const sorted = [...filtered].sort((a, b) => {
      const dateA = new Date(a.created_at).getTime();
      const dateB = new Date(b.created_at).getTime();
      return sortBy === 'newest' ? dateB - dateA : dateA - dateB;
    });

    return sorted;
  }, [nfts, filterStatus, sortBy]);

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <Loading size="lg" text="Loading NFTs..." />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Filters and Controls */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div className="flex items-center gap-2">
          <label htmlFor="status-filter" className="text-sm font-medium text-gray-700">
            Filter:
          </label>
          <select
            id="status-filter"
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value as NFT['status'] | 'all')}
            className="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Status</option>
            <option value="completed">Completed</option>
            <option value="minting">Minting</option>
            <option value="pending">Pending</option>
            <option value="failed">Failed</option>
          </select>
        </div>

        <div className="flex items-center gap-2">
          <label htmlFor="sort-by" className="text-sm font-medium text-gray-700">
            Sort:
          </label>
          <select
            id="sort-by"
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as 'newest' | 'oldest')}
            className="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="newest">Newest First</option>
            <option value="oldest">Oldest First</option>
          </select>
        </div>
      </div>

      {/* NFT Count */}
      <div className="text-sm text-gray-600">
        Showing {filteredAndSortedNFTs.length} of {nfts.length} NFTs
      </div>

      {/* NFT Grid */}
      {filteredAndSortedNFTs.length === 0 ? (
        <div className="text-center py-12">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-100 mb-4">
            <svg
              className="w-8 h-8 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
              />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            {emptyMessage}
          </h3>
          <p className="text-sm text-gray-500">
            {filterStatus !== 'all'
              ? 'Try changing the filter to see more NFTs'
              : 'Connect to WiFi to receive your first NFT'}
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredAndSortedNFTs.map((nft) => (
            <NFTCard key={nft.id} nft={nft} onClick={onNFTClick} />
          ))}
        </div>
      )}
    </div>
  );
}
