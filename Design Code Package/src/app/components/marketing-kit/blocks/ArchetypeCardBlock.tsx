import type { ArchetypeCardBlock as ArchetypeCardBlockType } from '../types';
import { renderRichText } from '../utils/renderRichText';

interface Props {
  block: ArchetypeCardBlockType;
}

export function ArchetypeCardBlock({ block }: Props) {
  const isPrimary = block.label.toLowerCase().includes('primary');
  
  return (
    <div className={`border-2 rounded-lg p-6 mb-8 ${
      isPrimary 
        ? 'bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-300' 
        : 'bg-gradient-to-br from-purple-50 to-pink-50 border-purple-300'
    }`}>
      {/* Label */}
      <div className="mb-4">
        <span className={`inline-block px-3 py-1 rounded-full text-sm font-semibold ${
          isPrimary 
            ? 'bg-blue-600 text-white' 
            : 'bg-purple-600 text-white'
        }`}>
          {block.label}
        </span>
      </div>

      {/* Title */}
      <h3 className="text-2xl font-bold text-gray-900 mb-4">
        {block.title}
      </h3>

      {/* Description */}
      <div className="text-base text-gray-800 leading-relaxed mb-6">
        {renderRichText(block.description)}
      </div>

      {/* Details Grid */}
      <div className="space-y-3 bg-white/50 rounded-lg p-4">
        <div>
          <span className="font-semibold text-gray-900">Mission:</span>{' '}
          <span className="text-gray-800">{block.mission}</span>
        </div>
        <div>
          <span className="font-semibold text-gray-900">Voice:</span>{' '}
          <span className="text-gray-800">{block.voice}</span>
        </div>
        <div>
          <span className="font-semibold text-gray-900">Values:</span>{' '}
          <span className="text-gray-800">{block.values}</span>
        </div>
        <div>
          <span className="font-semibold text-gray-900">Emotional Promise:</span>{' '}
          <span className="text-gray-800 italic">"{block.emotionalPromise}"</span>
        </div>
      </div>
    </div>
  );
}
