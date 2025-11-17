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
    
    /**
     * 重要ユーザー一覧を表示
     */
    public function importance()
    {
        // 重要度スコアトップユーザーを取得
        $topUsers = DB::table('users')
            ->leftJoin(DB::raw('(SELECT user_id, COUNT(*) as purchase_count FROM orders WHERE status = "completed" GROUP BY user_id) as orders'), 'users.id', '=', 'orders.user_id')
            ->leftJoin(DB::raw('(SELECT referrer_id, COUNT(*) as referral_count FROM referrals WHERE status = "completed" GROUP BY referrer_id) as referrals'), 'users.id', '=', 'referrals.referrer_id')
            ->leftJoin(DB::raw('(SELECT user_id, COUNT(DISTINCT DATE(created_at)) as login_count FROM user_activities WHERE activity_type = "login" AND created_at >= DATE_SUB(NOW(), INTERVAL 90 DAY) GROUP BY user_id) as logins'), 'users.id', '=', 'logins.user_id')
            ->select(
                'users.id',
                'users.name',
                'users.email',
                'users.importance_score',
                'users.importance_level',
                DB::raw('COALESCE(orders.purchase_count, 0) as purchase_count'),
                DB::raw('COALESCE(referrals.referral_count, 0) as referral_count'),
                DB::raw('COALESCE(logins.login_count, 0) as login_count')
            )
            ->whereNotNull('users.importance_score')
            ->where('users.importance_score', '>', 0)
            ->orderBy('users.importance_score', 'desc')
            ->limit(100)
            ->get();
        
        return view('admin.users.importance', compact('topUsers'));
    }
    
    /**
     * ユーザーのスコアを更新
     */
    public function updateScore($id)
    {
        // スコア更新ロジックをここに実装
        // 実際にはバックエンドAPIを呼び出す
        
        return redirect()->back()->with('success', 'スコアを更新しました');
    }
}
