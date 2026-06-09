import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { cn } from '@/utils';

interface MarkdownRendererProps {
  content: string;
  className?: string;
}

// Custom styles for markdown elements without requiring @tailwindcss/typography plugin
const markdownStyles = {
  h1: 'text-3xl font-bold mt-8 mb-4 text-foreground',
  h2: 'text-2xl font-bold mt-6 mb-3 text-foreground',
  h3: 'text-xl font-semibold mt-5 mb-2 text-foreground',
  h4: 'text-lg font-semibold mt-4 mb-2 text-foreground',
  p: 'mb-4 leading-relaxed',
  ul: 'list-disc pl-6 mb-4 space-y-1',
  ol: 'list-decimal pl-6 mb-4 space-y-1',
  li: 'mb-1',
  blockquote: 'border-l-4 border-muted pl-4 italic text-muted-foreground my-4',
  a: 'text-primary hover:underline',
  hr: 'my-6 border-border',
  img: 'max-w-full h-auto rounded-lg my-4',
  strong: 'font-bold',
  em: 'italic',
  del: 'line-through',
  code: 'bg-muted px-1.5 py-0.5 rounded text-sm font-mono',
  pre: 'bg-muted p-4 rounded-lg overflow-x-auto my-4',
  table: 'min-w-full border-collapse border border-border my-4',
  th: 'border border-border bg-muted px-4 py-2 text-left font-semibold',
  td: 'border border-border px-4 py-2',
};

export function MarkdownRenderer({ content, className }: MarkdownRendererProps) {
  return (
    <div className={cn('max-w-none', className)}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          h1: ({ children }) => <h1 className={markdownStyles.h1}>{children}</h1>,
          h2: ({ children }) => <h2 className={markdownStyles.h2}>{children}</h2>,
          h3: ({ children }) => <h3 className={markdownStyles.h3}>{children}</h3>,
          h4: ({ children }) => <h4 className={markdownStyles.h4}>{children}</h4>,
          p: ({ children }) => <p className={markdownStyles.p}>{children}</p>,
          ul: ({ children }) => <ul className={markdownStyles.ul}>{children}</ul>,
          ol: ({ children }) => <ol className={markdownStyles.ol}>{children}</ol>,
          li: ({ children }) => <li className={markdownStyles.li}>{children}</li>,
          blockquote: ({ children }) => <blockquote className={markdownStyles.blockquote}>{children}</blockquote>,
          a: ({ children, href }) => <a href={href} className={markdownStyles.a} target="_blank" rel="noopener noreferrer">{children}</a>,
          hr: () => <hr className={markdownStyles.hr} />,
          img: ({ src, alt }) => <img src={src} alt={alt} className={markdownStyles.img} />,
          strong: ({ children }) => <strong className={markdownStyles.strong}>{children}</strong>,
          em: ({ children }) => <em className={markdownStyles.em}>{children}</em>,
          del: ({ children }) => <del className={markdownStyles.del}>{children}</del>,
          code: ({ children, inline }: any) =>
            inline ? (
              <code className={markdownStyles.code}>{children}</code>
            ) : (
              <pre className={markdownStyles.pre}>
                <code className="text-sm font-mono">{children}</code>
              </pre>
            ),
          table: ({ children }) => (
            <div className="overflow-x-auto my-4">
              <table className={markdownStyles.table}>{children}</table>
            </div>
          ),
          th: ({ children }) => <th className={markdownStyles.th}>{children}</th>,
          td: ({ children }) => <td className={markdownStyles.td}>{children}</td>,
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}

