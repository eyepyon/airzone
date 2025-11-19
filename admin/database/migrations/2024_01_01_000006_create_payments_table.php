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
        Schema::create('payments', function (Blueprint $table) {
            $table->string('id', 36)->primary();
            $table->string('order_id', 36)->nullable(false);
            $table->string('stripe_payment_intent_id', 255)->unique()->nullable(false);
            $table->integer('amount')->nullable(false)->comment('Amount in smallest currency unit');
            $table->string('currency', 3)->default('jpy')->nullable(false);
            $table->enum('status', ['pending', 'processing', 'succeeded', 'failed', 'cancelled'])
                  ->default('pending')
                  ->nullable(false);
            $table->timestamp('created_at')->useCurrent();
            $table->timestamp('updated_at')->useCurrent()->useCurrentOnUpdate();
            
            // Foreign keys
            $table->foreign('order_id')
                  ->references('id')
                  ->on('orders')
                  ->onDelete('cascade');
            
            // Indexes
            $table->index('order_id', 'idx_order_id');
            $table->index('stripe_payment_intent_id', 'idx_stripe_payment_intent_id');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('payments');
    }
};
