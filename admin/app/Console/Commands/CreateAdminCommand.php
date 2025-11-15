<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use App\Models\Admin;
use Illuminate\Support\Facades\Hash;

class CreateAdminCommand extends Command
{
    protected $signature = 'admin:create {email?} {password?}';
    protected $description = '管理者アカウントを作成';

    public function handle()
    {
        $email = $this->argument('email') ?? $this->ask('メールアドレス');
        $password = $this->argument('password') ?? $this->secret('パスワード');
        $name = $this->ask('名前', 'Admin');

        Admin::create([
            'name' => $name,
            'email' => $email,
            'password' => Hash::make($password),
        ]);

        $this->info('管理者アカウントを作成しました');
        $this->info("Email: {$email}");
    }
}
