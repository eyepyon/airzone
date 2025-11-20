-- 商品の受け取り方法に「AirZOne受取」を追加し、複数選択可能にする

-- 1. productsテーブルに受け取り方法の選択肢を保存するカラムを追加
ALTER TABLE products 
ADD COLUMN IF NOT EXISTS delivery_options JSON DEFAULT NULL COMMENT '利用可能な受け取り方法の配列';

-- 既存のdelivery_methodカラムのデータをdelivery_optionsに移行
UPDATE products 
SET delivery_options = JSON_ARRAY(delivery_method)
WHERE delivery_method IS NOT NULL AND delivery_options IS NULL;

-- 2. ordersテーブルに選択された受け取り方法を保存するカラムを追加
ALTER TABLE orders 
ADD COLUMN IF NOT EXISTS selected_delivery_method VARCHAR(50) DEFAULT NULL COMMENT 'ユーザーが選択した受け取り方法';

-- 3. order_itemsテーブルにも受け取り方法を保存（商品ごとに異なる可能性があるため）
ALTER TABLE order_items 
ADD COLUMN IF NOT EXISTS selected_delivery_method VARCHAR(50) DEFAULT NULL COMMENT 'この商品の受け取り方法';

-- インデックスを追加
CREATE INDEX IF NOT EXISTS idx_orders_delivery_method ON orders(selected_delivery_method);
CREATE INDEX IF NOT EXISTS idx_order_items_delivery_method ON order_items(selected_delivery_method);
