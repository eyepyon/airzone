<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class OrderController extends Controller
{
    public function index(Request $request)
    {
        $query = DB::table('orders')
            ->join('users', 'orders.user_id', '=', 'users.id')
            ->select('orders.*', 'users.name as user_name', 'users.email as user_email');

        if ($request->status) {
            $query->where('orders.status', $request->status);
        }

        $orders = $query->orderBy('orders.created_at', 'desc')->paginate(20);
        return view('admin.orders.index', compact('orders'));
    }

    public function show($id)
    {
        $order = DB::table('orders')
            ->join('users', 'orders.user_id', '=', 'users.id')
            ->select('orders.*', 'users.name as user_name', 'users.email as user_email')
            ->where('orders.id', $id)
            ->first();

        if (!$order) abort(404);

        $items = DB::table('order_items')
            ->join('products', 'order_items.product_id', '=', 'products.id')
            ->select('order_items.*', 'products.name as product_name')
            ->where('order_items.order_id', $id)
            ->get();

        $payment = DB::table('payments')->where('order_id', $id)->first();

        return view('admin.orders.show', compact('order', 'items', 'payment'));
    }

    public function update(Request $request, $id)
    {
        $validated = $request->validate([
            'status' => 'required|in:pending,processing,completed,failed,cancelled',
        ]);

        $validated['updated_at'] = now();
        DB::table('orders')->where('id', $id)->update($validated);

        return redirect()->back()->with('success', '注文ステータスを更新しました');
    }
}
