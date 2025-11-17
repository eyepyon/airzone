<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\DB;

class ReferralController extends Controller
{
    /**
     * 紹介一覧を表示
     */
    public function index()
    {
        // ユーザーごとの紹介統計と重要度スコアを取得
        $referralStats = DB::table('users')
            ->leftJoin('referrals', 'users.id', '=', 'referrals.referrer_id')
            ->leftJoin('referral_clicks', 'users.id', '=', 'referral_clicks.referrer_id')
            ->select(
                'users.id',
                'users.name',
                'users.email',
                'users.referral_code',
                'users.coins',
                'users.importance_score',
                'users.importance_level',
                DB::raw('COUNT(DISTINCT referrals.id) as total_referrals'),
                DB::raw('COUNT(DISTINCT CASE WHEN referrals.status = "completed" THEN referrals.id END) as completed_referrals'),
                DB::raw('COUNT(DISTINCT CASE WHEN referrals.status = "pending" THEN referrals.id END) as pending_referrals'),
                DB::raw('SUM(CASE WHEN referrals.status = "completed" THEN referrals.coins_awarded ELSE 0 END) as total_coins_earned'),
                DB::raw('COUNT(DISTINCT referral_clicks.id) as click_count')
            )
            ->groupBy('users.id', 'users.name', 'users.email', 'users.referral_code', 'users.coins', 'users.importance_score', 'users.importance_level')
            ->having('total_referrals', '>', 0)
            ->orderBy('users.importance_score', 'desc')
            ->paginate(20);

        // 全体統計
        $overallStats = [
            'total_users_with_referrals' => DB::table('users')
                ->whereNotNull('referral_code')
                ->whereExists(function ($query) {
                    $query->select(DB::raw(1))
                        ->from('referrals')
                        ->whereColumn('referrals.referrer_id', 'users.id');
                })
                ->count(),
            'total_referrals' => DB::table('referrals')->count(),
            'completed_referrals' => DB::table('referrals')->where('status', 'completed')->count(),
            'pending_referrals' => DB::table('referrals')->where('status', 'pending')->count(),
            'total_coins_awarded' => DB::table('referrals')->where('status', 'completed')->sum('coins_awarded'),
            'total_referred_users' => DB::table('users')->whereNotNull('referred_by')->count(),
        ];

        return view('admin.referrals.index', compact('referralStats', 'overallStats'));
    }

    /**
     * ユーザーの紹介詳細を表示
     */
    public function show($userId)
    {
        // ユーザー情報
        $user = DB::table('users')->where('id', $userId)->first();
        
        if (!$user) {
            abort(404);
        }

        // 紹介履歴
        $referrals = DB::table('referrals')
            ->join('users as referred_users', 'referrals.referred_id', '=', 'referred_users.id')
            ->where('referrals.referrer_id', $userId)
            ->select(
                'referrals.*',
                'referred_users.name as referred_name',
                'referred_users.email as referred_email'
            )
            ->orderBy('referrals.created_at', 'desc')
            ->get();

        // コイン取引履歴
        $coinTransactions = DB::table('coin_transactions')
            ->where('user_id', $userId)
            ->orderBy('created_at', 'desc')
            ->limit(50)
            ->get();

        // 統計
        $stats = [
            'total_referrals' => $referrals->count(),
            'completed_referrals' => $referrals->where('status', 'completed')->count(),
            'pending_referrals' => $referrals->where('status', 'pending')->count(),
            'total_coins_earned' => $referrals->where('status', 'completed')->sum('coins_awarded'),
            'current_coins' => $user->coins ?? 0,
        ];

        return view('admin.referrals.show', compact('user', 'referrals', 'coinTransactions', 'stats'));
    }

    /**
     * 紹介ランキング
     */
    public function ranking()
    {
        // 紹介数ランキング
        $topReferrers = DB::table('users')
            ->join('referrals', 'users.id', '=', 'referrals.referrer_id')
            ->select(
                'users.id',
                'users.name',
                'users.email',
                'users.referral_code',
                DB::raw('COUNT(DISTINCT referrals.id) as referral_count'),
                DB::raw('SUM(CASE WHEN referrals.status = "completed" THEN referrals.coins_awarded ELSE 0 END) as total_coins')
            )
            ->groupBy('users.id', 'users.name', 'users.email', 'users.referral_code')
            ->orderBy('referral_count', 'desc')
            ->limit(50)
            ->get();

        return view('admin.referrals.ranking', compact('topReferrers'));
    }
}
