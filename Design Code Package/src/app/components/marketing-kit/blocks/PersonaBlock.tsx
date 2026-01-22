import type { PersonaBlock as PersonaBlockType } from '../types';
import { ImageWithFallback } from '@/app/components/figma/ImageWithFallback';

interface Props {
  block: PersonaBlockType;
}

export function PersonaBlock({ block }: Props) {
  return (
    <div className="mb-8 border border-gray-200 rounded-lg overflow-hidden bg-white shadow-sm">
      {/* Header with image */}
      <div className="flex items-center gap-4 p-6 bg-gradient-to-r from-blue-50 to-indigo-50">
        {block.imageUrl && (
          <ImageWithFallback
            src={block.imageUrl}
            alt={block.name}
            className="w-20 h-20 rounded-full object-cover border-2 border-white shadow-md"
          />
        )}
        <div>
          <h3 className="text-xl font-bold text-gray-900">{block.name}</h3>
          <p className="text-sm text-gray-600">{block.title}</p>
        </div>
      </div>

      {/* Content */}
      <div className="p-6 space-y-4">
        {/* Demographics */}
        <div>
          <h4 className="text-sm font-semibold text-gray-700 mb-2">Demographics</h4>
          <p className="text-sm text-gray-800">{block.demographics}</p>
        </div>

        {/* Psychographics */}
        <div>
          <h4 className="text-sm font-semibold text-gray-700 mb-2">Psychographics</h4>
          <p className="text-sm text-gray-800">{block.psychographics}</p>
        </div>

        {/* Pain Points */}
        <div>
          <h4 className="text-sm font-semibold text-gray-700 mb-2">Pain Points</h4>
          <ul className="space-y-1">
            {block.painPoints.map((point, index) => (
              <li key={index} className="flex items-start gap-2">
                <span className="text-red-500 mt-0.5">✗</span>
                <span className="text-sm text-gray-800">{point}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Goals */}
        <div>
          <h4 className="text-sm font-semibold text-gray-700 mb-2">Goals</h4>
          <ul className="space-y-1">
            {block.goals.map((goal, index) => (
              <li key={index} className="flex items-start gap-2">
                <span className="text-green-500 mt-0.5">✓</span>
                <span className="text-sm text-gray-800">{goal}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
