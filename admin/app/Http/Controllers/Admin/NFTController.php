<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class NFTController extends Controller
{
    public function index(Request $request)
    {
        $query = DB::table('nft_mints')
            ->join('users', 'nft_mints.user_id', '=', 'users.id')
            ->select('nft_mints.*', 'users.name as user_name', 'users.email as user_email');

        if ($request->status) {
            $query->where('nft_mints.status', $request->status);
        }

        $nfts = $query->orderBy('nft_mints.created_at', 'desc')->paginate(20);
        return view('admin.nfts.index', compact('nfts'));
    }

    public function show($id)
    {
        $nft = DB::table('nft_mints')
            ->join('users', 'nft_mints.user_id', '=', 'users.id')
            ->select('nft_mints.*', 'users.name as user_name', 'users.email as user_email')
            ->where('nft_mints.id', $id)
            ->first();

        if (!$nft) abort(404);

        return view('admin.nfts.show', compact('nft'));
    }
}
