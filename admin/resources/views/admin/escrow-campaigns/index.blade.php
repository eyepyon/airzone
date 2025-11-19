@extends('admin.layout')

@section('title', 'エスクローキャンペーン管理')

@section('content')
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>エスクローキャンペーン管理</h1>
        <div>
            <a href="{{ route('admin.escrow-campaigns.stats') }}" class="btn btn-info">
                <i class="fas fa-chart-bar"></i> 統計
            </a>
            <a href="{{ route('admin.escrow-campaigns.create') }}" class="btn btn-primary">
                <i class="fas fa-plus"></i> 新規作成
            </a>
        </div>
    </div>

    @if(session('success'))
        <div class="alert alert-success alert-dismissible fade show" role="alert">
            {{ session('success') }}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    @endif

    <div class="card">
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>キャンペーン名</th>
                            <th>最小金額</th>
                            <th>ロック期間</th>
                            <th>NFT報酬</th>
                            <th>期間</th>
                            <th>参加者数</th>
                            <th>ステータス</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody>
                        @forelse($campaigns as $campaign)
                            <tr>
                                <td>
                                    <strong>{{ $campaign->name }}</strong>
                                    @if($campaign->description)
                                        <br><small class="text-muted">{{ Str::limit($campaign->description, 50) }}</small>
                                    @endif
                                </td>
                                <td>{{ number_format($campaign->min_amount_drops / 1000000, 2) }} XRP</td>
                                <td>{{ $campaign->lock_days }}日</td>
                                <td>{{ $campaign->nft_reward_name }}</td>
                                <td>
                                    <small>
                                        {{ \Carbon\Carbon::parse($campaign->start_date)->format('Y/m/d') }}<br>
                                        ～ {{ \Carbon\Carbon::parse($campaign->end_date)->format('Y/m/d') }}
                                    </small>
                                </td>
                                <td>
                                    {{ $campaign->current_participants }}
                                    @if($campaign->max_participants)
                                        / {{ $campaign->max_participants }}
                                    @endif
                                </td>
                                <td>
                                    @if($campaign->is_active)
                                        <span class="badge bg-success">有効</span>
                                    @else
                                        <span class="badge bg-secondary">無効</span>
                                    @endif
                                </td>
                                <td>
                                    <a href="{{ route('admin.escrow-campaigns.show', $campaign->id) }}"
                                       class="btn btn-sm btn-info" title="詳細">
                                        <i class="fas fa-eye"></i>
                                    </a>
                                    <a href="{{ route('admin.escrow-campaigns.edit', $campaign->id) }}"
                                       class="btn btn-sm btn-warning" title="編集">
                                        <i class="fas fa-edit"></i>
                                    </a>
                                    <form action="{{ route('admin.escrow-campaigns.destroy', $campaign->id) }}"
                                          method="POST" class="d-inline"
                                          onsubmit="return confirm('本当に削除しますか？');">
                                        @csrf
                                        @method('DELETE')
                                        <button type="submit" class="btn btn-sm btn-danger" title="削除">
                                            <i class="fas fa-trash"></i>
                                        </button>
                                    </form>
                                </td>
                            </tr>
                        @empty
                            <tr>
                                <td colspan="8" class="text-center text-muted">
                                    キャンペーンがありません
                                </td>
                            </tr>
                        @endforelse
                    </tbody>
                </table>
            </div>

            <div class="mt-3">
                {{ $campaigns->links() }}
            </div>
        </div>
    </div>
</div>
@endsection
