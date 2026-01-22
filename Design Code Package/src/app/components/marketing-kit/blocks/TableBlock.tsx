import type { TableBlock as TableBlockType } from '../types';
import { renderRichText } from '../utils/renderRichText';

interface Props {
  block: TableBlockType;
}

export function TableBlock({ block }: Props) {
  return (
    <div className="overflow-x-auto mb-6">
      <table className="w-full border-collapse">
        <thead>
          <tr className="bg-black">
            {block.headers.map((header, index) => (
              <th
                key={index}
                className="px-6 py-3 text-left text-sm font-semibold text-white border border-gray-300"
              >
                {header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {block.rows.map((row, rowIndex) => (
            <tr
              key={rowIndex}
              className={rowIndex % 2 === 0 ? 'bg-white' : 'bg-gray-50'}
            >
              {row.map((cell, cellIndex) => (
                <td
                  key={cellIndex}
                  className="px-6 py-4 text-sm text-gray-800 border border-gray-300 align-top"
                >
                  {renderRichText(cell)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}