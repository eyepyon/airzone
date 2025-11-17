<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Http;

class BatchTransferController extends Controller
{
    private $apiBaseUrl;
    
    public function __construct()
    {
        $this->apiBaseUrl = env('API_BASE_URL', 'http://localhost:5000');
    }
    
    /**
     * バッチ送金履歴一覧
     */
    public function index(Request $request)
    {
        $limit = $request->get('limit', 50);
        $offset = $request->get('offset', 0);
        
        // APIから履歴を取得
        $response = Http::withToken(session('admin_token'))
            ->get("{$this->apiBaseUrl}/api/v1/batch-transfer/history", [
                'limit' => $limit,
                'offset' => $offset
            ]);
        
        if ($response->successful()) {
            $data = $response->json();
            
            return view('admin.batch-transfers.index', [
                'transfers' => $data['transfers'] ?? [],
                'total' => $data['total'] ?? 0,
                'limit' => $limit,
                'offset' => $offset
            ]);
        }
        
        return view('admin.batch-transfers.index', [
            'transfers' => [],
            'total' => 0,
            'error' => 'Failed to load batch transfer history'
        ]);
    }
    
    /**
     * バッチ送金フォーム
     */
    public function create()
    {
        // ユーザー一覧を取得
        $users = DB::table('users')
            ->select('id', 'email', 'wallet_address', 'importance_level')
            ->whereNotNull('wallet_address')
            ->orderBy('importance_score', 'desc')
            ->get();
        
        return view('admin.batch-transfers.create', [
            'users' => $users
        ]);
    }
    
    /**
     * バッチ送金プレビュー
     */
    public function preview(Request $request)
    {
        $request->validate([
            'user_ids' => 'required|array',
            'amount_xrp' => 'required|numeric|min:0.000001'
        ]);
        
        // APIでプレビュー
        $response = Http::withToken(session('admin_token'))
            ->post("{$this->apiBaseUrl}/api/v1/batch-transfer/preview", [
                'user_ids' => $request->user_ids,
                'amount_xrp' => $request->amount_xrp
            ]);
        
        if ($response->successful()) {
            return response()->json($response->json());
        }
        
        return response()->json([
            'error' => 'Preview failed'
        ], 500);
    }
    
    /**
     * バッチ送金実行
     */
    public function send(Request $request)
    {
        $request->validate([
            'user_ids' => 'required|array',
            'amount_xrp' => 'required|numeric|min:0.000001',
            'reason' => 'required|string|max:500'
        ]);
        
        // APIでバッチ送金実行
        $response = Http::withToken(session('admin_token'))
            ->post("{$this->apiBaseUrl}/api/v1/batch-transfer/send", [
                'user_ids' => $request->user_ids,
                'amount_xrp' => $request->amount_xrp,
                'reason' => $request->reason
            ]);
        
        if ($response->successful()) {
            $result = $response->json();
            
            return redirect()
                ->route('admin.batch-transfers.index')
                ->with('success', "Batch transfer completed: {$result['summary']['successful']} successful, {$result['summary']['failed']} failed");
        }
        
        return redirect()
            ->back()
            ->with('error', 'Batch transfer failed: ' . $response->json()['error'] ?? 'Unknown error');
    }
    
    /**
     * VIPユーザーへのバッチ送金
     */
    public function sendToVip(Request $request)
    {
        $request->validate([
            'min_importance_level' => 'required|in:Bronze,Silver,Gold,Platinum,Diamond',
            'amount_xrp' => 'required|numeric|min:0.000001',
            'reason' => 'required|string|max:500'
        ]);
        
        // APIでVIPバッチ送金実行
        $response = Http::withToken(session('admin_token'))
            ->post("{$this->apiBaseUrl}/api/v1/batch-transfer/send-to-vip", [
                'min_importance_level' => $request->min_importance_level,
                'amount_xrp' => $request->amount_xrp,
                'reason' => $request->reason
            ]);
        
        if ($response->successful()) {
            $result = $response->json();
            
            return redirect()
                ->route('admin.batch-transfers.index')
                ->with('success', "VIP batch transfer completed: {$result['summary']['successful']} successful, {$result['summary']['failed']} failed");
        }
        
        return redirect()
            ->back()
            ->with('error', 'VIP batch transfer failed: ' . $response->json()['error'] ?? 'Unknown error');
    }
    
    /**
     * トップ紹介者へのバッチ送金
     */
    public function sendToTopReferrers(Request $request)
    {
        $request->validate([
            'top_n' => 'required|integer|min:1|max:1000',
            'amount_xrp' => 'required|numeric|min:0.000001',
            'reason' => 'required|string|max:500'
        ]);
        
        // APIでトップ紹介者バッチ送金実行
        $response = Http::withToken(session('admin_token'))
            ->post("{$this->apiBaseUrl}/api/v1/batch-transfer/send-to-top-referrers", [
                'top_n' => $request->top_n,
                'amount_xrp' => $request->amount_xrp,
                'reason' => $request->reason
            ]);
        
        if ($response->successful()) {
            $result = $response->json();
            
            return redirect()
                ->route('admin.batch-transfers.index')
                ->with('success', "Top referrer batch transfer completed: {$result['summary']['successful']} successful, {$result['summary']['failed']} failed");
        }
        
        return redirect()
            ->back()
            ->with('error', 'Top referrer batch transfer failed: ' . $response->json()['error'] ?? 'Unknown error');
    }
    
    /**
     * 統計情報
     */
    public function stats()
    {
        $stats = DB::table('batch_transfer_stats')
            ->orderBy('transfer_date', 'desc')
            ->limit(30)
            ->get();
        
        $totalStats = DB::table('batch_transfers')
            ->where('status', 'success')
            ->selectRaw('
                COUNT(*) as total_transfers,
                SUM(amount_xrp) as total_amount_xrp,
                AVG(amount_xrp) as avg_amount_xrp,
                COUNT(DISTINCT user_id) as unique_users
            ')
            ->first();
        
        return view('admin.batch-transfers.stats', [
            'daily_stats' => $stats,
            'total_stats' => $totalStats
        ]);
    }
}
