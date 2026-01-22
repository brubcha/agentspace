import type { BulletsBlock as BulletsBlockType } from '../types';
import { renderRichText } from '../utils/renderRichText';

interface Props {
  block: BulletsBlockType;
}

export function BulletsBlock({ block }: Props) {
  return (
    <ul className="space-y-2 mb-6">
      {block.items.map((item, index) => (
        <li key={index} className="flex items-start gap-3">
          <span className="text-gray-400 mt-1.5 select-none">•</span>
          <span className="text-base text-gray-800 flex-1">{renderRichText(item)}</span>
        </li>
      ))}
    </ul>
  );
}