/** @type {import('next').NextConfig} */
const nextConfig = {
  // 本番環境ではNext.jsサーバーとして実行
  images: {
    unoptimized: true,
  },
  basePath: "",
  // output: "export", // APIを使用するため静的エクスポートは無効化
};

export default nextConfig;
