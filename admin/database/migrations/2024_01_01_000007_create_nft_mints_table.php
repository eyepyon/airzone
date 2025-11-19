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
        Schema::create('nft_mints', function (Blueprint $table) {
            $table->string('id', 36)->primary();
            $table->string('user_id', 36)->nullable(false);
            $table->string('wallet_address', 255)->nullable(false);
            $table->string('nft_object_id', 255)->nullable();
            $table->string('transaction_digest', 255)->nullable();
            $table->enum('status', ['pending', 'minting', 'completed', 'failed'])
                  ->default('pending')
                  ->nullable(false);
            $table->json('nft_metadata')->nullable();
            $table->text('error_message')->nullable();
            $table->timestamp('created_at')->useCurrent();
            $table->timestamp('updated_at')->useCurrent()->useCurrentOnUpdate();
            
            // Foreign keys
            $table->foreign('user_id')
                  ->references('id')
                  ->on('users')
                  ->onDelete('cascade');
            
            // Indexes
            $table->index('user_id', 'idx_user_id');
            $table->index('wallet_address', 'idx_wallet_address');
            $table->index('status', 'idx_status');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('nft_mints');
    }
};
