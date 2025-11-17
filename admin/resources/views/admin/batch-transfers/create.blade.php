@extends('admin.layouts.app')

@section('title', 'Batch XRP Transfer')

@section('content')
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h3 mb-0">💸 Batch XRP Transfer</h1>
        <a href="{{ route('admin.batch-transfers.index') }}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Back to History
        </a>
    </div>

    @if(session('success'))
        <div class="alert alert-success alert-dismissible fade show">
            {{ session('success') }}
            <button type="button" class="close" data-dismiss="alert">&times;</button>
        </div>
    @endif

    @if(session('error'))
        <div class="alert alert-danger alert-dismissible fade show">
            {{ session('error') }}
            <button type="button" class="close" data-dismiss="alert">&times;</button>
        </div>
    @endif

    <!-- Info Banner -->
    <div class="alert alert-info">
        <h5><i class="fas fa-info-circle"></i> XRPL Batch Transactions</h5>
        <p class="mb-0">
            XRPLのTicket機能を使用して、複数のユーザーに効率的にXRPを送信します。
            通常のトランザクションと同じ手数料（約0.00001 XRP/tx）で並列処理が可能です。
        </p>
    </div>

    <div class="row">
        <!-- Quick Send Options -->
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0"><i class="fas fa-users"></i> 全ユーザーに送信</h5>
                </div>
                <div class="card-body">
                    <form action="{{ route('admin.batch-transfers.send-all') }}" method="POST" onsubmit="return confirm('全ユーザーにXRPを送信しますか？');">
                        @csrf
                        
                        <div class="form-group">
                            <label>送信量（XRP）</label>
                            <input type="number" name="amount_xrp" class="form-control" 
                                   step="0.000001" min="0.000001" required
                                   placeholder="例: 10">
                            <small class="form-text text-muted">各ユーザーに送信するXRP量</small>
                        </div>

                        <div class="form-group">
                            <label>理由</label>
                            <input type="text" name="reason" class="form-control" 
                                   placeholder="例: 月次報酬" required>
                        </div>

                        <div class="form-group">
                            <div class="custom-control custom-checkbox">
                                <input type="checkbox" class="custom-control-input" id="onlyWithWallet" name="only_with_wallet" checked>
                                <label class="custom-control-label" for="onlyWithWallet">
                                    ウォレットを持つユーザーのみ
                                </label>
                            </div>
                        </div>

                        <button type="submit" class="btn btn-primary btn-block">
                            <i class="fas fa-paper-plane"></i> 全ユーザーに送信
                        </button>
                    </form>
                </div>
            </div>
        </div>

        <!-- VIP Users -->
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-header bg-warning text-dark">
                    <h5 class="mb-0"><i class="fas fa-crown"></i> VIPユーザーに送信</h5>
                </div>
                <div class="card-body">
                    <form action="{{ route('admin.batch-transfers.send-to-vip') }}" method="POST" onsubmit="return confirm('VIPユーザーにXRPを送信しますか？');">
                        @csrf
                        
                        <div class="form-group">
                            <label>最小レベル</label>
                            <select name="min_importance_level" class="form-control" required>
                                <option value="Bronze">Bronze 以上</option>
                                <option value="Silver">Silver 以上</option>
                                <option value="Gold" selected>Gold 以上</option>
                                <option value="Platinum">Platinum 以上</option>
                                <option value="Diamond">Diamond のみ</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>送信量（XRP）</label>
                            <input type="number" name="amount_xrp" class="form-control" 
                                   step="0.000001" min="0.000001" required
                                   placeholder="例: 50">
                        </div>

                        <div class="form-group">
                            <label>理由</label>
                            <input type="text" name="reason" class="form-control" 
                                   placeholder="例: VIP月次報酬" required>
                        </div>

                        <button type="submit" class="btn btn-warning btn-block">
                            <i class="fas fa-crown"></i> VIPユーザーに送信
                        </button>
                    </form>
                </div>
            </div>
        </div>

        <!-- Top Referrers -->
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0"><i class="fas fa-trophy"></i> トップ紹介者に送信</h5>
                </div>
                <div class="card-body">
                    <form action="{{ route('admin.batch-transfers.send-to-top-referrers') }}" method="POST" onsubmit="return confirm('トップ紹介者にXRPを送信しますか？');">
                        @csrf
                        
                        <div class="form-group">
                            <label>上位N人</label>
                            <input type="number" name="top_n" class="form-control" 
                                   min="1" max="1000" value="10" required>
                            <small class="form-text text-muted">紹介数が多い上位N人</small>
                        </div>

                        <div class="form-group">
                            <label>送信量（XRP）</label>
                            <input type="number" name="amount_xrp" class="form-control" 
                                   step="0.000001" min="0.000001" required
                                   placeholder="例: 100">
                        </div>

                        <div class="form-group">
                            <label>理由</label>
                            <input type="text" name="reason" class="form-control" 
                                   placeholder="例: トップ紹介者ボーナス" required>
                        </div>

                        <button type="submit" class="btn btn-success btn-block">
                            <i class="fas fa-trophy"></i> トップ紹介者に送信
                        </button>
                    </form>
                </div>
            </div>
        </div>

        <!-- Custom Selection -->
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0"><i class="fas fa-hand-pointer"></i> カスタム選択</h5>
                </div>
                <div class="card-body">
                    <form action="{{ route('admin.batch-transfers.send') }}" method="POST" id="customForm">
                        @csrf
                        
                        <div class="form-group">
                            <label>ユーザーID（カンマ区切り）</label>
                            <textarea name="user_ids_text" class="form-control" rows="3" 
                                      placeholder="例: 1,2,3,4,5"></textarea>
                            <small class="form-text text-muted">または下のユーザー選択を使用</small>
                        </div>

                        <div class="form-group">
                            <label>送信量（XRP）</label>
                            <input type="number" name="amount_xrp" class="form-control" 
                                   step="0.000001" min="0.000001" required
                                   placeholder="例: 25">
                        </div>

                        <div class="form-group">
                            <label>理由</label>
                            <input type="text" name="reason" class="form-control" 
                                   placeholder="例: 特別報酬" required>
                        </div>

                        <button type="button" class="btn btn-secondary btn-block mb-2" onclick="showUserSelector()">
                            <i class="fas fa-search"></i> ユーザーを検索
                        </button>

                        <button type="submit" class="btn btn-info btn-block">
                            <i class="fas fa-paper-plane"></i> 選択したユーザーに送信
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <!-- Sponsor Wallet Status -->
    <div class="card">
        <div class="card-header">
            <h5 class="mb-0"><i class="fas fa-wallet"></i> スポンサーウォレット状態</h5>
        </div>
        <div class="card-body">
            <div id="sponsorStatus">
                <div class="text-center">
                    <div class="spinner-border" role="status">
                        <span class="sr-only">Loading...</span>
                    </div>
                    <p class="mt-2">ウォレット情報を取得中...</p>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- User Selector Modal -->
<div class="modal fade" id="userSelectorModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">ユーザー選択</h5>
                <button type="button" class="close" data-dismiss="modal">&times;</button>
            </div>
            <div class="modal-body">
                <input type="text" id="userSearch" class="form-control mb-3" placeholder="メールアドレスで検索...">
                <div id="userList" style="max-height: 400px; overflow-y: auto;">
                    <!-- ユーザーリストがここに表示される -->
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">キャンセル</button>
                <button type="button" class="btn btn-primary" onclick="applyUserSelection()">選択を適用</button>
            </div>
        </div>
    </div>
</div>

<script>
// スポンサーウォレット状態を取得
fetch('/api/v1/admin/xrpl/sponsor-health', {
    headers: {
        'Authorization': 'Bearer {{ session("admin_token") }}'
    }
})
.then(response => response.json())
.then(data => {
    const statusDiv = document.getElementById('sponsorStatus');
    if (data.healthy) {
        statusDiv.innerHTML = `
            <div class="alert alert-success">
                <h6><i class="fas fa-check-circle"></i> ウォレット正常</h6>
                <p class="mb-0">
                    <strong>残高:</strong> ${data.balance_xrp.toFixed(6)} XRP<br>
                    <strong>アドレス:</strong> <code>${data.sponsor_address}</code><br>
                    <strong>ネットワーク:</strong> ${data.network}
                </p>
            </div>
        `;
    } else {
        statusDiv.innerHTML = `
            <div class="alert alert-danger">
                <h6><i class="fas fa-exclamation-triangle"></i> ウォレット警告</h6>
                <p class="mb-0">
                    ${data.warnings.join('<br>')}
                </p>
            </div>
        `;
    }
})
.catch(error => {
    document.getElementById('sponsorStatus').innerHTML = `
        <div class="alert alert-warning">
            <p class="mb-0">ウォレット情報の取得に失敗しました</p>
        </div>
    `;
});

// ユーザー選択モーダル
let selectedUsers = [];

function showUserSelector() {
    $('#userSelectorModal').modal('show');
    loadUsers();
}

function loadUsers() {
    // ユーザーリストを取得（実装は省略）
    document.getElementById('userList').innerHTML = '<p class="text-muted">ユーザーリストを読み込み中...</p>';
}

function applyUserSelection() {
    const userIds = selectedUsers.join(',');
    document.querySelector('[name="user_ids_text"]').value = userIds;
    $('#userSelectorModal').modal('hide');
}

// カスタムフォーム送信時の処理
document.getElementById('customForm').addEventListener('submit', function(e) {
    const userIdsText = document.querySelector('[name="user_ids_text"]').value;
    if (!userIdsText.trim()) {
        e.preventDefault();
        alert('ユーザーIDを入力してください');
        return false;
    }
    
    // カンマ区切りをJSON配列に変換
    const userIds = userIdsText.split(',').map(id => id.trim()).filter(id => id);
    
    // hidden inputを作成
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'user_ids';
    input.value = JSON.stringify(userIds);
    this.appendChild(input);
    
    return confirm(`${userIds.length}人のユーザーにXRPを送信しますか？`);
});
</script>
@endsection
