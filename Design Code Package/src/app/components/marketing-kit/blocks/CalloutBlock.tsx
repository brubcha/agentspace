import type { CalloutBlock as CalloutBlockType } from '../types';
import { renderRichText } from '../utils/renderRichText';

interface Props {
  block: CalloutBlockType;
}

export function CalloutBlock({ block }: Props) {
  const variantStyles = {
    info: 'bg-blue-50 border-blue-200 text-blue-900',
    warning: 'bg-amber-50 border-amber-200 text-amber-900',
    success: 'bg-green-50 border-green-200 text-green-900',
  };

  const variant = block.variant || 'info';

  return (
    <div
      className={`p-4 rounded-lg border-l-4 mb-6 ${variantStyles[variant]}`}
    >
      <p className="text-sm leading-relaxed">{renderRichText(block.content)}</p>
    </div>
  );
}