/** @type {import('next').NextConfig} */
const nextConfig = {
  // 本番環境ではNext.jsサーバーとして実行
  images: {
    unoptimized: true,
  },
  basePath: "",
  // output: "export", // APIを使用するため静的エクスポートは無効化
  
  // APIリクエストをバックエンドにプロキシ
  async rewrites() {
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';
    return [
      {
        source: '/api/:path*',
        destination: `${backendUrl}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;
