import type { OpportunityCardsBlock as OpportunityCardsBlockType } from '../types';
import { renderRichText } from '../utils/renderRichText';

interface Props {
  block: OpportunityCardsBlockType;
}

export function OpportunityCardsBlock({ block }: Props) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
      {block.cards.map((card, index) => (
        <div
          key={index}
          className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow"
        >
          <h3 className="text-lg font-bold text-gray-900 mb-3">
            {card.title}
          </h3>
          <div className="text-base text-gray-700 leading-relaxed">
            {renderRichText(card.content)}
          </div>
        </div>
      ))}
    </div>
  );
}
