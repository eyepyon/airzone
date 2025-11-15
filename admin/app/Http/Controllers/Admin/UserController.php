<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class UserController extends Controller
{
    public function index(Request $request)
    {
        $query = DB::table('users')
            ->leftJoin('wallets', 'users.id', '=', 'wallets.user_id')
            ->select('users.*', 'wallets.address as wallet_address');

        if ($request->search) {
            $query->where(function($q) use ($request) {
                $q->where('users.email', 'like', "%{$request->search}%")
                  ->orWhere('users.name', 'like', "%{$request->search}%");
            });
        }

        $users = $query->orderBy('users.created_at', 'desc')->paginate(20);
        return view('admin.users.index', compact('users'));
    }

    public function show($id)
    {
        $user = DB::table('users')->where('id', $id)->first();
        if (!$user) abort(404);

        $wallet = DB::table('wallets')->where('user_id', $id)->first();
        $orders = DB::table('orders')->where('user_id', $id)->orderBy('created_at', 'desc')->get();
        $nfts = DB::table('nft_mints')->where('user_id', $id)->orderBy('created_at', 'desc')->get();

        return view('admin.users.show', compact('user', 'wallet', 'orders', 'nfts'));
    }

    public function destroy($id)
    {
        DB::table('users')->where('id', $id)->delete();
        return redirect()->route('users.index')->with('success', 'ユーザーを削除しました');
    }
}
