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
    primary: "#030213",
    secondary: "#ececf0",
    muted: "#ececf0",
    accent: "#e9ebef",
    card: "#ffffff",
    border: "#e6e6e6", // replaced rgba(0,0,0,0.1) with a light gray hex for docx compatibility
    destructive: "#d4183d",
    background: "#ffffff",
    foreground: "#232323",
    heading1: "#212121",
    heading2: "#424242",
    heading3: "#616161",
    tableHeaderBg: "#000000",
    tableHeaderFg: "#FFFFFF",
    tableRowAlt: "#f9fafb",
    tableRow: "#ffffff",
    subhead: "#616161", // same as heading3
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
