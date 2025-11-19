'use client';

import { useEffect, useRef } from 'react';
import QRCode from 'qrcode';
import Button from '@/components/ui/Button';

interface PickupQRCodeProps {
  orderId: string;
  orderItemId: string;
  productName: string;
}

export default function PickupQRCode({
  orderId,
  orderItemId,
  productName,
}: PickupQRCodeProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (canvasRef.current) {
      const qrData = JSON.stringify({
        order_id: orderId,
        item_id: orderItemId,
        type: 'pickup',
        timestamp: Date.now(),
      });

      QRCode.toCanvas(canvasRef.current, qrData, {
        width: 300,
        margin: 2,
        color: {
          dark: '#000000',
          light: '#FFFFFF',
        },
      });
    }
  }, [orderId, orderItemId]);

  const handleDownload = () => {
    if (canvasRef.current) {
      const url = canvasRef.current.toDataURL('image/png');
      const link = document.createElement('a');
      link.download = `pickup-qr-${orderItemId}.png`;
      link.href = url;
      link.click();
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="text-center">
        <h3 className="text-xl font-bold text-gray-900 mb-2">受け取りQRコード</h3>
        <p className="text-sm text-gray-600 mb-6">{productName}</p>

        <div className="bg-gray-50 p-6 rounded-lg inline-block mb-6">
          <canvas ref={canvasRef} className="mx-auto" />
        </div>

        <div className="space-y-4">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-start">
              <svg
                className="w-5 h-5 text-blue-600 mt-0.5 mr-3 flex-shrink-0"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                  clipRule="evenodd"
                />
              </svg>
              <div className="text-left">
                <h4 className="text-sm font-semibold text-blue-900">受け取り方法</h4>
                <ul className="text-xs text-blue-700 mt-2 space-y-1">
                  <li>• 会場の受付でこのQRコードを提示してください</li>
                  <li>• スタッフがスキャンして商品をお渡しします</li>
                  <li>• スクリーンショットを保存しておくと便利です</li>
                </ul>
              </div>
            </div>
          </div>

          <div className="flex gap-3">
            <Button onClick={handleDownload} variant="primary" className="flex-1">
              <svg
                className="w-5 h-5 mr-2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                />
              </svg>
              QRコードを保存
            </Button>
          </div>

          <div className="text-xs text-gray-500">
            注文ID: {orderId.slice(0, 8)}...
          </div>
        </div>
      </div>
    </div>
  );
}
