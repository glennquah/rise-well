import { ClerkProvider, SignIn, SignedIn, SignedOut } from '@clerk/nextjs';
import type { Metadata } from 'next';
import { Geist, Geist_Mono } from 'next/font/google';
import { Toaster } from 'sonner';
import './globals.css';
import Footer from './layout/Footer';
import NavigationBar from './layout/NavigationBar';

const geistSans = Geist({
  variable: '--font-geist-sans',
  subsets: ['latin'],
});

const geistMono = Geist_Mono({
  variable: '--font-geist-mono',
  subsets: ['latin'],
});

export const metadata: Metadata = {
  title: 'RiseWell',
  description: 'Your personalized IoT alarm clock',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ClerkProvider
      appearance={{
        variables: {
          colorPrimary: 'blue',
          colorText: 'black',
        },
      }}
    >
      <html lang="en">
        <body
          className={`${geistSans.variable} ${geistMono.variable} antialiased`}
        >
          <main>
            <SignedOut>
              <div className="flex items-center justify-center min-h-screen">
                <SignIn routing="hash" />
              </div>
            </SignedOut>
            <SignedIn>
              {' '}
              <NavigationBar />
              <div className="pt-8">{children}</div>
              <Toaster />
              <Footer />
            </SignedIn>
          </main>
        </body>
      </html>
    </ClerkProvider>
  );
}
