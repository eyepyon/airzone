<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('products', function (Blueprint $table) {
            $table->string('id', 36)->primary();
            $table->string('name', 255)->nullable(false);
            $table->text('description')->nullable();
            $table->integer('price')->nullable(false)->comment('Price in smallest currency unit (e.g., cents, yen)');
            $table->integer('stock_quantity')->nullable(false)->default(0);
            $table->string('image_url', 500)->nullable();
            $table->string('required_nft_id', 36)->nullable()->comment('Optional NFT requirement');
            $table->boolean('is_active')->default(true)->nullable(false);
            $table->timestamp('created_at')->useCurrent();
            $table->timestamp('updated_at')->useCurrent()->useCurrentOnUpdate();
            
            // Indexes
            $table->index('is_active', 'idx_is_active');
            $table->index('required_nft_id', 'idx_required_nft');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('products');
    }
};
