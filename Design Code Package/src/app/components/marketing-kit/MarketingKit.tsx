import type { MarketingKitData, Block, Section, Subsection } from './types';
import { ParagraphBlock } from './blocks/ParagraphBlock';
import { BulletsBlock } from './blocks/BulletsBlock';
import { TableBlock } from './blocks/TableBlock';
import { PersonaBlock } from './blocks/PersonaBlock';
import { CalloutBlock } from './blocks/CalloutBlock';
import { NumberedListBlock } from './blocks/NumberedListBlock';
import { ChecklistBlock } from './blocks/ChecklistBlock';
import { OpportunityCardsBlock } from './blocks/OpportunityCardsBlock';
import { ArchetypeCardBlock } from './blocks/ArchetypeCardBlock';
import { HeadingBlock } from './blocks/HeadingBlock';

interface Props {
  data: MarketingKitData;
}

function renderBlock(block: Block, index: number) {
  switch (block.type) {
    case 'Paragraph':
      return <ParagraphBlock key={index} block={block} />;
    case 'Bullets':
      return <BulletsBlock key={index} block={block} />;
    case 'Table':
      return <TableBlock key={index} block={block} />;
    case 'Persona':
      return <PersonaBlock key={index} block={block} />;
    case 'Callout':
      return <CalloutBlock key={index} block={block} />;
    case 'NumberedList':
      return <NumberedListBlock key={index} block={block} />;
    case 'Checklist':
      return <ChecklistBlock key={index} block={block} />;
    case 'OpportunityCards':
      return <OpportunityCardsBlock key={index} block={block} />;
    case 'ArchetypeCard':
      return <ArchetypeCardBlock key={index} block={block} />;
    case 'Heading':
      return <HeadingBlock key={index} block={block} />;
    default:
      return null;
  }
}

function renderSubsection(subsection: Subsection, index: number) {
  return (
    <div key={index} className="mb-6">
      <h3 className="text-xl font-bold text-gray-900 mb-4">{subsection.title}</h3>
      <div>
        {subsection.blocks.map((block, blockIndex) =>
          renderBlock(block, blockIndex)
        )}
      </div>
    </div>
  );
}

function renderSection(section: Section, sectionIndex: number) {
  return (
    <section key={sectionIndex} className="pb-8 border-b border-gray-200 last:border-b-0">
      {/* Section Title */}
      <h2 className="text-2xl font-bold text-gray-900 mb-6">
        {section.title}
      </h2>

      {/* Subsections (if any) */}
      {section.subsections && section.subsections.length > 0 && (
        <div className="space-y-6">
          {section.subsections.map((subsection, subsectionIndex) =>
            renderSubsection(subsection, subsectionIndex)
          )}
        </div>
      )}

      {/* Direct blocks (if any) */}
      {section.blocks && section.blocks.length > 0 && (
        <div>
          {section.blocks.map((block, blockIndex) =>
            renderBlock(block, blockIndex)
          )}
        </div>
      )}
    </section>
  );
}

export function MarketingKit({ data }: Props) {
  return (
    <div className="max-w-full mx-auto bg-white">
      {/* Header */}
      <div className="mb-12 pb-8 border-b-2 border-gray-200">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">
          Marketing Kit
        </h1>
        <p className="text-xl text-gray-600">{data.clientName}</p>
      </div>

      {/* Sections */}
      <div className="space-y-12">
        {data.sections.map((section, sectionIndex) =>
          renderSection(section, sectionIndex)
        )}
      </div>
    </div>
  );
}