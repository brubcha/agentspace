import type { ChecklistBlock as ChecklistBlockType } from '../types';
import { Check, X } from 'lucide-react';
import { renderRichText } from '../utils/renderRichText';

interface Props {
  block: ChecklistBlockType;
}

export function ChecklistBlock({ block }: Props) {
  return (
    <div className="space-y-3 mb-6">
      {block.items.map((item, index) => (
        <div key={index} className="flex items-start gap-3">
          {item.checked ? (
            <Check className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
          ) : (
            <X className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
          )}
          <span className="text-base text-gray-800 flex-1">{renderRichText(item.text)}</span>
        </div>
      ))}
    </div>
  );
}