// TypeScript interfaces matching the Python data structure

export interface MarketingKitData {
  clientName: string;
  sections: Section[];
}

export interface Section {
  title: string;
  subsections?: Subsection[];
  blocks?: Block[];
}

export interface Subsection {
  title: string;
  blocks: Block[];
}

export type Block =
  | ParagraphBlock
  | BulletsBlock
  | TableBlock
  | PersonaBlock
  | CalloutBlock
  | NumberedListBlock
  | ChecklistBlock
  | OpportunityCardsBlock
  | ArchetypeCardBlock
  | HeadingBlock;

export interface ParagraphBlock {
  type: 'Paragraph';
  content: string | RichText[];
}

export interface RichText {
  text: string;
  bold?: boolean;
  italic?: boolean;
  link?: string;
  superscript?: boolean;
}

export interface HeadingBlock {
  type: 'Heading';
  level: 3 | 4 | 5;
  content: string;
}

export interface BulletsBlock {
  type: 'Bullets';
  items: (string | RichText[])[];
}

export interface TableBlock {
  type: 'Table';
  headers: string[];
  rows: (string | RichText[])[][];
  variant?: 'default' | 'compact';
}

export interface PersonaBlock {
  type: 'Persona';
  name: string;
  title: string;
  demographics: string;
  psychographics: string;
  painPoints: string[];
  goals: string[];
  imageUrl?: string;
}

export interface CalloutBlock {
  type: 'Callout';
  content: string | RichText[];
  variant?: 'info' | 'warning' | 'success';
}

export interface NumberedListBlock {
  type: 'NumberedList';
  items: (string | RichText[])[];
  variant?: 'default' | 'large'; // 'large' for 01, 02, 03 style with full descriptions
}

export interface ChecklistBlock {
  type: 'Checklist';
  items: ChecklistItem[];
}

export interface ChecklistItem {
  text: string | RichText[];
  checked: boolean;
}

export interface OpportunityCardsBlock {
  type: 'OpportunityCards';
  cards: OpportunityCard[];
}

export interface OpportunityCard {
  title: string;
  content: string | RichText[];
}

export interface ArchetypeCardBlock {
  type: 'ArchetypeCard';
  label: string; // "Primary: Architect" or "Secondary: Collective"
  title: string;
  description: string | RichText[];
  mission: string;
  voice: string;
  values: string;
  emotionalPromise: string;
}
