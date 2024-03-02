import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import '@radix-ui/themes/styles.css';
import type { Viewport } from "next";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Plaid Family Lights",
  description: "Web controller for the Plaid Family Lights",
};

export const viewport: Viewport = {
  minimumScale: 1.0,
  maximumScale: 1.0,
  userScalable: false,
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="bg-gray-600 w-full h-full">
        {children}
      </body>
    </html>
  );
}
