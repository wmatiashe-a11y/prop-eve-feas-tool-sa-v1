import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Prop Dev Feas Tool SA",
  description: "Property development feasibility tool",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
