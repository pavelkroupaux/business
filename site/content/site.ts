/**
 * All site copy lives here, separated from layout.
 *
 * ─────────────────────────────────────────────────────────────────────────────
 * PROVENANCE — read before trusting any string in this file.
 *
 * The live site could not be reached from the build environment, so the real
 * copy could not be preserved as Phase 3 intended. Every string is tagged:
 *
 *   [SEARCH]      Recovered from public search-engine metadata for
 *                 pavelkroupa.com. Real, but second-hand — worth verifying
 *                 against the live page, and possibly truncated.
 *   [PLACEHOLDER] Written to give the layout something to render. NOT Pavel's
 *                 copy. Must be replaced.
 *
 * Nothing here is a paraphrase of real copy presented as if it were real copy.
 * Where the wording was unknown it is obviously provisional, so it can never be
 * mistaken for the original.
 * ─────────────────────────────────────────────────────────────────────────────
 */

export const site = {
  /** [SEARCH] Page title used across the live site. */
  brand: 'Pavel Kroupa',
  /** [SEARCH] From the live <title>: "Pavel Kroupa – Design Leadership & Innovation". */
  tagline: 'Design Leadership & Innovation',
  /** [SEARCH] Listed as the contact address. */
  email: 'design@pavelkroupa.com',
  /** [SEARCH] Listed location. */
  location: 'Mezno, Czechia',
  url: 'https://www.pavelkroupa.com',
};

/** [SEARCH] Routes confirmed to exist on the live site. */
export const navLinks = [
  { label: 'Work', href: '/portfolio' },
  { label: 'About', href: '/about' },
  { label: 'Contact', href: '/contact' },
];

export const navCta = { label: 'Get in touch', href: '/contact' };

export const socialLinks = [
  { label: 'LinkedIn', href: 'https://www.linkedin.com/in/pavelkroupa/' },
];

export const home = {
  /** [PLACEHOLDER] */
  eyebrow: 'Product design & leadership',
  /** [SEARCH] Derived from the site title — likely close, verify wording. */
  headline: 'Design leadership and innovation',
  /** [PLACEHOLDER] Built from themes in search metadata, not the real intro. */
  intro:
    'Digital product manager and designer working at the intersection of technology, psychology and anthropology — leading teams to ship user-centred products.',
  work: {
    /** [PLACEHOLDER] */
    eyebrow: 'Selected work',
    title: 'Projects',
    description:
      'A few things worth showing. Replace this section once the real project list is available.',
  },
  /** [PLACEHOLDER] */
  cta: {
    title: 'Looking for a design partner?',
    description: 'Tell me about the problem you are working on.',
    action: 'Start a conversation',
  },
};

export interface Project {
  slug: string;
  title: string;
  summary: string;
  meta: string[];
  featured?: boolean;
  /** Body paragraphs for the case-study page. */
  body: string[];
}

export const projects: Project[] = [
  {
    /** [SEARCH] This case study exists at /portfolio/coinmate. */
    slug: 'coinmate',
    /** [SEARCH] From the live page title. */
    title: 'Designing a Simple Cryptocurrency Exchange',
    /** [SEARCH] Close to the published description — verify against the page. */
    summary:
      'How even a cryptocurrency exchange can be made simple and approachable, by prioritising clarity and empowering users.',
    /** [PLACEHOLDER] */
    meta: ['Product design', 'Fintech'],
    featured: true,
    /** [PLACEHOLDER] Structure only — the real case-study body was not readable. */
    body: [
      'Placeholder body copy. The real case study could not be read from the live site, so this text exists only to exercise the Prose component and show how a case study lays out.',
      'Replace with the original narrative — context, the problem, the approach taken, and what shipped.',
    ],
  },
  {
    /** [PLACEHOLDER] Entire project — a second card to show grid behaviour. */
    slug: 'placeholder-project',
    title: 'Second project placeholder',
    summary:
      'Not a real project. Present so the work grid can be reviewed with more than one card in it.',
    meta: ['Placeholder'],
    body: [
      'Delete this project once the real portfolio list is available.',
    ],
  },
];

export const about = {
  /** [PLACEHOLDER] */
  eyebrow: 'About',
  /** [PLACEHOLDER] */
  headline: 'Designing with people, not just for them',
  /** [PLACEHOLDER] */
  intro:
    'Placeholder introduction. Replace with the real About copy from the live site.',
  /** [SEARCH] These specifics appeared in public metadata — verify each one. */
  body: [
    'Experienced digital product manager and designer, working on user-centric strategic design and product development, and leading teams to deliver projects end to end.',
    'Mentored aspiring UX designers at Femme Palette, taught Design Thinking to students at CVUT, and spoken at events including the Czech Online Expo.',
    '[PLACEHOLDER] Remaining biography to be filled in from the live About page.',
  ],
};

export const contact = {
  /** [PLACEHOLDER] */
  eyebrow: 'Contact',
  headline: 'Let’s talk',
  intro:
    'Placeholder contact copy. Replace with the real wording from the live contact page.',
};
