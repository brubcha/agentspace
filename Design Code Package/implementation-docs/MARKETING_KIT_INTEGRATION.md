# Marketing Kit Component Library - Integration Guide

## Overview

This component library renders marketing kits with a professional, standardized design regardless of the input content. Perfect for AgentSpace's custom marketing kit generation.

## File Structure

```
/src/app/components/marketing-kit/
├── types.ts                          # TypeScript interfaces
├── MarketingKit.tsx                  # Main component
├── utils/
│   └── renderRichText.tsx            # Rich text formatter
├── blocks/
│   ├── ParagraphBlock.tsx
│   ├── BulletsBlock.tsx
│   ├── TableBlock.tsx
│   ├── PersonaBlock.tsx
│   ├── CalloutBlock.tsx
│   ├── NumberedListBlock.tsx
│   ├── ChecklistBlock.tsx
│   ├── OpportunityCardsBlock.tsx
│   ├── ArchetypeCardBlock.tsx
│   └── HeadingBlock.tsx
└── index.ts                          # Barrel export
```

## Quick Start

### 1. Import the component

```tsx
import { MarketingKit } from '@/app/components/marketing-kit';
import type { MarketingKitData } from '@/app/components/marketing-kit';
```

### 2. Use it with your agent's output

```tsx
function YourComponent() {
  const [marketingKitData, setMarketingKitData] = useState<MarketingKitData | null>(null);

  // When your agent generates data
  const handleAgentResponse = (agentOutput) => {
    setMarketingKitData(agentOutput);
  };

  return (
    <div>
      {marketingKitData && <MarketingKit data={marketingKitData} />}
    </div>
  );
}
```

## Data Structure

The component expects data in this format:

```typescript
{
  clientName: string;
  sections: [
    {
      title: string;
      // Option 1: Direct blocks
      blocks: [...],
      // Option 2: Nested subsections
      subsections: [
        {
          title: string;
          blocks: [...]
        }
      ]
    }
  ]
}
```

## Rich Text Support

All text content supports rich formatting:

```python
# Python example - Simple string
content = "Plain text paragraph"

# Python example - Rich text with formatting
content = [
    {"text": "This is ", "bold": False},
    {"text": "bold text", "bold": True},
    {"text": " and this is ", "bold": False},
    {"text": "italic", "italic": True},
    {"text": " with a ", "bold": False},
    {"text": "link", "link": "https://example.com"},
    {"text": " and a footnote", "bold": False},
    {"text": "1", "superscript": True}
]
```

## Block Types

### 1. Paragraph Block
Simple or rich text content.

```python
{
    "type": "Paragraph",
    "content": "Your text here..."
    # OR with rich text:
    # "content": [
    #     {"text": "Bold text", "bold": True},
    #     {"text": " normal text"}
    # ]
}
```

### 2. Bullets Block
Unordered list with bullet points.

```python
{
    "type": "Bullets",
    "items": [
        "First item",
        "Second item",
        # Can also use rich text:
        [
            {"text": "Bold item", "bold": True},
            {"text": " with normal text"}
        ]
    ]
}
```

### 3. Numbered List Block
Numbered items with orange circular badges (01, 02, 03...).

```python
{
    "type": "NumberedList",
    "variant": "default",  # or "large" for big key findings
    "items": [
        "First step",
        "Second step",
        # Can use rich text for bold headings:
        [
            {"text": "Bold Heading", "bold": True},
            {"text": "\nFollowed by description text"}
        ]
    ]
}
```

### 4. Checklist Block
Items with green checkmarks ✓ or red X marks ✗.

```python
{
    "type": "Checklist",
    "items": [
        {"text": "Completed task", "checked": True},
        {"text": "Pending task", "checked": False},
        # Can use rich text:
        {
            "text": [
                {"text": "Task with ", "bold": False},
                {"text": "formatting", "bold": True}
            ],
            "checked": True
        }
    ]
}
```

### 5. Table Block
Professional tables with black headers.

```python
{
    "type": "Table",
    "headers": ["Column 1", "Column 2", "Column 3"],
    "rows": [
        ["Row 1 Cell 1", "Row 1 Cell 2", "Row 1 Cell 3"],
        # Can use rich text in cells:
        [
            [
                {"text": "Bold cell", "bold": True}
            ],
            "Normal cell",
            [
                {"text": "Link cell", "link": "https://example.com"}
            ]
        ]
    ],
    "variant": "default"  # or "compact"
}
```

### 6. Persona Block
User persona cards with demographics, psychographics, pain points, and goals.

```python
{
    "type": "Persona",
    "name": "Sarah Chen",
    "title": "VP of Engineering",
    "demographics": "Age 38-45, MBA or Computer Science degree...",
    "psychographics": "Values innovation and efficiency...",
    "painPoints": [
        "Legacy systems slowing down development",
        "Difficulty scaling infrastructure"
    ],
    "goals": [
        "Modernize technology stack",
        "Improve development velocity by 30%"
    ],
    "imageUrl": "https://example.com/image.jpg"  # Optional
}
```

### 7. Callout Block
Highlighted information boxes (info, warning, success).

```python
{
    "type": "Callout",
    "content": "Important information to highlight...",
    # Or rich text:
    # "content": [{"text": "Bold callout", "bold": True}],
    "variant": "info"  # "info" | "warning" | "success"
}
```

### 8. Opportunity Cards Block
Grid of opportunity/feature cards.

```python
{
    "type": "OpportunityCards",
    "cards": [
        {
            "title": "Workflow Efficiency",
            "content": "Description of the opportunity..."
            # Can use rich text for content
        },
        {
            "title": "Digital Tools",
            "content": "Another opportunity..."
        }
    ]
}
```

### 9. Archetype Card Block
Special cards for brand archetypes with gradient backgrounds.

```python
{
    "type": "ArchetypeCard",
    "label": "Primary: Architect (System Builder)",
    "title": "The Architect",
    "description": "As the Architect archetype, Swift Innovation exists to...",
    "mission": "Build and align the infrastructure...",
    "voice": "Confident, precise, structured, outcome-focused.",
    "values": "Integration, clarity, accountability, design of systems.",
    "emotionalPromise": "We don't patch problems - we architect momentum."
}
```

### 10. Heading Block
Subsection headings (H3, H4, H5).

```python
{
    "type": "Heading",
    "level": 3,  # 3, 4, or 5
    "content": "Subsection Title"
}
```

## Section Structure

### Flat Sections (Direct Blocks)
```python
{
    "title": "Section Title",
    "blocks": [
        {"type": "Paragraph", "content": "Text here..."},
        {"type": "Bullets", "items": ["Item 1", "Item 2"]}
    ]
}
```

### Nested Sections (With Subsections)
```python
{
    "title": "Main Section Title",
    "subsections": [
        {
            "title": "Subsection 1",
            "blocks": [
                {"type": "Paragraph", "content": "Text..."}
            ]
        },
        {
            "title": "Subsection 2",
            "blocks": [
                {"type": "Bullets", "items": ["Item 1", "Item 2"]}
            ]
        }
    ]
}
```

### Mixed (Subsections + Direct Blocks)
```python
{
    "title": "Section Title",
    "subsections": [
        {
            "title": "First Subsection",
            "blocks": [...]
        }
    ],
    "blocks": [
        # These blocks appear after all subsections
        {"type": "Paragraph", "content": "Additional content..."}
    ]
}
```

## Python to TypeScript Mapping

The JSON structure generated by your Python agent works directly with the React component:

```python
# Your Python agent generates:
marketing_kit = {
    "clientName": "Swift Innovation",
    "sections": [
        {
            "title": "Overview",
            "subsections": [
                {
                    "title": "How to Use It",
                    "blocks": [
                        {
                            "type": "Paragraph",
                            "content": [
                                {"text": "This kit serves as the ", "bold": False},
                                {"text": "foundation", "bold": True},
                                {"text": " for all Swift activity."}
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "title": "Key Findings",
            "blocks": [
                {
                    "type": "NumberedList",
                    "variant": "large",
                    "items": [
                        [
                            {"text": "Finding Title", "bold": True},
                            {"text": "\nDetailed description here..."}
                        ]
                    ]
                }
            ]
        }
    ]
}
```

This JSON structure is passed directly to the React component without transformation.

## Styling

The components match your original Google Doc design:

- **Colors**: Black table headers, orange numbered badges, green checkmarks, red X marks, blue/purple archetype cards
- **Typography**: Clean sans-serif, hierarchical headings, bold/italic support
- **Layout**: Max-width 896px (4xl), centered, white background, generous spacing
- **Tables**: Black headers with white text, alternating row colors, bordered cells
- **Cards**: Gradient backgrounds for archetypes, shadow effects for opportunities

All styling is done with Tailwind CSS v4.

## Customization

### Changing Colors
Edit individual block components in `/src/app/components/marketing-kit/blocks/`

### Adding New Block Types
1. Add new interface to `types.ts`
2. Create new block component in `blocks/` folder
3. Add case to `renderBlock()` function in `MarketingKit.tsx`

### Adjusting Layout
Modify `MarketingKit.tsx` to change spacing, max-width, or section dividers

## Example: Complete Marketing Kit

See `/src/app/App.tsx` for a full working example matching the Swift Innovation structure with:
- Subsections ("How to Use It", "What's Inside")
- Rich text formatting (bold, italic, links, superscripts)
- Opportunity cards
- Brand archetype cards
- Large numbered lists for key findings
- Tables with channel opportunities
- References with formatted citations

## Dependencies

- React 18.3+
- Tailwind CSS 4.0+
- lucide-react (for icons)

All dependencies are already installed in this project.

## For AgentSpace Developers

### Integration Steps:
1. Copy the `/src/app/components/marketing-kit/` folder into your AgentSpace codebase
2. Ensure you have Tailwind CSS configured
3. Install `lucide-react` if not already present
4. Have your Python agent generate JSON matching the structure above
5. Pass the JSON directly to the `<MarketingKit data={jsonData} />` component

### Data Flow:
```
User Form Input → Python Agent → JSON Structure → React Component → Rendered Marketing Kit
```

The JSON structure is **identical** between Python and TypeScript, so no transformation needed!
