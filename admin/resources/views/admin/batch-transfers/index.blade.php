@extends('admin.layouts.app')

@section('title', 'Batch Transfers')

@section('content')
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h3 mb-0">Batch Transfer History</h1>
        <div>
            <a href="{{ route('admin.batch-transfers.stats') }}" class="btn btn-info">
                <i class="fas fa-chart-bar"></i> Statistics
            </a>
            <a href="{{ route('admin.batch-transfers.create') }}" class="btn btn-primary">
                <i class="fas fa-paper-plane"></i> New Batch Transfer
            </a>
        </div>
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

    <div class="card">
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>User</th>
                            <th>Wallet Address</th>
                            <th>Amount (XRP)</th>
                            <th>Transaction Hash</th>
                            <th>Ticket Seq</th>
                            <th>Reason</th>
                            <th>Status</th>
                            <th>Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        @forelse($transfers as $transfer)
                            <tr>
                                <td>{{ $transfer['id'] }}</td>
                                <td>
                                    <div>{{ $transfer['email'] }}</div>
                                    @if(isset($transfer['importance_level']))
                                        <span class="badge badge-{{ $transfer['importance_level'] == 'Diamond' ? 'primary' : ($transfer['importance_level'] == 'Platinum' ? 'info' : ($transfer['importance_level'] == 'Gold' ? 'warning' : 'secondary')) }}">
                                            {{ $transfer['importance_level'] }}
                                        </span>
                                    @endif
                                </td>
                                <td>
                                    <small class="text-monospace">{{ substr($transfer['wallet_address'], 0, 10) }}...</small>
                                </td>
                                <td>
                                    <strong>{{ number_format($transfer['amount_xrp'], 6) }}</strong> XRP
                                </td>
                                <td>
                                    <a href="https://testnet.xrpl.org/transactions/{{ $transfer['transaction_hash'] }}" 
                                       target="_blank" 
                                       class="text-monospace small">
                                        {{ substr($transfer['transaction_hash'], 0, 10) }}...
                                        <i class="fas fa-external-link-alt"></i>
                                    </a>
                                </td>
                                <td>{{ $transfer['ticket_sequence'] ?? '-' }}</td>
                                <td>
                                    <small>{{ $transfer['reason'] }}</small>
                                </td>
                                <td>
                                    @if($transfer['status'] == 'success')
                                        <span class="badge badge-success">Success</span>
                                    @else
                                        <span class="badge badge-danger">Failed</span>
                                    @endif
                                </td>
                                <td>
                                    <small>{{ date('Y-m-d H:i', strtotime($transfer['created_at'])) }}</small>
                                </td>
                            </tr>
                        @empty
                            <tr>
                                <td colspan="9" class="text-center text-muted py-4">
                                    No batch transfers found
                                </td>
                            </tr>
                        @endforelse
                    </tbody>
                </table>
            </div>

            @if($total > $limit)
                <div class="d-flex justify-content-between align-items-center mt-3">
                    <div>
                        Showing {{ $offset + 1 }} to {{ min($offset + $limit, $total) }} of {{ $total }} transfers
                    </div>
                    <nav>
                        <ul class="pagination mb-0">
                            @if($offset > 0)
                                <li class="page-item">
                                    <a class="page-link" href="?offset={{ max(0, $offset - $limit) }}&limit={{ $limit }}">Previous</a>
                                </li>
                            @endif
                            @if($offset + $limit < $total)
                                <li class="page-item">
                                    <a class="page-link" href="?offset={{ $offset + $limit }}&limit={{ $limit }}">Next</a>
                                </li>
                            @endif
                        </ul>
                    </nav>
                </div>
            @endif
        </div>
    </div>
</div>
@endsection
