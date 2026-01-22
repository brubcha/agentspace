import type { ParagraphBlock as ParagraphBlockType } from '../types';
import { renderRichText } from '../utils/renderRichText';

interface Props {
  block: ParagraphBlockType;
}

export function ParagraphBlock({ block }: Props) {
  return (
    <p className="text-base leading-relaxed text-gray-800 mb-4">
      {renderRichText(block.content)}
    </p>
  );
}