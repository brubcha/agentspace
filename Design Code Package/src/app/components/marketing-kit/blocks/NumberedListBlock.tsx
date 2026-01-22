import type { NumberedListBlock as NumberedListBlockType } from '../types';
import { renderRichText } from '../utils/renderRichText';

interface Props {
  block: NumberedListBlockType;
}

export function NumberedListBlock({ block }: Props) {
  const isLarge = block.variant === 'large';

  if (isLarge) {
    // Large variant with bold numbered headings (01, 02, 03...)
    return (
      <div className="space-y-6 mb-6">
        {block.items.map((item, index) => (
          <div key={index} className="flex items-start gap-4">
            {/* Large numbered badge */}
            <div className="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-orange-400 to-amber-500 flex items-center justify-center shadow-md">
              <span className="text-white text-base font-bold">
                {String(index + 1).padStart(2, '0')}
              </span>
            </div>
            {/* Content */}
            <div className="text-base text-gray-800 flex-1 pt-1.5">
              {renderRichText(item)}
            </div>
          </div>
        ))}
      </div>
    );
  }

  // Default variant - simpler style
  return (
    <div className="space-y-4 mb-6">
      {block.items.map((item, index) => (
        <div key={index} className="flex items-start gap-4">
          {/* Numbered circle */}
          <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-orange-400 to-amber-500 flex items-center justify-center">
            <span className="text-white text-sm font-bold">
              {String(index + 1).padStart(2, '0')}
            </span>
          </div>
          {/* Content */}
          <p className="text-base text-gray-800 flex-1 pt-1">{renderRichText(item)}</p>
        </div>
      ))}
    </div>
  );
}