'use client';

import { useState } from 'react';
import type { DeliveryMethod } from '@/types';

interface DeliveryMethodSelectorProps {
  availableMethods: DeliveryMethod[];
  selectedMethod: DeliveryMethod | null;
  onSelect: (method: DeliveryMethod) => void;
}

const deliveryMethodLabels: Record<DeliveryMethod, { label: string; description: string; icon: string }> = {
  venue_pickup: {
    label: '会場内受取',
    description: 'イベント会場で商品を受け取ります',
    icon: '🏢',
  },
  home_delivery: {
    label: '宅配便配送',
    description: 'ご自宅まで配送します（送料別途）',
    icon: '📦',
  },
  airzone_pickup: {
    label: 'AirZOne受取',
    description: 'AirZOne店舗で受け取ります',
    icon: '🏪',
  },
};

export default function DeliveryMethodSelector({
  availableMethods,
  selectedMethod,
  onSelect,
}: DeliveryMethodSelectorProps) {
  return (
    <div className="space-y-3">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        受け取り方法を選択してください <span className="text-red-500">*</span>
      </label>
      {availableMethods.map((method) => {
        const info = deliveryMethodLabels[method];
        const isSelected = selectedMethod === method;

        return (
          <button
            key={method}
            type="button"
            onClick={() => onSelect(method)}
            className={`w-full text-left p-4 border-2 rounded-lg transition-all ${
              isSelected
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-200 hover:border-gray-300 bg-white'
            }`}
          >
            <div className="flex items-start">
              <span className="text-2xl mr-3">{info.icon}</span>
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <h3 className={`font-semibold ${isSelected ? 'text-blue-900' : 'text-gray-900'}`}>
                    {info.label}
                  </h3>
                  {isSelected && (
                    <svg className="w-5 h-5 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        fillRule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                        clipRule="evenodd"
                      />
                    </svg>
                  )}
                </div>
                <p className={`text-sm mt-1 ${isSelected ? 'text-blue-700' : 'text-gray-600'}`}>
                  {info.description}
                </p>
              </div>
            </div>
          </button>
        );
      })}
    </div>
  );
}
