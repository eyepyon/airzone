/** @type {import('next').NextConfig} */
const nextConfig = {
  // 本番環境ではNext.jsサーバーとして実行
  images: {
    unoptimized: true,
  },
  basePath: "",
  output: "export",
};

export default nextConfig;
