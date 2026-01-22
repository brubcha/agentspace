import type { HeadingBlock as HeadingBlockType } from '../types';

interface Props {
  block: HeadingBlockType;
}

export function HeadingBlock({ block }: Props) {
  const Tag = `h${block.level}` as keyof JSX.IntrinsicElements;
  
  const styles = {
    3: 'text-xl font-bold text-gray-900 mb-4 mt-6',
    4: 'text-lg font-semibold text-gray-800 mb-3 mt-5',
    5: 'text-base font-semibold text-gray-700 mb-2 mt-4',
  };

  return (
    <Tag className={styles[block.level]}>
      {block.content}
    </Tag>
  );
}
