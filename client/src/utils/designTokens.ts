// Design tokens extracted from theme.css for use in docx generation
export const designTokens = {
  fontSize: {
    base: 18, // 9pt (current body size)
    heading1: 26, // 13pt
    heading2: 22, // 11pt
    heading3: 18, // 9pt
    tableHeader: 14, // 7pt
    tableCell: 14, // 7pt
    subhead: 18, // 9pt (same as heading3)
  },
  colors: {
    // Table Colors
    tableHeaderBg: "#000000", // Black
    tableHeaderFg: "#FFFFFF", // White
    tableRow: "#FFFFFF", // Even rows
    tableRowAlt: "#F9FAFB", // Odd rows (light gray)
    tableBorder: "#D1D5DB", // Border gray
    tableCellText: "#000000", // Table body text (black for Engagement Index)

    // Numbered List (Orange Circles)
    orangeGradientStart: "#FB923C",
    orangeGradientEnd: "#F59E0B",
    numberTextWhite: "#FFFFFF",

    // Checklist Icons
    checkMarkGreen: "#22C55E",
    xMarkRed: "#EF4444",

    // Bullet Points
    bulletGray: "#000000", // Black bullets

    // Brand Archetype Cards - Primary
    primaryGradientStart: "#EFF6FF",
    primaryGradientEnd: "#EEF2FF",
    primaryBorder: "#93C5FD",
    primaryLabelBg: "#2563EB",
    primaryLabelText: "#FFFFFF",

    // Brand Archetype Cards - Secondary
    secondaryGradientStart: "#FAF5FF",
    secondaryGradientEnd: "#FDF2F8",
    secondaryBorder: "#D8B4FE",
    secondaryLabelBg: "#9333EA",
    secondaryLabelText: "#FFFFFF",

    // Callout Boxes
    infoBg: "#EFF6FF",
    infoBorder: "#BFDBFE",
    infoText: "#1E3A8A",
    warningBg: "#FFFBEB",
    warningBorder: "#FDE68A",
    warningText: "#78350F",
    successBg: "#F0FDF4",
    successBorder: "#BBF7D0",
    successText: "#14532D",

    // Opportunity Cards
    opportunityCardBg: "#FFFFFF",
    opportunityCardBorder: "#E5E7EB",
    opportunityCardTitle: "#111827",
    opportunityCardBody: "#374151",

    // Body Text & Backgrounds
    primaryText: "#1F2937",
    headingText: "#111827",
    pageBg: "#F9FAFB",
    contentSectionBg: "#FFFFFF",

    // Legacy/compatibility (keep for now)
    primary: "#030213",
    secondary: "#ececf0",
    muted: "#ececf0",
    accent: "#e9ebef",
    card: "#ffffff",
    border: "#e6e6e6",
    destructive: "#d4183d",
    background: "#ffffff",
    foreground: "#232323",
    heading1: "#212121",
    heading2: "#424242",
    heading3: "#616161",
    subhead: "#616161",
  },
  fontWeight: {
    normal: 400,
    medium: 500,
    bold: 700,
  },
  radius: 10, // px
  spacing: {
    paragraphAfter: 160,
    heading1Before: 320,
    heading1After: 240,
    heading2Before: 240,
    heading2After: 160,
    heading3Before: 160,
    heading3After: 80,
    tableCellPadding: 8, // px
    bulletAfter: 80,
    subheadBefore: 160,
    subheadAfter: 80,
    sectionTitleAfter: 80,
  },
};
