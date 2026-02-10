/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: "standalone",

  transpilePackages: [
    "@fullcalendar/common",
    "@fullcalendar/daygrid",
    "@fullcalendar/react",
    "@fullcalendar/core",
  ],

  // Enable the fast SWC compiler for Emotion (replaces Babel)
  compiler: {
    emotion: true,
  },

  // Expose emulator flag to client side for Firebase configuration
  // This is set to 'true' in development (docker-compose) and 'false' in production
  env: {
    NEXT_PUBLIC_USE_FIREBASE_EMULATOR: process.env.NODE_ENV === "development" ? "true" : "false",
  },

  images: {
    remotePatterns: [
      {
        protocol: "http",
        hostname: "localhost",
      },
      {
        protocol: "http",
        hostname: "127.0.0.1",
      },
      {
        protocol: "https",
        hostname: "firebasestorage.googleapis.com", // For production Firebase
      },
    ],
  },

  typescript: {
    ignoreBuildErrors: true,
  },

};

module.exports = nextConfig;