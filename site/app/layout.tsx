import type { Metadata } from 'next';
import './globals.css';
import { Footer } from '@ds/Footer';
import { site, navLinks, socialLinks } from '@/content/site';
import { SiteNav } from './SiteNav';

export const metadata: Metadata = {
  title: {
    default: `${site.brand} – ${site.tagline}`,
    template: `%s – ${site.brand}`,
  },
  description: site.tagline,
  metadataBase: new URL(site.url),
  // robots.txt asks crawlers not to fetch these pages; this emits the noindex
  // meta tag that also keeps them out of the index if a URL is discovered some
  // other way (a shared link, a backlink), which robots.txt alone does not do.
  robots: { index: false, follow: false, nocache: true },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="flex min-h-screen flex-col">
        <a href="#main" className="skip-link rounded-md bg-action-primary px-4 py-2 text-action-on-primary">
          Skip to content
        </a>

        <SiteNav />

        <main id="main" className="flex-1">
          {children}
        </main>

        <Footer
          brand={site.brand}
          tagline={site.tagline}
          email={site.email}
          links={navLinks}
          social={socialLinks}
        />
      </body>
    </html>
  );
}
