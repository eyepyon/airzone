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
        Schema::create('referrals', function (Blueprint $table) {
            $table->string('id', 36)->primary();
            $table->string('referrer_id', 36)->nullable(false);
            $table->string('referred_id', 36)->nullable(false);
            $table->enum('status', ['pending', 'completed', 'cancelled'])
                  ->default('pending');
            $table->integer('coins_awarded')->default(0);
            $table->timestamp('created_at')->useCurrent();
            $table->timestamp('completed_at')->nullable();
            
            // Foreign keys
            $table->foreign('referrer_id')
                  ->references('id')
                  ->on('users');
            
            $table->foreign('referred_id')
                  ->references('id')
                  ->on('users');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('referrals');
    }
};
