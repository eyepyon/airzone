@extends('admin.layout')

@section('title', 'エスクローキャンペーン統計')

@section('content')
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>エスクローキャンペーン統計</h1>
        <a href="{{ route('admin.escrow-campaigns.index') }}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> 戻る
        </a>
    </div>

    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card text-center">
                <div class="card-body">
                    <h6 class="text-muted">総キャンペーン数</h6>
                    <h2 class="mb-0">{{ $totalCampaigns }}</h2>
                    <small class="text-success">有効: {{ $activeCampaigns }}</small>
                </div>
            </div>
        </div>

        <div class="col-md-3">
            <div class="card text-center">
                <div class="card-body">
                    <h6 class="text-muted">総ステーク数</h6>
                    <h2 class="mb-0">{{ $totalStakes }}</h2>
                    <small class="text-primary">アクティブ: {{ $activeStakes }}</small>
                </div>
            </div>
        </div>

        <div class="col-md-3">
            <div class="card text-center">
                <div class="card-body">
                    <h6 class="text-muted">完了ステーク数</h6>
                    <h2 class="mb-0">{{ $completedStakes }}</h2>
                    <small class="text-success">
                        {{ $totalStakes > 0 ? number_format(($completedStakes / $totalStakes) * 100, 1) : 0 }}%
                    </small>
                </div>
            </div>
        </div>

        <div class="col-md-3">
            <div class="card text-center">
                <div class="card-body">
                    <h6 class="text-muted">総ロック額</h6>
                    <h2 class="mb-0">{{ number_format($totalLockedXRP, 2) }}</h2>
                    <small class="text-info">XRP</small>
                </div>
            </div>
        </div>
    </div>

    <div class="card">
        <div class="card-header">
            <h5 class="mb-0">キャンペーン別統計</h5>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>キャンペーン名</th>
                            <th>ステータス</th>
                            <th>総ステーク数</th>
                            <th>アクティブ</th>
                            <th>完了</th>
                            <th>ロック中XRP</th>
                            <th>完了率</th>
                        </tr>
                    </thead>
                    <tbody>
                        @forelse($campaignStats as $stat)
                            <tr>
                                <td>{{ $stat->name }}</td>
                                <td>
                                    @if($stat->is_active)
                                        <span class="badge bg-success">有効</span>
                                    @else
                                        <span class="badge bg-secondary">無効</span>
                                    @endif
                                </td>
                                <td>{{ $stat->total_stakes }}</td>
                                <td>
                                    <span class="badge bg-primary">{{ $stat->active_stakes }}</span>
                                </td>
                                <td>
                                    <span class="badge bg-success">{{ $stat->completed_stakes }}</span>
                                </td>
                                <td>{{ number_format($stat->locked_drops / 1000000, 2) }} XRP</td>
                                <td>
                                    @if($stat->total_stakes > 0)
                                        <div class="progress" style="height: 20px;">
                                            <div class="progress-bar bg-success"
                                                 role="progressbar"
                                                 style="width: {{ ($stat->completed_stakes / $stat->total_stakes) * 100 }}%">
                                                {{ number_format(($stat->completed_stakes / $stat->total_stakes) * 100, 1) }}%
                                            </div>
                                        </div>
                                    @else
                                        <span class="text-muted">-</span>
                                    @endif
                                </td>
                            </tr>
                        @empty
                            <tr>
                                <td colspan="7" class="text-center text-muted">
                                    データがありません
                                </td>
                            </tr>
                        @endforelse
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
@endsection
