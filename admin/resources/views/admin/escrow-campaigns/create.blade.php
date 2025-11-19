@extends('admin.layout')

@section('title', 'エスクローキャンペーン作成')

@section('content')
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>エスクローキャンペーン作成</h1>
        <a href="{{ route('admin.escrow-campaigns.index') }}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> 戻る
        </a>
    </div>

    <div class="card">
        <div class="card-body">
            <form action="{{ route('admin.escrow-campaigns.store') }}" method="POST">
                @csrf

                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="name" class="form-label">キャンペーン名 <span class="text-danger">*</span></label>
                            <input type="text" class="form-control @error('name') is-invalid @enderror"
                                   id="name" name="name" value="{{ old('name') }}" required>
                            @error('name')
                                <div class="invalid-feedback">{{ $message }}</div>
                            @enderror
                        </div>
                    </div>

                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="is_active" class="form-label">ステータス</label>
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" id="is_active"
                                       name="is_active" {{ old('is_active', true) ? 'checked' : '' }}>
                                <label class="form-check-label" for="is_active">有効</label>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="mb-3">
                    <label for="description" class="form-label">説明</label>
                    <textarea class="form-control @error('description') is-invalid @enderror"
                              id="description" name="description" rows="3">{{ old('description') }}</textarea>
                    @error('description')
                        <div class="invalid-feedback">{{ $message }}</div>
                    @enderror
                </div>

                <div class="row">
                    <div class="col-md-4">
                        <div class="mb-3">
                            <label for="min_amount_xrp" class="form-label">最小金額 (XRP) <span class="text-danger">*</span></label>
                            <input type="number" class="form-control @error('min_amount_drops') is-invalid @enderror"
                                   id="min_amount_xrp" step="0.01" min="0"
                                   value="{{ old('min_amount_xrp', 100) }}" required
                                   onchange="document.getElementById('min_amount_drops').value = Math.floor(this.value * 1000000)">
                            <input type="hidden" id="min_amount_drops" name="min_amount_drops"
                                   value="{{ old('min_amount_drops', 100000000) }}">
                            @error('min_amount_drops')
                                <div class="invalid-feedback">{{ $message }}</div>
                            @enderror
                        </div>
                    </div>

                    <div class="col-md-4">
                        <div class="mb-3">
                            <label for="lock_days" class="form-label">ロック期間 (日) <span class="text-danger">*</span></label>
                            <input type="number" class="form-control @error('lock_days') is-invalid @enderror"
                                   id="lock_days" name="lock_days" value="{{ old('lock_days', 30) }}"
                                   min="1" required>
                            @error('lock_days')
                                <div class="invalid-feedback">{{ $message }}</div>
                            @enderror
                        </div>
                    </div>

                    <div class="col-md-4">
                        <div class="mb-3">
                            <label for="max_participants" class="form-label">最大参加者数</label>
                            <input type="number" class="form-control @error('max_participants') is-invalid @enderror"
                                   id="max_participants" name="max_participants"
                                   value="{{ old('max_participants') }}" min="1">
                            <small class="text-muted">空欄の場合は無制限</small>
                            @error('max_participants')
                                <div class="invalid-feedback">{{ $message }}</div>
                            @enderror
                        </div>
                    </div>
                </div>

                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="start_date" class="form-label">開始日時 <span class="text-danger">*</span></label>
                            <input type="datetime-local" class="form-control @error('start_date') is-invalid @enderror"
                                   id="start_date" name="start_date" value="{{ old('start_date') }}" required>
                            @error('start_date')
                                <div class="invalid-feedback">{{ $message }}</div>
                            @enderror
                        </div>
                    </div>

                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="end_date" class="form-label">終了日時 <span class="text-danger">*</span></label>
                            <input type="datetime-local" class="form-control @error('end_date') is-invalid @enderror"
                                   id="end_date" name="end_date" value="{{ old('end_date') }}" required>
                            @error('end_date')
                                <div class="invalid-feedback">{{ $message }}</div>
                            @enderror
                        </div>
                    </div>
                </div>

                <hr class="my-4">
                <h5>NFT報酬設定</h5>

                <div class="mb-3">
                    <label for="nft_reward_name" class="form-label">NFT名 <span class="text-danger">*</span></label>
                    <input type="text" class="form-control @error('nft_reward_name') is-invalid @enderror"
                           id="nft_reward_name" name="nft_reward_name"
                           value="{{ old('nft_reward_name') }}" required>
                    @error('nft_reward_name')
                        <div class="invalid-feedback">{{ $message }}</div>
                    @enderror
                </div>

                <div class="mb-3">
                    <label for="nft_reward_description" class="form-label">NFT説明</label>
                    <textarea class="form-control @error('nft_reward_description') is-invalid @enderror"
                              id="nft_reward_description" name="nft_reward_description"
                              rows="3">{{ old('nft_reward_description') }}</textarea>
                    @error('nft_reward_description')
                        <div class="invalid-feedback">{{ $message }}</div>
                    @enderror
                </div>

                <div class="mb-3">
                    <label for="nft_reward_image_url" class="form-label">NFT画像URL</label>
                    <input type="url" class="form-control @error('nft_reward_image_url') is-invalid @enderror"
                           id="nft_reward_image_url" name="nft_reward_image_url"
                           value="{{ old('nft_reward_image_url') }}">
                    @error('nft_reward_image_url')
                        <div class="invalid-feedback">{{ $message }}</div>
                    @enderror
                </div>

                <div class="d-flex justify-content-end gap-2">
                    <a href="{{ route('admin.escrow-campaigns.index') }}" class="btn btn-secondary">
                        キャンセル
                    </a>
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-save"></i> 作成
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>

<script>
// ページ読み込み時にdrops値を設定
document.addEventListener('DOMContentLoaded', function() {
    const xrpInput = document.getElementById('min_amount_xrp');
    const dropsInput = document.getElementById('min_amount_drops');
    dropsInput.value = Math.floor(xrpInput.value * 1000000);
});
</script>
@endsection
