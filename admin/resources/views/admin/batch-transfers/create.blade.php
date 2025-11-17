@extends('admin.layouts.app')

@section('title', 'New Batch Transfer')

@section('content')
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h3 mb-0">New Batch Transfer</h1>
        <a href="{{ route('admin.batch-transfers.index') }}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Back to History
        </a>
    </div>

    <div class="row">
        <!-- Manual Selection -->
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Manual User Selection</h5>
                </div>
                <div class="card-body">
                    <form id="manualTransferForm" action="{{ route('admin.batch-transfers.send') }}" method="POST">
                        @csrf
                        
                        <div class="form-group">
                            <label>Select Users</label>
                            <select name="user_ids[]" id="userSelect" class="form-control" multiple size="10">
                                @foreach($users as $user)
                                    <option value="{{ $user->id }}">
                                        {{ $user->email }} 
                                        @if($user->importance_level)
                                            ({{ $user->importance_level }})
                                        @endif
                                    </option>
                                @endforeach
                            </select>
                            <small class="form-text text-muted">Hold Ctrl/Cmd to select multiple users</small>
                        </div>

                        <div class="form-group">
                            <label>Amount per User (XRP)</label>
                            <input type="number" name="amount_xrp" id="manualAmount" class="form-control" 
                                   step="0.000001" min="0.000001" required>
                        </div>

                        <div class="form-group">
                            <label>Reason</label>
                            <input type="text" name="reason" class="form-control" 
                                   placeholder="e.g., Monthly reward" required>
                        </div>

                        <button type="button" class="btn btn-info" onclick="previewManualTransfer()">
                            <i class="fas fa-eye"></i> Preview
                        </button>
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-paper-plane"></i> Send
                        </button>
                    </form>
                </div>
            </div>
        </div>

        <!-- VIP Users -->
        <div class="col-md-6">
            <div class="card mb-3">
                <div class="card-header">
                    <h5 class="mb-0">Send to VIP Users</h5>
                </div>
                <div class="card-body">
                    <form action="{{ route('admin.batch-transfers.send-to-vip') }}" method="POST">
                        @csrf
                        
                        <div class="form-group">
                            <label>Minimum Level</label>
                            <select name="min_importance_level" class="form-control" required>
                                <option value="Bronze">Bronze and above</option>
                                <option value="Silver">Silver and above</option>
                                <option value="Gold">Gold and above</option>
                                <option value="Platinum">Platinum and above</option>
                                <option value="Diamond">Diamond only</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Amount per User (XRP)</label>
                            <input type="number" name="amount_xrp" class="form-control" 
                                   step="0.000001" min="0.000001" required>
                        </div>

                        <div class="form-group">
                            <label>Reason</label>
                            <input type="text" name="reason" class="form-control" 
                                   placeholder="e.g., VIP monthly reward" required>
                        </div>

                        <button type="submit" class="btn btn-primary btn-block">
                            <i class="fas fa-crown"></i> Send to VIP Users
                        </button>
                    </form>
                </div>
            </div>

            <!-- Top Referrers -->
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Send to Top Referrers</h5>
                </div>
                <div class="card-body">
                    <form action="{{ route('admin.batch-transfers.send-to-top-referrers') }}" method="POST">
                        @csrf
                        
                        <div class="form-group">
                            <label>Top N Users</label>
                            <input type="number" name="top_n" class="form-control" 
                                   min="1" max="1000" value="10" required>
                        </div>

                        <div class="form-group">
                            <label>Amount per User (XRP)</label>
                            <input type="number" name="amount_xrp" class="form-control" 
                                   step="0.000001" min="0.000001" required>
                        </div>

                        <div class="form-group">
                            <label>Reason</label>
                            <input type="text" name="reason" class="form-control" 
                                   placeholder="e.g., Top referrer reward" required>
                        </div>

                        <button type="submit" class="btn btn-primary btn-block">
                            <i class="fas fa-trophy"></i> Send to Top Referrers
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <!-- Preview Modal -->
    <div class="modal fade" id="previewModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Batch Transfer Preview</h5>
                    <button type="button" class="close" data-dismiss="modal">&times;</button>
                </div>
                <div class="modal-body" id="previewContent">
                    <!-- Preview content will be loaded here -->
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-primary" onclick="submitManualTransfer()">
                        Confirm and Send
                    </button>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
function previewManualTransfer() {
    const userIds = Array.from(document.getElementById('userSelect').selectedOptions).map(opt => opt.value);
    const amountXrp = document.getElementById('manualAmount').value;
    
    if (userIds.length === 0) {
        alert('Please select at least one user');
        return;
    }
    
    if (!amountXrp || amountXrp <= 0) {
        alert('Please enter a valid amount');
        return;
    }
    
    fetch('{{ route("admin.batch-transfers.preview") }}', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': '{{ csrf_token() }}'
        },
        body: JSON.stringify({
            user_ids: userIds,
            amount_xrp: parseFloat(amountXrp)
        })
    })
    .then(response => response.json())
    .then(data => {
        let html = `
            <div class="alert alert-info">
                <h5>Summary</h5>
                <ul class="mb-0">
                    <li>Total Users: ${data.total_users}</li>
                    <li>Valid Users (with wallet): ${data.valid_users}</li>
                    <li>Invalid Users (no wallet): ${data.invalid_users}</li>
                    <li>Amount per User: ${data.amount_per_user_xrp} XRP</li>
                    <li><strong>Total Amount: ${data.total_amount_xrp} XRP</strong></li>
                </ul>
            </div>
        `;
        
        if (data.users.length > 0) {
            html += '<h6>Recipients:</h6><ul>';
            data.users.forEach(user => {
                html += `<li>${user.email} (${user.importance_level || 'N/A'})</li>`;
            });
            html += '</ul>';
        }
        
        if (data.users_without_wallet.length > 0) {
            html += '<div class="alert alert-warning"><h6>Users without wallet (will be skipped):</h6><ul>';
            data.users_without_wallet.forEach(user => {
                html += `<li>${user.email}</li>`;
            });
            html += '</ul></div>';
        }
        
        document.getElementById('previewContent').innerHTML = html;
        $('#previewModal').modal('show');
    })
    .catch(error => {
        alert('Preview failed: ' + error.message);
    });
}

function submitManualTransfer() {
    document.getElementById('manualTransferForm').submit();
}
</script>
@endsection
