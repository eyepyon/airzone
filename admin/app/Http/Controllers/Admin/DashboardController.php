<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\DB;
use Carbon\Carbon;

class DashboardController extends Controller
{
    public function index()
    {
        $now = Carbon::now();
        $today = $now->startOfDay();
        $thisMonth = $now->copy()->startOfMonth();
        
        // 基本統計
        $stats = [
            'users' => DB::table('users')->count(),
            'orders' => DB::table('orders')->count(),
            'products' => DB::table('products')->count(),
            'nfts' => DB::table('nft_mints')->where('status', 'completed')->count(),
            'revenue' => DB::table('orders')->where('status', 'completed')->sum('total_amount'),
        ];

        // DAU (Daily Active Users) - 今日ログインしたユニークユーザー数
        $dau = DB::table('user_activities')
            ->where('activity_type', 'login')
            ->where('created_at', '>=', $today)
            ->distinct('user_id')
            ->count('user_id');

        // MAU (Monthly Active Users) - 今月ログインしたユニークユーザー数
        $mau = DB::table('user_activities')
            ->where('activity_type', 'login')
            ->where('created_at', '>=', $thisMonth)
            ->distinct('user_id')
            ->count('user_id');

        // 今日のダウンロード数
        $dailyDownloads = DB::table('user_activities')
            ->where('activity_type', 'download')
            ->where('created_at', '>=', $today)
            ->count();

        // 今月のダウンロード数
        $monthlyDownloads = DB::table('user_activities')
            ->where('activity_type', 'download')
            ->where('created_at', '>=', $thisMonth)
            ->count();

        // 総ダウンロード数
        $totalDownloads = DB::table('user_activities')
            ->where('activity_type', 'download')
            ->count();

        // 過去7日間のDAU推移
        $dauTrend = [];
        for ($i = 6; $i >= 0; $i--) {
            $date = $now->copy()->subDays($i)->startOfDay();
            $nextDate = $date->copy()->addDay();
            $count = DB::table('user_activities')
                ->where('activity_type', 'login')
                ->where('created_at', '>=', $date)
                ->where('created_at', '<', $nextDate)
                ->distinct('user_id')
                ->count('user_id');
            
            $dauTrend[] = [
                'date' => $date->format('m/d'),
                'count' => $count
            ];
        }

        // 過去7日間のダウンロード推移
        $downloadTrend = [];
        for ($i = 6; $i >= 0; $i--) {
            $date = $now->copy()->subDays($i)->startOfDay();
            $nextDate = $date->copy()->addDay();
            $count = DB::table('user_activities')
                ->where('activity_type', 'download')
                ->where('created_at', '>=', $date)
                ->where('created_at', '<', $nextDate)
                ->count();
            
            $downloadTrend[] = [
                'date' => $date->format('m/d'),
                'count' => $count
            ];
        }

        // エンゲージメント率 (DAU/MAU)
        $engagementRate = $mau > 0 ? round(($dau / $mau) * 100, 1) : 0;

        $recentOrders = DB::table('orders')
            ->join('users', 'orders.user_id', '=', 'users.id')
            ->select('orders.*', 'users.name as user_name', 'users.email as user_email')
            ->orderBy('orders.created_at', 'desc')
            ->limit(10)
            ->get();

        $metrics = [
            'dau' => $dau,
            'mau' => $mau,
            'dailyDownloads' => $dailyDownloads,
            'monthlyDownloads' => $monthlyDownloads,
            'totalDownloads' => $totalDownloads,
            'engagementRate' => $engagementRate,
            'dauTrend' => $dauTrend,
            'downloadTrend' => $downloadTrend,
        ];

        return view('admin.dashboard', compact('stats', 'recentOrders', 'metrics'));
    }
}
