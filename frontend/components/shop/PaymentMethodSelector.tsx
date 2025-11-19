'use client';

import { useState } from 'react';
import Card from '@/components/ui/Card';

export type PaymentMethod = 'stripe' | 'xrpl';

interface PaymentMethodSelectorProps {
  onSelect: (method: PaymentMethod) => void;
  selectedMethod?: PaymentMethod;
}

export default function PaymentMethodSelector({
  onSelect,
  selectedMethod,
}: PaymentMethodSelectorProps) {
  const [selected, setSelected] = useState<PaymentMethod>(
    selectedMethod || 'stripe'
  );

  const handleSelect = (method: PaymentMethod) => {
    setSelected(method);
    onSelect(method);
  };

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold text-gray-900">支払い方法を選択</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Stripe Payment */}
        <button
          onClick={() => handleSelect('stripe')}
          className={`text-left transition-all ${
            selected === 'stripe'
              ? 'ring-2 ring-blue-500'
              : 'hover:border-blue-300'
          }`}
        >
          <Card className="p-6 h-full">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center">
                <div
                  className={`w-6 h-6 rounded-full border-2 flex items-center justify-center mr-3 ${
                    selected === 'stripe'
                      ? 'border-blue-500 bg-blue-500'
                      : 'border-gray-300'
                  }`}
                >
                  {selected === 'stripe' && (
                    <svg
                      className="w-4 h-4 text-white"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fillRule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clipRule="evenodd"
                      />
                    </svg>
                  )}
                </div>
                <h3 className="text-lg font-semibold text-gray-900">
                  クレジットカード
                </h3>
              </div>
              <svg
                className="w-12 h-8"
                viewBox="0 0 60 25"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  fill="#635BFF"
                  d="M59.64 14.28h-8.06c.19 1.93 1.6 2.55 3.2 2.55 1.64 0 2.96-.37 4.05-.95v3.32a8.33 8.33 0 01-4.56 1.1c-4.01 0-6.83-2.5-6.83-7.48 0-4.19 2.39-7.52 6.3-7.52 3.92 0 5.96 3.28 5.96 7.5 0 .4-.04 1.26-.06 1.48zm-5.92-5.62c-1.03 0-2.17.73-2.17 2.58h4.25c0-1.85-1.07-2.58-2.08-2.58zM40.95 20.3c-1.44 0-2.32-.6-2.9-1.04l-.02 4.63-4.12.87V5.57h3.76l.08 1.02a4.7 4.7 0 013.23-1.29c2.9 0 5.62 2.6 5.62 7.4 0 5.23-2.7 7.6-5.65 7.6zM40 8.95c-.95 0-1.54.34-1.97.81l.02 6.12c.4.44.98.78 1.95.78 1.52 0 2.54-1.65 2.54-3.87 0-2.15-1.04-3.84-2.54-3.84zM28.24 5.57h4.13v14.44h-4.13V5.57zm0-4.7L32.37 0v3.36l-4.13.88V.88zm-4.32 9.35v9.79H19.8V5.57h3.7l.12 1.22c1-1.77 3.07-1.41 3.62-1.22v3.79c-.52-.17-2.29-.43-3.32.86zm-8.55 4.72c0 2.43 2.6 1.68 3.12 1.46v3.36c-.55.3-1.54.54-2.89.54a4.15 4.15 0 01-4.27-4.24l.01-13.17 4.02-.86v3.54h3.14V9.1h-3.13v5.85zm-4.91.7c0 2.97-2.31 4.66-5.73 4.66a11.2 11.2 0 01-4.46-.93v-3.93c1.38.75 3.1 1.31 4.46 1.31.92 0 1.53-.24 1.53-1C6.26 13.77 0 14.51 0 9.95 0 7.04 2.28 5.3 5.62 5.3c1.36 0 2.72.2 4.09.75v3.88a9.23 9.23 0 00-4.1-1.06c-.86 0-1.44.25-1.44.93 0 1.85 6.29.97 6.29 5.88z"
                />
              </svg>
            </div>

            <p className="text-sm text-gray-600 mb-3">
              Visa、Mastercard、American Express、JCBなど
            </p>

            <div className="flex items-center text-xs text-gray-500">
              <svg
                className="w-4 h-4 mr-1"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z"
                  clipRule="evenodd"
                />
              </svg>
              安全な決済
            </div>
          </Card>
        </button>

        {/* XRPL Payment */}
        <button
          onClick={() => handleSelect('xrpl')}
          className={`text-left transition-all ${
            selected === 'xrpl'
              ? 'ring-2 ring-purple-500'
              : 'hover:border-purple-300'
          }`}
        >
          <Card className="p-6 h-full">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center">
                <div
                  className={`w-6 h-6 rounded-full border-2 flex items-center justify-center mr-3 ${
                    selected === 'xrpl'
                      ? 'border-purple-500 bg-purple-500'
                      : 'border-gray-300'
                  }`}
                >
                  {selected === 'xrpl' && (
                    <svg
                      className="w-4 h-4 text-white"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fillRule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clipRule="evenodd"
                      />
                    </svg>
                  )}
                </div>
                <h3 className="text-lg font-semibold text-gray-900">
                  XRP決済
                </h3>
              </div>
              <div className="text-2xl">💎</div>
            </div>

            <p className="text-sm text-gray-600 mb-3">
              XRPLウォレットから直接支払い
            </p>

            <div className="space-y-2">
              <div className="flex items-center text-xs text-green-600">
                <svg
                  className="w-4 h-4 mr-1"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clipRule="evenodd"
                  />
                </svg>
                低手数料
              </div>
              <div className="flex items-center text-xs text-green-600">
                <svg
                  className="w-4 h-4 mr-1"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clipRule="evenodd"
                  />
                </svg>
                即時決済
              </div>
            </div>
          </Card>
        </button>
      </div>

      {/* Payment Method Info */}
      {selected === 'xrpl' && (
        <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
          <div className="flex items-start">
            <svg
              className="w-5 h-5 text-purple-600 mt-0.5 mr-3 flex-shrink-0"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                clipRule="evenodd"
              />
            </svg>
            <div>
              <h4 className="text-sm font-semibold text-purple-900">
                XRP決済について
              </h4>
              <p className="text-xs text-purple-700 mt-1">
                あなたのXRPLウォレットから直接支払います。
                決済完了後、自動的にNFTがミントされます。
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
