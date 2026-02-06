import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Autonomous Incident Analyst',
  description: 'AI-powered incident analysis and resolution',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
