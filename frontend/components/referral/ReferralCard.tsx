'use client';

import { useState, useEffect } from 'react';

interface ReferralData {
  referral_code: string;
  referral_link: string;
  share_links: {
    twitter: string;
    facebook: string;
    line: string;
  };
}

export default function ReferralCard() {
  const [referralData, setReferralData] = useState<ReferralData | null>(null);
  const [copied, setCopied] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchReferralCode();
  }, []);

  const fetchReferralCode = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
      const response = await fetch(`${apiUrl}/api/v1/referral/code`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
      });
      
      if (response.ok) {
        const data = await response.json();
        setReferralData(data.data);
      }
    } catch (error) {
      console.error('Failed to fetch referral code:', error);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = () => {
    if (referralData) {
      navigator.clipboard.writeText(referralData.referral_link);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="h-10 bg-gray-200 rounded mb-4"></div>
        </div>
      </div>
    );
  }

  if (!referralData) return null;

  return (
    <div className="bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg shadow-lg p-6 text-white">
      <h3 className="text-xl font-bold mb-2">友達を招待</h3>
      <p className="text-purple-100 mb-4">
        友達を招待してコインをゲット！招待された友達は限定商品が購入できます。
      </p>

      <div className="bg-white/20 rounded-lg p-4 mb-4">
        <label className="text-sm text-purple-100 mb-2 block">あなたの紹介コード</label>
        <div className="flex items-center gap-2">
          <input
            type="text"
            value={referralData.referral_code}
            readOnly
            className="flex-1 px-4 py-2 bg-white/30 rounded-lg text-white font-mono text-lg"
          />
          <button
            onClick={copyToClipboard}
            className="px-4 py-2 bg-white text-purple-600 rounded-lg hover:bg-purple-50 transition"
          >
            {copied ? '✓ コピー済み' : 'コピー'}
          </button>
        </div>
      </div>

      <div className="bg-white/20 rounded-lg p-4 mb-4">
        <label className="text-sm text-purple-100 mb-2 block">紹介リンク</label>
        <input
          type="text"
          value={referralData.referral_link}
          readOnly
          className="w-full px-4 py-2 bg-white/30 rounded-lg text-white text-sm"
        />
      </div>

      <div className="space-y-2">
        <p className="text-sm text-purple-100">SNSでシェア:</p>
        <div className="flex gap-2">
          <a
            href={referralData.share_links.twitter}
            target="_blank"
            rel="noopener noreferrer"
            className="flex-1 px-4 py-2 bg-blue-400 hover:bg-blue-500 rounded-lg text-center transition"
          >
            𝕏 Twitter
          </a>
          <a
            href={referralData.share_links.line}
            target="_blank"
            rel="noopener noreferrer"
            className="flex-1 px-4 py-2 bg-green-500 hover:bg-green-600 rounded-lg text-center transition"
          >
            LINE
          </a>
          <a
            href={referralData.share_links.facebook}
            target="_blank"
            rel="noopener noreferrer"
            className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-center transition"
          >
            Facebook
          </a>
        </div>
      </div>
    </div>
  );
}
