<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;

class ProductController extends Controller
{
    public function index()
    {
        $products = DB::table('products')->orderBy('created_at', 'desc')->paginate(20);
        return view('admin.products.index', compact('products'));
    }

    public function create()
    {
        return view('admin.products.create');
    }

    public function store(Request $request)
    {
        $validated = $request->validate([
            'name' => 'required|max:255',
            'description' => 'nullable',
            'price' => 'required|integer|min:0',
            'stock_quantity' => 'required|integer|min:0',
            'image_url' => 'nullable|url',
            'is_active' => 'boolean',
        ]);

        $validated['id'] = Str::uuid();
        $validated['created_at'] = now();
        $validated['updated_at'] = now();
        $validated['is_active'] = $request->has('is_active');

        DB::table('products')->insert($validated);
        return redirect()->route('products.index')->with('success', '商品を作成しました');
    }

    public function edit($id)
    {
        $product = DB::table('products')->where('id', $id)->first();
        if (!$product) abort(404);
        return view('admin.products.edit', compact('product'));
    }

    public function update(Request $request, $id)
    {
        $validated = $request->validate([
            'name' => 'required|max:255',
            'description' => 'nullable',
            'price' => 'required|integer|min:0',
            'stock_quantity' => 'required|integer|min:0',
            'image_url' => 'nullable|url',
            'is_active' => 'boolean',
        ]);

        $validated['updated_at'] = now();
        $validated['is_active'] = $request->has('is_active');

        DB::table('products')->where('id', $id)->update($validated);
        return redirect()->route('products.index')->with('success', '商品を更新しました');
    }

    public function destroy($id)
    {
        DB::table('products')->where('id', $id)->delete();
        return redirect()->route('products.index')->with('success', '商品を削除しました');
    }
}
