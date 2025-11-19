-- 商品テーブルにカテゴリーと受け取り方法を追加

-- カテゴリーカラムを追加
ALTER TABLE products 
ADD COLUMN category ENUM('goods', 'nft', 'ticket') DEFAULT 'goods' AFTER description;

-- 受け取り方法カラムを追加
ALTER TABLE products 
ADD COLUMN delivery_method ENUM('venue_pickup', 'home_delivery') DEFAULT 'venue_pickup' AFTER category;

-- 既存のデータにデフォルト値を設定
UPDATE products SET category = 'goods' WHERE category IS NULL;
UPDATE products SET delivery_method = 'venue_pickup' WHERE delivery_method IS NULL;
