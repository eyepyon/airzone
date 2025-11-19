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
        Schema::create('order_items', function (Blueprint $table) {
            $table->string('id', 36)->primary();
            $table->string('order_id', 36)->nullable(false);
            $table->string('product_id', 36)->nullable(false);
            $table->integer('quantity')->nullable(false);
            $table->integer('unit_price')->nullable(false)->comment('Price per unit at time of order');
            $table->integer('subtotal')->nullable(false)->comment('quantity * unit_price');
            $table->timestamp('created_at')->useCurrent();
            $table->timestamp('updated_at')->useCurrent()->useCurrentOnUpdate();
            
            // Foreign keys
            $table->foreign('order_id')
                  ->references('id')
                  ->on('orders')
                  ->onDelete('cascade');
            
            $table->foreign('product_id')
                  ->references('id')
                  ->on('products');
            
            // Indexes
            $table->index('order_id', 'idx_order_id');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('order_items');
    }
};
