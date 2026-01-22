import type { RichText } from '../types';

export function renderRichText(content: string | RichText[]): React.ReactNode {
  if (typeof content === 'string') {
    return content;
  }

  return content.map((segment, index) => {
    let element: React.ReactNode = segment.text;

    if (segment.link) {
      element = (
        <a
          key={index}
          href={segment.link}
          className="text-blue-600 hover:text-blue-800 underline"
          target="_blank"
          rel="noopener noreferrer"
        >
          {element}
        </a>
      );
    }

    if (segment.bold) {
      element = <strong key={index}>{element}</strong>;
    }

    if (segment.italic) {
      element = <em key={index}>{element}</em>;
    }

    if (segment.superscript) {
      element = <sup key={index} className="text-xs">{element}</sup>;
    }

    return <span key={index}>{element}</span>;
  });
}
