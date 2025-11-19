<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;

class EscrowCampaignController extends Controller
{
    public function index()
    {
        $campaigns = DB::table('escrow_campaigns')
            ->orderBy('created_at', 'desc')
            ->paginate(20);

        return view('admin.escrow-campaigns.index', compact('campaigns'));
    }

    public function create()
    {
        return view('admin.escrow-campaigns.create');
    }

    public function store(Request $request)
    {
        $validated = $request->validate([
            'name' => 'required|max:255',
            'description' => 'nullable',
            'min_amount_drops' => 'required|integer|min:0',
            'lock_days' => 'required|integer|min:1',
            'nft_reward_name' => 'required|max:255',
            'nft_reward_description' => 'nullable',
            'nft_reward_image_url' => 'nullable|url',
            'start_date' => 'required|date',
            'end_date' => 'required|date|after:start_date',
            'max_participants' => 'nullable|integer|min:1',
            'is_active' => 'boolean',
        ]);

        $validated['id'] = Str::uuid();
        $validated['current_participants'] = 0;
        $validated['created_at'] = now();
        $validated['updated_at'] = now();
        $validated['is_active'] = $request->has('is_active');

        DB::table('escrow_campaigns')->insert($validated);

        return redirect()->route('admin.escrow-campaigns.index')
            ->with('success', 'エスクローキャンペーンを作成しました');
    }

    public function show($id)
    {
        $campaign = DB::table('escrow_campaigns')->where('id', $id)->first();

        if (!$campaign) {
            abort(404);
        }

        // キャンペーンの参加者一覧を取得
        $stakes = DB::table('escrow_stakes')
            ->join('users', 'escrow_stakes.user_id', '=', 'users.id')
            ->where('escrow_stakes.campaign_id', $id)
            ->select(
                'escrow_stakes.*',
                'users.username',
                'users.email'
            )
            ->orderBy('escrow_stakes.created_at', 'desc')
            ->paginate(20);

        return view('admin.escrow-campaigns.show', compact('campaign', 'stakes'));
    }

    public function edit($id)
    {
        $campaign = DB::table('escrow_campaigns')->where('id', $id)->first();

        if (!$campaign) {
            abort(404);
        }

        return view('admin.escrow-campaigns.edit', compact('campaign'));
    }

    public function update(Request $request, $id)
    {
        $validated = $request->validate([
            'name' => 'required|max:255',
            'description' => 'nullable',
            'min_amount_drops' => 'required|integer|min:0',
            'lock_days' => 'required|integer|min:1',
            'nft_reward_name' => 'required|max:255',
            'nft_reward_description' => 'nullable',
            'nft_reward_image_url' => 'nullable|url',
            'start_date' => 'required|date',
            'end_date' => 'required|date|after:start_date',
            'max_participants' => 'nullable|integer|min:1',
            'is_active' => 'boolean',
        ]);

        $validated['updated_at'] = now();
        $validated['is_active'] = $request->has('is_active');

        DB::table('escrow_campaigns')->where('id', $id)->update($validated);

        return redirect()->route('admin.escrow-campaigns.index')
            ->with('success', 'エスクローキャンペーンを更新しました');
    }

    public function destroy($id)
    {
        DB::table('escrow_campaigns')->where('id', $id)->delete();

        return redirect()->route('admin.escrow-campaigns.index')
            ->with('success', 'エスクローキャンペーンを削除しました');
    }

    public function stats()
    {
        // 統計情報を取得
        $totalCampaigns = DB::table('escrow_campaigns')->count();
        $activeCampaigns = DB::table('escrow_campaigns')->where('is_active', true)->count();
        $totalStakes = DB::table('escrow_stakes')->count();
        $activeStakes = DB::table('escrow_stakes')->where('status', 'active')->count();
        $completedStakes = DB::table('escrow_stakes')->where('status', 'completed')->count();

        // 総ロック額を計算
        $totalLockedDrops = DB::table('escrow_stakes')
            ->where('status', 'active')
            ->sum('amount_drops');
        $totalLockedXRP = $totalLockedDrops / 1000000;

        // キャンペーン別の統計
        $campaignStats = DB::table('escrow_campaigns')
            ->leftJoin('escrow_stakes', 'escrow_campaigns.id', '=', 'escrow_stakes.campaign_id')
            ->select(
                'escrow_campaigns.id',
                'escrow_campaigns.name',
                'escrow_campaigns.is_active',
                DB::raw('COUNT(escrow_stakes.id) as total_stakes'),
                DB::raw('SUM(CASE WHEN escrow_stakes.status = "active" THEN 1 ELSE 0 END) as active_stakes'),
                DB::raw('SUM(CASE WHEN escrow_stakes.status = "completed" THEN 1 ELSE 0 END) as completed_stakes'),
                DB::raw('SUM(CASE WHEN escrow_stakes.status = "active" THEN escrow_stakes.amount_drops ELSE 0 END) as locked_drops')
            )
            ->groupBy('escrow_campaigns.id', 'escrow_campaigns.name', 'escrow_campaigns.is_active')
            ->orderBy('total_stakes', 'desc')
            ->get();

        return view('admin.escrow-campaigns.stats', compact(
            'totalCampaigns',
            'activeCampaigns',
            'totalStakes',
            'activeStakes',
            'completedStakes',
            'totalLockedXRP',
            'campaignStats'
        ));
    }
}
