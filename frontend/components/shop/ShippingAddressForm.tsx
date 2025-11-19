'use client';

import { useState } from 'react';
import type { ShippingAddress } from '@/types';
import Button from '@/components/ui/Button';

interface ShippingAddressFormProps {
  onSubmit: (address: ShippingAddress) => void;
  onCancel?: () => void;
  initialData?: ShippingAddress;
}

const PREFECTURES = [
  '北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県',
  '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県',
  '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県',
  '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府', '兵庫県',
  '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県', '山口県',
  '徳島県', '香川県', '愛媛県', '高知県', '福岡県', '佐賀県', '長崎県',
  '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県',
];

const DELIVERY_TIMES = [
  '指定なし',
  '午前中（8:00-12:00）',
  '14:00-16:00',
  '16:00-18:00',
  '18:00-20:00',
  '19:00-21:00',
];

export default function ShippingAddressForm({
  onSubmit,
  onCancel,
  initialData,
}: ShippingAddressFormProps) {
  const [formData, setFormData] = useState<ShippingAddress>(
    initialData || {
      recipient_name: '',
      postal_code: '',
      prefecture: '',
      city: '',
      address_line1: '',
      address_line2: '',
      phone_number: '',
      delivery_time_preference: '',
    }
  );

  const [errors, setErrors] = useState<Partial<Record<keyof ShippingAddress, string>>>({});

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    // Clear error when user starts typing
    if (errors[name as keyof ShippingAddress]) {
      setErrors((prev) => ({ ...prev, [name]: undefined }));
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Partial<Record<keyof ShippingAddress, string>> = {};

    if (!formData.recipient_name.trim()) {
      newErrors.recipient_name = '受取人名を入力してください';
    }

    if (!formData.postal_code.trim()) {
      newErrors.postal_code = '郵便番号を入力してください';
    } else if (!/^\d{3}-?\d{4}$/.test(formData.postal_code)) {
      newErrors.postal_code = '正しい郵便番号を入力してください（例: 123-4567）';
    }

    if (!formData.prefecture) {
      newErrors.prefecture = '都道府県を選択してください';
    }

    if (!formData.city.trim()) {
      newErrors.city = '市区町村を入力してください';
    }

    if (!formData.address_line1.trim()) {
      newErrors.address_line1 = '番地を入力してください';
    }

    if (!formData.phone_number.trim()) {
      newErrors.phone_number = '電話番号を入力してください';
    } else if (!/^0\d{9,10}$/.test(formData.phone_number.replace(/-/g, ''))) {
      newErrors.phone_number = '正しい電話番号を入力してください';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validateForm()) {
      onSubmit(formData);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-gray-900 mb-4">配送先情報</h2>
        <p className="text-sm text-gray-600 mb-6">
          商品の配送先住所を入力してください
        </p>
      </div>

      {/* Recipient Name */}
      <div>
        <label htmlFor="recipient_name" className="block text-sm font-medium text-gray-700 mb-2">
          受取人名 <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          id="recipient_name"
          name="recipient_name"
          value={formData.recipient_name}
          onChange={handleChange}
          className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
            errors.recipient_name ? 'border-red-500' : 'border-gray-300'
          }`}
          placeholder="山田 太郎"
        />
        {errors.recipient_name && (
          <p className="mt-1 text-sm text-red-600">{errors.recipient_name}</p>
        )}
      </div>

      {/* Postal Code */}
      <div>
        <label htmlFor="postal_code" className="block text-sm font-medium text-gray-700 mb-2">
          郵便番号 <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          id="postal_code"
          name="postal_code"
          value={formData.postal_code}
          onChange={handleChange}
          className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
            errors.postal_code ? 'border-red-500' : 'border-gray-300'
          }`}
          placeholder="123-4567"
        />
        {errors.postal_code && (
          <p className="mt-1 text-sm text-red-600">{errors.postal_code}</p>
        )}
      </div>

      {/* Prefecture */}
      <div>
        <label htmlFor="prefecture" className="block text-sm font-medium text-gray-700 mb-2">
          都道府県 <span className="text-red-500">*</span>
        </label>
        <select
          id="prefecture"
          name="prefecture"
          value={formData.prefecture}
          onChange={handleChange}
          className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
            errors.prefecture ? 'border-red-500' : 'border-gray-300'
          }`}
        >
          <option value="">選択してください</option>
          {PREFECTURES.map((pref) => (
            <option key={pref} value={pref}>
              {pref}
            </option>
          ))}
        </select>
        {errors.prefecture && (
          <p className="mt-1 text-sm text-red-600">{errors.prefecture}</p>
        )}
      </div>

      {/* City */}
      <div>
        <label htmlFor="city" className="block text-sm font-medium text-gray-700 mb-2">
          市区町村 <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          id="city"
          name="city"
          value={formData.city}
          onChange={handleChange}
          className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
            errors.city ? 'border-red-500' : 'border-gray-300'
          }`}
          placeholder="渋谷区"
        />
        {errors.city && <p className="mt-1 text-sm text-red-600">{errors.city}</p>}
      </div>

      {/* Address Line 1 */}
      <div>
        <label htmlFor="address_line1" className="block text-sm font-medium text-gray-700 mb-2">
          番地 <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          id="address_line1"
          name="address_line1"
          value={formData.address_line1}
          onChange={handleChange}
          className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
            errors.address_line1 ? 'border-red-500' : 'border-gray-300'
          }`}
          placeholder="道玄坂1-2-3"
        />
        {errors.address_line1 && (
          <p className="mt-1 text-sm text-red-600">{errors.address_line1}</p>
        )}
      </div>

      {/* Address Line 2 */}
      <div>
        <label htmlFor="address_line2" className="block text-sm font-medium text-gray-700 mb-2">
          建物名・部屋番号（任意）
        </label>
        <input
          type="text"
          id="address_line2"
          name="address_line2"
          value={formData.address_line2}
          onChange={handleChange}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="〇〇ビル 101号室"
        />
      </div>

      {/* Phone Number */}
      <div>
        <label htmlFor="phone_number" className="block text-sm font-medium text-gray-700 mb-2">
          電話番号 <span className="text-red-500">*</span>
        </label>
        <input
          type="tel"
          id="phone_number"
          name="phone_number"
          value={formData.phone_number}
          onChange={handleChange}
          className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
            errors.phone_number ? 'border-red-500' : 'border-gray-300'
          }`}
          placeholder="090-1234-5678"
        />
        {errors.phone_number && (
          <p className="mt-1 text-sm text-red-600">{errors.phone_number}</p>
        )}
      </div>

      {/* Delivery Time Preference */}
      <div>
        <label
          htmlFor="delivery_time_preference"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          配送希望時間帯（任意）
        </label>
        <select
          id="delivery_time_preference"
          name="delivery_time_preference"
          value={formData.delivery_time_preference}
          onChange={handleChange}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          {DELIVERY_TIMES.map((time) => (
            <option key={time} value={time}>
              {time}
            </option>
          ))}
        </select>
      </div>

      {/* Buttons */}
      <div className="flex gap-4 pt-4">
        <Button type="submit" variant="primary" className="flex-1">
          この住所で注文する
        </Button>
        {onCancel && (
          <Button type="button" variant="secondary" onClick={onCancel} className="flex-1">
            キャンセル
          </Button>
        )}
      </div>
    </form>
  );
}
