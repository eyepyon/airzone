@extends('admin.layout')

@section('title', 'エスクローキャンペーン詳細')

@section('content')
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>エスクローキャンペーン詳細</h1>
        <div>
            <a href="{{ route('admin.escrow-campaigns.edit', $campaign->id) }}" class="btn btn-warning">
                <i class="fas fa-edit"></i> 編集
            </a>
            <a href="{{ route('admin.escrow-campaigns.index') }}" class="btn btn-secondary">
                <i class="fas fa-arrow-left"></i> 戻る
            </a>
        </div>
    </div>

    <div class="row">
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="mb-0">キャンペーン情報</h5>
                </div>
                <div class="card-body">
                    <table class="table table-borderless">
                        <tr>
                            <th width="40%">キャンペーン名:</th>
                            <td>{{ $campaign->name }}</td>
                        </tr>
                        <tr>
                            <th>説明:</th>
                            <td>{{ $campaign->description ?? '-' }}</td>
                        </tr>
                        <tr>
                            <th>最小金額:</th>
                            <td>{{ number_format($campaign->min_amount_drops / 1000000, 2) }} XRP</td>
                        </tr>
                        <tr>
                            <th>ロック期間:</th>
                            <td>{{ $campaign->lock_days }}日</td>
                        </tr>
                        <tr>
                            <th>開始日時:</th>
                            <td>{{ \Carbon\Carbon::parse($campaign->start_date)->format('Y/m/d H:i') }}</td>
                        </tr>
                        <tr>
                            <th>終了日時:</th>
                            <td>{{ \Carbon\Carbon::parse($campaign->end_date)->format('Y/m/d H:i') }}</td>
                        </tr>
                        <tr>
                            <th>参加者数:</th>
                            <td>
                                {{ $campaign->current_participants }}
                                @if($campaign->max_participants)
                                    / {{ $campaign->max_participants }}
                                @endif
                            </td>
                        </tr>
                        <tr>
                            <th>ステータス:</th>
                            <td>
                                @if($campaign->is_active)
                                    <span class="badge bg-success">有効</span>
                                @else
                                    <span class="badge bg-secondary">無効</span>
                                @endif
                            </td>
                        </tr>
                    </table>
                </div>
            </div>
        </div>

        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="mb-0">NFT報酬</h5>
                </div>
                <div class="card-body">
                    @if($campaign->nft_reward_image_url)
                        <div class="text-center mb-3">
                            <img src="{{ $campaign->nft_reward_image_url }}"
                                 alt="{{ $campaign->nft_reward_name }}"
                                 class="img-fluid" style="max-height: 200px;">
                        </div>
                    @endif
                    <table class="table table-borderless">
                        <tr>
                            <th width="40%">NFT名:</th>
                            <td>{{ $campaign->nft_reward_name }}</td>
                        </tr>
                        <tr>
                            <th>NFT説明:</th>
                            <td>{{ $campaign->nft_reward_description ?? '-' }}</td>
                        </tr>
                        <tr>
                            <th>画像URL:</th>
                            <td>
                                @if($campaign->nft_reward_image_url)
                                    <a href="{{ $campaign->nft_reward_image_url }}" target="_blank">
                                        {{ Str::limit($campaign->nft_reward_image_url, 50) }}
                                    </a>
                                @else
                                    -
                                @endif
                            </td>
                        </tr>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <div class="card">
        <div class="card-header">
            <h5 class="mb-0">参加者一覧</h5>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>ユーザー</th>
                            <th>ウォレットアドレス</th>
                            <th>ステーク金額</th>
                            <th>ロック期間</th>
                            <th>完了予定</th>
                            <th>ステータス</th>
                            <th>参加日時</th>
                        </tr>
                    </thead>
                    <tbody>
                        @forelse($stakes as $stake)
                            <tr>
                                <td>
                                    <strong>{{ $stake->username }}</strong><br>
                                    <small class="text-muted">{{ $stake->email }}</small>
                                </td>
                                <td>
                                    <small>{{ Str::limit($stake->wallet_address, 20) }}</small>
                                </td>
                                <td>{{ number_format($stake->amount_drops / 1000000, 2) }} XRP</td>
                                <td>{{ $stake->lock_days }}日</td>
                                <td>{{ \Carbon\Carbon::parse($stake->finish_after)->format('Y/m/d H:i') }}</td>
                                <td>
                                    @if($stake->status === 'active')
                                        <span class="badge bg-primary">アクティブ</span>
                                    @elseif($stake->status === 'completed')
                                        <span class="badge bg-success">完了</span>
                                    @else
                                        <span class="badge bg-secondary">{{ $stake->status }}</span>
                                    @endif
                                    @if($stake->nft_awarded)
                                        <span class="badge bg-info">NFT付与済</span>
                                    @endif
                                </td>
                                <td>{{ \Carbon\Carbon::parse($stake->created_at)->format('Y/m/d H:i') }}</td>
                            </tr>
                        @empty
                            <tr>
                                <td colspan="7" class="text-center text-muted">
                                    参加者がいません
                                </td>
                            </tr>
                        @endforelse
                    </tbody>
                </table>
            </div>

            <div class="mt-3">
                {{ $stakes->links() }}
            </div>
        </div>
    </div>
</div>
@endsection
