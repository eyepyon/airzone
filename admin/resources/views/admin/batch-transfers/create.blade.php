@extends('admin.layout')

@section('title', '一括XRP送金')

@section('content')
<div class="mb-6">
    <div class="flex justify-between items-center">
        <h1 class="text-3xl font-bold text-gray-900">💸 一括XRP送金</h1>
        <a href="{{ route('admin.batch-transfers.index') }}" class="inline-flex items-center px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors">
            <i class="fas fa-arrow-left mr-2"></i> 履歴に戻る
        </a>
    </div>
</div>

<!-- Info Banner -->
<div class="bg-blue-50 border-l-4 border-blue-500 p-4 mb-6">
    <div class="flex">
        <div class="flex-shrink-0">
            <i class="fas fa-info-circle text-blue-500 text-xl"></i>
        </div>
        <div class="ml-3">
            <h3 class="text-lg font-medium text-blue-900">XRPL一括トランザクション</h3>
            <p class="text-sm text-blue-700 mt-1">
                XRPLのTicket機能を使用して、複数のユーザーに効率的にXRPを送信します。
                通常のトランザクションと同じ手数料（約0.00001 XRP/tx）で並列処理が可能です。
            </p>
        </div>
    </div>
</div>

<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
    <!-- Quick Send Options -->
    <div class="bg-white rounded-lg shadow-md overflow-hidden">
        <div class="bg-blue-600 text-white px-6 py-4">
            <h2 class="text-xl font-bold"><i class="fas fa-users mr-2"></i>全ユーザーに送信</h2>
        </div>
        <div class="p-6">
            <form action="{{ route('admin.batch-transfers.send-all') }}" method="POST" onsubmit="return confirm('全ユーザーにXRPを送信しますか？');">
                @csrf
                
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">送信量（XRP）</label>
                    <input type="number" name="amount_xrp" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
                           step="0.000001" min="0.000001" required
                           placeholder="例: 10">
                    <p class="text-sm text-gray-500 mt-1">各ユーザーに送信するXRP量</p>
                </div>

                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">理由</label>
                    <input type="text" name="reason" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
                           placeholder="例: 月次報酬" required>
                </div>

                <div class="mb-6">
                    <label class="flex items-center">
                        <input type="checkbox" id="onlyWithWallet" name="only_with_wallet" checked class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500">
                        <span class="ml-2 text-sm text-gray-700">ウォレットを持つユーザーのみ</span>
                    </label>
                </div>

                <button type="submit" class="w-full bg-blue-600 text-white px-4 py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium">
                    <i class="fas fa-paper-plane mr-2"></i>全ユーザーに送信
                </button>
            </form>
        </div>
    </div>

    <!-- VIP Users -->
    <div class="bg-white rounded-lg shadow-md overflow-hidden">
        <div class="bg-yellow-500 text-gray-900 px-6 py-4">
            <h2 class="text-xl font-bold"><i class="fas fa-crown mr-2"></i>VIPユーザーに送信</h2>
        </div>
        <div class="p-6">
            <form action="{{ route('admin.batch-transfers.send-to-vip') }}" method="POST" onsubmit="return confirm('VIPユーザーにXRPを送信しますか？');">
                @csrf
                
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">最小レベル</label>
                    <select name="min_importance_level" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent" required>
                        <option value="Bronze">Bronze 以上</option>
                        <option value="Silver">Silver 以上</option>
                        <option value="Gold" selected>Gold 以上</option>
                        <option value="Platinum">Platinum 以上</option>
                        <option value="Diamond">Diamond のみ</option>
                    </select>
                </div>

                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">送信量（XRP）</label>
                    <input type="number" name="amount_xrp" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent" 
                           step="0.000001" min="0.000001" required
                           placeholder="例: 50">
                </div>

                <div class="mb-6">
                    <label class="block text-sm font-medium text-gray-700 mb-2">理由</label>
                    <input type="text" name="reason" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent" 
                           placeholder="例: VIP月次報酬" required>
                </div>

                <button type="submit" class="w-full bg-yellow-500 text-gray-900 px-4 py-3 rounded-lg hover:bg-yellow-600 transition-colors font-medium">
                    <i class="fas fa-crown mr-2"></i>VIPユーザーに送信
                </button>
            </form>
        </div>
    </div>

    <!-- Top Referrers -->
    <div class="bg-white rounded-lg shadow-md overflow-hidden">
        <div class="bg-green-600 text-white px-6 py-4">
            <h2 class="text-xl font-bold"><i class="fas fa-trophy mr-2"></i>トップ紹介者に送信</h2>
        </div>
        <div class="p-6">
            <form action="{{ route('admin.batch-transfers.send-to-top-referrers') }}" method="POST" onsubmit="return confirm('トップ紹介者にXRPを送信しますか？');">
                @csrf
                
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">上位N人</label>
                    <input type="number" name="top_n" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent" 
                           min="1" max="1000" value="10" required>
                    <p class="text-sm text-gray-500 mt-1">紹介数が多い上位N人</p>
                </div>

                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">送信量（XRP）</label>
                    <input type="number" name="amount_xrp" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent" 
                           step="0.000001" min="0.000001" required
                           placeholder="例: 100">
                </div>

                <div class="mb-6">
                    <label class="block text-sm font-medium text-gray-700 mb-2">理由</label>
                    <input type="text" name="reason" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent" 
                           placeholder="例: トップ紹介者ボーナス" required>
                </div>

                <button type="submit" class="w-full bg-green-600 text-white px-4 py-3 rounded-lg hover:bg-green-700 transition-colors font-medium">
                    <i class="fas fa-trophy mr-2"></i>トップ紹介者に送信
                </button>
            </form>
        </div>
    </div>

    <!-- Custom Selection -->
    <div class="bg-white rounded-lg shadow-md overflow-hidden">
        <div class="bg-cyan-600 text-white px-6 py-4">
            <h2 class="text-xl font-bold"><i class="fas fa-hand-pointer mr-2"></i>カスタム選択</h2>
        </div>
        <div class="p-6">
            <form action="{{ route('admin.batch-transfers.send') }}" method="POST" id="customForm">
                @csrf
                
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">ユーザーID（カンマ区切り）</label>
                    <textarea name="user_ids_text" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent" rows="3" 
                              placeholder="例: 1,2,3,4,5"></textarea>
                    <p class="text-sm text-gray-500 mt-1">または下のユーザー選択を使用</p>
                </div>

                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">送信量（XRP）</label>
                    <input type="number" name="amount_xrp" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent" 
                           step="0.000001" min="0.000001" required
                           placeholder="例: 25">
                </div>

                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">理由</label>
                    <input type="text" name="reason" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent" 
                           placeholder="例: 特別報酬" required>
                </div>

                <button type="button" class="w-full bg-gray-600 text-white px-4 py-3 rounded-lg hover:bg-gray-700 transition-colors font-medium mb-3" onclick="showUserSelector()">
                    <i class="fas fa-search mr-2"></i>ユーザーを検索
                </button>

                <button type="submit" class="w-full bg-cyan-600 text-white px-4 py-3 rounded-lg hover:bg-cyan-700 transition-colors font-medium">
                    <i class="fas fa-paper-plane mr-2"></i>選択したユーザーに送信
            </form>
        </div>
    </div>
</div>

<!-- Sponsor Wallet Status -->
<div class="bg-white rounded-lg shadow-md overflow-hidden mt-6">
    <div class="bg-gray-800 text-white px-6 py-4">
        <h2 class="text-xl font-bold"><i class="fas fa-wallet mr-2"></i>スポンサーウォレット状態</h2>
    </div>
    <div class="p-6">
        <div id="sponsorStatus">
            <div class="text-center py-8">
                <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                <p class="mt-4 text-gray-600">ウォレット情報を取得中...</p>
            </div>
        </div>
    </div>
</div>

<!-- User Selector Modal -->
<div id="userSelectorModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 hidden overflow-y-auto h-full w-full z-50">
    <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-lg bg-white">
        <div class="flex justify-between items-center pb-3 border-b">
            <h3 class="text-xl font-bold text-gray-900">ユーザー選択</h3>
            <button type="button" class="text-gray-400 hover:text-gray-600" onclick="closeUserSelector()">
                <i class="fas fa-times text-2xl"></i>
            </button>
        </div>
        <div class="mt-4">
            <input type="text" id="userSearch" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent mb-4" placeholder="メールアドレスで検索...">
            <div id="userList" class="max-h-96 overflow-y-auto border border-gray-200 rounded-lg p-4">
                <!-- ユーザーリストがここに表示される -->
            </div>
        </div>
        <div class="flex justify-end space-x-3 mt-4 pt-3 border-t">
            <button type="button" class="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors" onclick="closeUserSelector()">キャンセル</button>
            <button type="button" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors" onclick="applyUserSelection()">選択を適用</button>
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
            <div class="bg-green-50 border-l-4 border-green-500 p-4">
                <div class="flex">
                    <div class="flex-shrink-0">
                        <i class="fas fa-check-circle text-green-500 text-xl"></i>
                    </div>
                    <div class="ml-3">
                        <h3 class="text-lg font-medium text-green-900">ウォレット正常</h3>
                        <div class="mt-2 text-sm text-green-700">
                            <p><strong>残高:</strong> ${data.balance_xrp.toFixed(6)} XRP</p>
                            <p><strong>アドレス:</strong> <code class="bg-green-100 px-2 py-1 rounded">${data.sponsor_address}</code></p>
                            <p><strong>ネットワーク:</strong> ${data.network}</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
    } else {
        statusDiv.innerHTML = `
            <div class="bg-red-50 border-l-4 border-red-500 p-4">
                <div class="flex">
                    <div class="flex-shrink-0">
                        <i class="fas fa-exclamation-triangle text-red-500 text-xl"></i>
                    </div>
                    <div class="ml-3">
                        <h3 class="text-lg font-medium text-red-900">ウォレット警告</h3>
                        <div class="mt-2 text-sm text-red-700">
                            ${data.warnings.map(w => `<p>• ${w}</p>`).join('')}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
})
.catch(error => {
    document.getElementById('sponsorStatus').innerHTML = `
        <div class="bg-yellow-50 border-l-4 border-yellow-500 p-4">
            <p class="text-yellow-700">ウォレット情報の取得に失敗しました</p>
        </div>
    `;
});

// ユーザー選択モーダル
let selectedUsers = [];

function showUserSelector() {
    document.getElementById('userSelectorModal').classList.remove('hidden');
    loadUsers();
}

function closeUserSelector() {
    document.getElementById('userSelectorModal').classList.add('hidden');
}

function loadUsers() {
    // ユーザーリストを取得（実装は省略）
    document.getElementById('userList').innerHTML = '<p class="text-gray-500">ユーザーリストを読み込み中...</p>';
}

function applyUserSelection() {
    const userIds = selectedUsers.join(',');
    document.querySelector('[name="user_ids_text"]').value = userIds;
    closeUserSelector();
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
