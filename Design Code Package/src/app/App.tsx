import { MarketingKit } from "@/app/components/marketing-kit";
import type { MarketingKitData } from "@/app/components/marketing-kit";

// Complete Swift Innovation Marketing Kit data
const sampleData: MarketingKitData = {
  clientName: "Swift Innovation",
  sections: [
    // OVERVIEW SECTION
    {
      title: "Overview",
      subsections: [
        {
          title: "",
          blocks: [
            {
              type: "Paragraph",
              content:
                "Swift Innovation is more than a services company, it is a connected system of disciplines designed to build momentum for businesses. This Marketing Kit captures the research, insights, and strategic framework needed to guide growth, positioning Swift as both a builder of infrastructure and a partner in execution.",
            },
            {
              type: "Subhead",
              text: "Purpose of the Kit",
            },
            {
              type: "Bullets",
              items: [
                "Clarify Swift's position in the Support + Products + Platform market.",
                "Define target audiences and their challenges.",
                "Document Swift's voice, archetypes, and identity.",
                "Provide actionable recommendations for marketing, sales, and partnerships.",
              ],
            },
          ],
        },
        {
          title: "How to Use It",
          blocks: [
            {
              type: "Paragraph",
              content:
                "This kit serves as the foundation for all Swift activity, from campaigns and creative assets to sales presentations and partnerships. By following its guidelines, every communication will reflect Swift's clarity, connectedness, and focus on outcomes.",
            },
          ],
        },
        {
          title: "What's Inside",
          blocks: [
            {
              type: "Bullets",
              items: [
                "The Goal",
                "Key Findings",
                "Brand Voice",
                "Market Landscape",
                "Audience & Personas",
                "Brand Archetypes",
              ],
            },
          ],
        },
      ],
    },

    // THE GOAL SECTION
    {
      title: "The Goal",
      blocks: [
        {
          type: "Paragraph",
          content:
            "To establish Swift Innovation as the go-to partner for companies seeking to align strategy, speed, and execution under one roof. First by dominating the mid-market B2B space (manufacturing, technology, services), and then scaling into vertical-specific ecosystems through Agency Direct and White Label channels.",
        },
      ],
    },

    // OPPORTUNITY AREAS SECTION
    {
      title: "Opportunity Areas",
      blocks: [
        {
          type: "OpportunityCards",
          cards: [
            {
              title: "Workflow Efficiency",
              content:
                "Silos slow everything down - marketing runs campaigns without dev support, sales works leads without aligned operations, leadership loses clarity. Swift solves this by embedding cross-disciplinary teams into client workflows. Design, marketing, development, and strategy operate as one unit, creating seamless handoffs, faster delivery, and a culture of aligned execution that compounds growth.",
            },
            {
              title: "Digital Tools",
              content:
                "Disconnected platforms create wasted time and unclear results. Swift equips every client with a unified foundation of CRMs, analytics, and automation - the same operational backbone we use ourselves. This structure provides real-time visibility, automates repeatable tasks, and creates scalable infrastructure that supports growth without chaos.",
            },
            {
              title: "Market Trends",
              content:
                "Business is shifting fast: 60% of the workforce will be independent by 2027, 66% of companies outsource, and 73% already hire globally. Swift was built for this future. By embracing independence, distributed expertise, and embedded partnerships, we position clients not just to adapt but to gain an advantage from the new world of work.",
            },
            {
              title: "Revenue Streams",
              content:
                "Sustainable growth requires layered channels. Swift expands revenue through:",
            },
          ],
        },
        {
          type: "Bullets",
          items: [
            [
              { text: "Support Retainers", bold: true },
              { text: " → Ongoing, embedded cross-functional teams." },
            ],
            [
              { text: "Productized Deliverables", bold: true },
              {
                text: " → Fixed-scope assets (websites, decks, reviews) delivered with speed and clarity.",
              },
            ],
            [
              { text: "Platform Licensing", bold: true },
              {
                text: " → Branded CRM and analytics environments that create sticky, recurring infrastructure.",
              },
            ],
          ],
        },
      ],
    },

    // KEY FINDINGS SECTION
    {
      title: "Key Findings",
      blocks: [
        {
          type: "NumberedList",
          variant: "large",
          items: [
            [
              { text: "Fragmentation is the Core Problem", bold: true },
              {
                text: "\nMost businesses piece together agencies, consultants, and disconnected tools. This creates silos, wasted spend, and stalled execution. Swift was designed to remove fragmentation by embedding all disciplines under one roof.",
              },
            ],
            [
              { text: "Independence is Reshaping Work", bold: true },
              {
                text: "\nBy 2027, 60% of the workforce will be independent, and most companies already outsource or hire globally. Swift's model embraces this shift, connecting distributed expertise into a unified system.",
              },
            ],
            [
              { text: "Execution is the Bottleneck", bold: true },
              {
                text: "\nStrategy without delivery - or delivery without strategy - stalls growth. Competitors lean one way or the other. Swift bridges this gap by aligning strategy, speed, and execution.",
              },
            ],
            [
              { text: "The Mid-Market is Underserved", bold: true },
              {
                text: "\nSmaller companies rely on scrappy tactics, while enterprises hire full teams and agencies. Mid-market businesses are left in between - too complex for freelancers, too lean for enterprise retainers. Swift focuses on this gap.",
              },
            ],
            [
              { text: "Embedded Models Outperform Vendors", bold: true },
              {
                text: '\nHiring "another agency" adds more complexity. Businesses scale faster when expertise is embedded, accountable, and aligned to outcomes. Swift operates as an extension of the client team, not just a vendor.',
              },
            ],
            [
              { text: "Infrastructure is the Differentiator", bold: true },
              {
                text: "\nMost competitors stop at services. Swift builds systems: CRM, automation, and analytics platforms that create consistency, visibility, and scale. This backbone is what makes results sustainable.",
              },
            ],
          ],
        },
      ],
    },

    // MARKET LANDSCAPE SECTION
    {
      title: "Market Landscape",
      subsections: [
        {
          title: "Macro Trends & Growth",
          blocks: [
            {
              type: "Bullets",
              items: [
                [
                  { text: "Outsourcing is mainstream.", bold: true },
                  {
                    text: " Roughly 66% of U.S. businesses outsource at least one department, including IT, HR, and marketing.",
                  },
                  { text: "1", superscript: true },
                ],
                [
                  { text: "Independence is surging.", bold: true },
                  {
                    text: " Workforce models are shifting - fractional and freelance talent is increasingly central to the future of work.",
                  },
                  { text: "2", superscript: true },
                ],
                [
                  { text: "Businesses scale globally.", bold: true },
                  {
                    text: " The global BPO market is valued at $302.6 billion (2024) with projected growth to $525 billion by 2030.",
                  },
                  { text: "3", superscript: true },
                ],
                [
                  { text: "Strategic not just tactical.", bold: true },
                  {
                    text: " Outsourcing is evolving into a tool for innovation and flexibility, not just cost savings or capacity fill-ins.",
                  },
                  { text: "4", superscript: true },
                ],
              ],
            },
          ],
        },
        {
          title: "Competitor Landscape & Buying Behavior",
          blocks: [
            {
              type: "Bullets",
              items: [
                [
                  { text: 'Agencies sell "campaigns."', bold: true },
                  {
                    text: " They focus on tactical execution rather than integrated strategy and infrastructure.",
                  },
                ],
                [
                  { text: 'Consultants sell "strategy."', bold: true },
                  {
                    text: " Insight-rich but often disconnected from execution and follow-through.",
                  },
                ],
                [
                  { text: 'Dev shops sell "code."', bold: true },
                  {
                    text: " Technical execution without strategic framing or broader business alignment.",
                  },
                ],
                [
                  { text: "Swift sells all three-embedded.", bold: true },
                  {
                    text: " Our model combines strategy, fast execution, and infrastructure in one aligned package, bridging the gaps competitors leave behind.",
                  },
                ],
              ],
            },
          ],
        },
        {
          title: "Channel Opportunities",
          blocks: [
            {
              type: "Table",
              headers: ["Channel", "Opportunity Insight", "Recommendation"],
              rows: [
                [
                  "Search (Google)",
                  "Decision-makers in mid-market companies actively search for solutions around outsourcing, CRM setup, digital transformation, and growth strategy.",
                  'Launch high-priority search campaigns targeting terms like "fractional marketing support," "outsourced development team," and "CRM for mid-market businesses." Build landing pages aligned to each search intent.',
                ],
                [
                  "Awareness Channels (FB/IG/YouTube)",
                  "Business owners and executives are exposed to brand credibility via thought leadership and case storytelling, even if they don't convert immediately.",
                  "Use short video explainers and client stories to showcase momentum, execution speed, and integrated disciplines. Position Swift as the alternative to fragmented agencies and consultants.",
                ],
                [
                  "Email Marketing (B2B)",
                  "Executives and founders expect clear communication, education, and proof before booking exploratory calls.",
                  "Deploy nurture flows highlighting case studies, industry insights, and ROI proof points. Segment by vertical (manufacturing, tech, services) for relevance.",
                ],
                [
                  "B2B Partnerships / Retail",
                  "Agencies and consultancies lack capacity but need reliable execution partners. White-label partnerships offer scalability.",
                  "Build structured white-label programs with sell sheets, co-branded case studies, and agency outreach campaigns.",
                ],
                [
                  "LinkedIn",
                  "Primary platform for C-suite, founders, and decision-makers. Strongest channel for direct outreach and thought leadership.",
                  "Invest in LinkedIn both for outbound (cold campaigns, InMail) and inbound (thought leadership posts, case content). Build credibility through leadership profiles (CEO/CCO).",
                ],
              ],
            },
          ],
        },
      ],
    },

    // AUDIENCE & USER PERSONAS SECTION
    {
      title: "Audience & User Personas",
      subsections: [
        {
          title: "B2B User Personas",
          blocks: [
            {
              type: "Persona",
              name: "The Overloaded Founder",
              title:
                "Scrappy founders running mid-market companies who juggle multiple hats and feel the strain of disconnected teams, tools, and vendors.",
              demographics:
                "Gen X/Millennial founders; often in manufacturing, tech, or service industries.",
              psychographics:
                'Ambitious but burned out; values autonomy, quick wins, and partners who "get it done."',
              painPoints: [
                "Profile: Founders/CEOs of $1M–$20M businesses.",
                "Motivation: Free up time and mental bandwidth to focus on vision.",
                "Needs: Reliable execution, clarity across disciplines, and partners who can own outcomes without handholding.",
                'Messaging: "Momentum without micromanagement."',
                "Buying Behavior: Chooses vendors who feel like extensions of their team; willing to pay for speed, efficiency, and reduced complexity.",
              ],
              goals: [],
            },
            {
              type: "Persona",
              name: "The Skeptical Executive",
              title:
                "Leaders who have been burned by agencies or consultants before and now demand proof, accountability, and outcomes.",
              demographics: "Senior leaders at $10M–$100M companies.",
              psychographics:
                "Data-driven, expects rigor and reliability; values credibility over creativity alone.",
              painPoints: [
                "Profile: COOs, CMOs, and VPs of Growth in mid-sized companies.",
                "Motivation: Confidence in execution, transparency in reporting, and measurable ROI.",
                "Needs: Strategy tied directly to delivery; clear visibility into results.",
                'Messaging: "Not another vendor. A connected partner."',
                "Buying Behavior: Requires case studies, references, and dashboards; signs long-term once trust is built.",
              ],
              goals: [],
            },
            {
              type: "Persona",
              name: "The White Label Agency Lead",
              title:
                "Agency owners and consultants who need to scale capacity but can't afford to hire in-house.",
              demographics:
                "Agency teams of 5–25, often in design, marketing, or niche tech services.",
              psychographics:
                "Entrepreneurial, protective of their client relationships, values white-label discretion.",
              painPoints: [
                "Profile: Agency founders or boutique consultants (marketing, creative, or dev shops).",
                "Motivation: Increase delivery capacity while protecting margins.",
                "Needs: Invisible, reliable execution partner who works seamlessly under their brand.",
                'Messaging: "Expand without overhead."',
                "Buying Behavior: Buys on trust; long-term partnerships once delivery quality is proven.",
              ],
              goals: [],
            },
            {
              type: "Persona",
              name: "The Enterprise Operator",
              title:
                "Executives at larger organizations who need embedded support without adding headcount.",
              demographics:
                "Corporate decision-makers in operations, marketing, or digital transformation.",
              psychographics:
                "Risk-averse but pragmatic; values proven partners who can navigate enterprise complexity.",
              painPoints: [
                "Profile: Directors and senior managers at enterprises ($100M+ revenue).",
                "Motivation: Fill capability gaps quickly without navigating corporate hiring hurdles.",
                "Needs: Cross-functional expertise, scalable infrastructure, and embedded teams that feel internal.",
                'Messaging: "Teams that build momentum."',
                "Buying Behavior: Engages via pilot projects; expands to multi-discipline retainers when results are clear.",
              ],
              goals: [],
            },
          ],
        },
        {
          title: "B2B Industry Targets",
          blocks: [
            {
              type: "Heading",
              level: 4,
              content: "Manufacturing",
            },
            {
              type: "Bullets",
              items: [
                [
                  { text: "Mid-Market Manufacturers", bold: true },
                  {
                    text: "\nCompanies ($10M–$250M) modernizing operations, sales, and customer engagement.",
                  },
                ],
                [
                  { text: "Niche Industrial Producers", bold: true },
                  {
                    text: "\nPlastics, materials, and component manufacturers needing branding, sales support, and digital presence.",
                  },
                ],
                [
                  { text: "Regional Supply Chain Operators", bold: true },
                  {
                    text: "\nManufacturers seeking CRM, workflow, and automation tools to streamline B2B distribution and partnerships.",
                  },
                ],
                [
                  { text: "OEM & Equipment Builders", bold: true },
                  {
                    text: "\nProducers requiring scalable marketing infrastructure and sales enablement to support dealer networks.",
                  },
                ],
              ],
            },
            {
              type: "Heading",
              level: 4,
              content: "Software & Technology",
            },
            {
              type: "Bullets",
              items: [
                [
                  { text: "SaaS Scale-Ups", bold: true },
                  {
                    text: "\nGrowth-stage companies needing embedded marketing, design, and development to accelerate adoption.",
                  },
                ],
                [
                  { text: "Independent Software Vendors (ISVs)", bold: true },
                  {
                    text: "\nTeams that require CRM, automation, and product marketing infrastructure.",
                  },
                ],
                [
                  { text: "Tech-Enabled Services", bold: true },
                  {
                    text: "\nBusinesses offering hybrid software + services models that lack in-house creative and operational depth.",
                  },
                ],
                [
                  { text: "AI & Emerging Tech Firms", bold: true },
                  {
                    text: "\nInnovators requiring brand credibility, decks, and proposals to secure funding and partnerships.",
                  },
                ],
              ],
            },
            {
              type: "Heading",
              level: 4,
              content: "Agencies & Channel Partners",
            },
            {
              type: "Bullets",
              items: [
                [
                  { text: "Independent Marketing Agencies", bold: true },
                  {
                    text: "\n5–50 person firms seeking white-label design, dev, or marketing execution.",
                  },
                ],
                [
                  { text: "Creative Boutiques", bold: true },
                  {
                    text: "\nNiche design and branding shops needing support to scale delivery capacity.",
                  },
                ],
                [
                  { text: "Consultants & Fractional Leaders", bold: true },
                  {
                    text: "\nFractional CMOs, COOs, and growth consultants requiring execution to turn strategies into outcomes.",
                  },
                ],
                [
                  { text: "Agency Networks", bold: true },
                  {
                    text: "\nGroups of small agencies that can resell or embed Swift's CRM + analytics platform under their own brand.",
                  },
                ],
              ],
            },
            {
              type: "Heading",
              level: 4,
              content: "Consumer Goods",
            },
            {
              type: "Bullets",
              items: [
                [
                  { text: "Emerging Consumer Brands", bold: true },
                  {
                    text: "\nEarly-stage DTC companies building brand identity, websites, and ecommerce platforms.",
                  },
                ],
                [
                  { text: "Mid-Market Consumer Goods", bold: true },
                  {
                    text: "\nCompanies scaling regionally/nationally that require CRM-driven sales infrastructure and digital marketing.",
                  },
                ],
                [
                  { text: "Lifestyle & Specialty Goods", bold: true },
                  {
                    text: "\nPremium product makers needing brand kits, campaign execution, and retail support.",
                  },
                ],
                [
                  { text: "Retail-Ready Brands", bold: true },
                  {
                    text: "\nConsumer packaged goods expanding into retail channels that need design, sales, and marketing alignment.",
                  },
                ],
              ],
            },
          ],
        },
        {
          title: "NAICS Codes Research",
          blocks: [
            {
              type: "Table",
              headers: [
                "Category",
                "NAICS Code",
                "USA Companies Est.",
                "Description",
              ],
              rows: [
                [
                  "Pet Retail / Pet Products",
                  "459910",
                  "10,853",
                  "Pet and Pet Supplies Retailers: Retailing pets, pet foods, and pet supplies.",
                ],
                [
                  "Pet Care (non-veterinary)",
                  "812910",
                  "32,943",
                  "Pet Care (except Veterinary) Services: Pet grooming, boarding, daycare, walking, sitting, etc.",
                ],
                [
                  "Veterinary Services",
                  "541940",
                  "46,350",
                  "Veterinary Services: Practice of veterinary medicine, dentistry, surgery for pets; includes pet hospitals and clinics.",
                ],
                [
                  "Pet Food Manufacturing",
                  "311111 and 311119",
                  "153 and 1,797",
                  "Dog and Cat Food Manufacturing and Other Animal Food Manufacturing: For companies producing pet foods.",
                ],
                [
                  "Wholesale (Pets & Supplies)",
                  "424990",
                  "3,209",
                  "Other Miscellaneous Nondurable Goods Merchant Wholesalers: Includes wholesalers in pet-related categories.",
                ],
              ],
            },
            {
              type: "Table",
              headers: [
                "Category",
                "NAICS Code(s)",
                "Estimated U.S. Companies",
                "Description",
              ],
              rows: [
                [
                  "Manufacturing",
                  "31-33",
                  "~660,000 establishments",
                  "Manufacturers of goods from machinery to electronics, components, materials (NAICS Association, NAICS Association, Bureau of Labor Statistics)",
                ],
                [
                  "Software & Technology",
                  "541511, 541512",
                  "Part of ~2.49 million in professional, scientific, and technical services (NAICS Association)",
                  "NAICS 541511: Custom Computer Programming Services; 541512: Computer Systems Design",
                ],
                [
                  "Agencies & Consultants",
                  "541611",
                  "Within ~2.49 million in professional, scientific, and technical services (NAICS Association)",
                  "Administrative Management & General Management Consulting",
                ],
                [
                  "Consumer Goods (DTC)",
                  "454110, 454311",
                  "Within broader retail (~1.8 million U.S. retail businesses) (NAICS Association)",
                  "Electronic Shopping/Mail-order houses; Warehouse clubs & supercenters",
                ],
              ],
            },
          ],
        },
        {
          title: "Data Broker Research",
          blocks: [
            {
              type: "Table",
              headers: [
                "Industry",
                "Global Companies Est.",
                "USA Companies Est.",
                "Description",
              ],
              rows: [
                [
                  "Manufacturing",
                  "1M",
                  "150K",
                  "Electronic Manufacturing, Food Manufacturing, Machinery",
                ],
                [
                  "Software & Technology",
                  "2.6M",
                  "477K",
                  "Software and Information Technology: SaaS",
                ],
                [
                  "Agencies & Consultants",
                  "1M",
                  "232K",
                  "Marketing and Advertising Agencies",
                ],
                [
                  "Consumer Goods (DTC)",
                  "80K",
                  "21K",
                  "Consumer Goods and Consumer Electronics",
                ],
              ],
            },
          ],
        },
      ],
    },

    // BRAND ARCHETYPES SECTION
    {
      title: "Brand Archetypes",
      blocks: [
        {
          type: "ArchetypeCard",
          label: "Primary: Architect (System Builder)",
          title: "The Architect",
          description:
            "As the Architect archetype, Swift Innovation exists to design and connect the systems that power growth. We are not just another agency or consultancy - we build frameworks where design, marketing, development, operations, sales, and strategy align under one roof. Originality lives in how we integrate disciplines; precision lives in the infrastructure we create. Our voice is confident and structured, using clear, outcome-driven language to demonstrate how fragmented efforts become momentum when brought together. The result is not just outsourced support, but a growth engine designed with purpose.",
          mission:
            "Build and align the infrastructure that allows businesses to scale without fragmentation.",
          voice: "Confident, precise, structured, outcome-focused.",
          values: "Integration, clarity, accountability, design of systems.",
          emotionalPromise: "We don't patch problems - we architect momentum.",
        },
        {
          type: "ArchetypeCard",
          label: "Secondary: Collective (Community Builder)",
          title: "The Collective",
          description:
            "Embracing the Collective archetype, Swift stands as proof that independence is strongest when it moves together. We thrive on connection - independents collaborating across borders, disciplines working without silos, ideas scaling through shared execution. Our role is to unify, not command: to foster collaboration, shared ownership, and sustainable momentum. Our voice is inclusive, collaborative, and forward-moving, using language that emphasizes unity and progress over hierarchy. For clients, the message is clear - when you work with Swift, you don't hire a vendor; you join a system of independence moving as one.",
          mission:
            "Prove that independence is strongest when it moves together, unbound by borders, labels, or limits.",
          voice: "Inclusive, collaborative, momentum-driven.",
          values: "Connection, contribution, trust, shared progress.",
          emotionalPromise: "We don't just work for you - we move with you.",
        },
      ],
    },

    // BRAND VOICE SECTION (COMPLETE)
    {
      title: "Brand Voice",
      subsections: [
        {
          title: "Brand Essence",
          blocks: [
            {
              type: "Paragraph",
              content: [
                { text: "Momentum through clarity.", bold: true },
                {
                  text: " Swift Innovation transforms fragmented efforts into connected systems - embedding design, marketing, development, operations, sales, and strategy under one roof. We move with precision and speed, creating infrastructure that drives growth without chaos.",
                },
              ],
            },
          ],
        },
        {
          title: "Brand Purpose",
          blocks: [
            {
              type: "Paragraph",
              content:
                "Help businesses grow without fragmentation by uniting strategy, execution, and technology in one embedded partner - so leaders can focus on vision while Swift delivers momentum.",
            },
          ],
        },
        {
          title: "Brand Personality",
          blocks: [
            {
              type: "Paragraph",
              content: [
                { text: "Adjectives: ", bold: true },
                {
                  text: "Confident, precise, collaborative, accountable, modern, outcome-driven",
                },
              ],
            },
            {
              type: "Paragraph",
              content: [
                { text: "Expression: ", bold: true },
                {
                  text: "Clear, declarative statements; structured yet approachable; future-focused with a pragmatic edge",
                },
              ],
            },
          ],
        },
        {
          title: "Tone & Voice Examples",
          blocks: [
            {
              type: "Bullets",
              items: [
                '"We measure outcomes, not hours."',
                '"Independence is strongest when it moves together."',
                '"Momentum without micromanagement."',
                '"Strategy is nothing without execution."',
              ],
            },
          ],
        },
        {
          title: "Voice in Action",
          blocks: [
            {
              type: "Bullets",
              items: [
                [
                  { text: "Homepage headline: ", bold: true },
                  {
                    text: '"Building momentum through connected disciplines."',
                  },
                ],
                [
                  { text: "LinkedIn caption: ", bold: true },
                  {
                    text: '"Most agencies sell campaigns. Consultants sell strategy. Dev shops sell code. We bring them together into one embedded system - designed to deliver outcomes."',
                  },
                ],
                [
                  { text: "Twitter/X Post: ", bold: true },
                  {
                    text: '"Growth doesn\'t stall from lack of ideas. It stalls from fragmentation. Swift Innovation removes the silos so execution actually scales."',
                  },
                ],
                [
                  { text: "Sales Deck Slide: ", bold: true },
                  {
                    text: '"Products. Support. Platform. Three tracks. One system. Growth without fragmentation."',
                  },
                ],
                [
                  { text: "Google Search Ad: ", bold: true },
                  {
                    text: "Headline: Outsourced Support + Products | Description: Design, marketing, and development aligned under one roof. Faster outcomes, scalable infrastructure.",
                  },
                ],
                [
                  { text: "Email reassurance: ", bold: true },
                  {
                    text: '"Swift isn\'t another vendor. We embed as part of your team, aligning strategy, execution, and tools to deliver measurable outcomes."',
                  },
                ],
              ],
            },
          ],
        },
        {
          title: "Factual Foundations",
          blocks: [
            {
              type: "Bullets",
              items: [
                "Support + Products + Platform model",
                "Disciplines: Design, Marketing, Development, Sales, Operations, Strategy, Maintenance",
                "Embedded + white-label delivery capability",
                "CRM + analytics platform backbone",
                "Proven results across multiple industries (manufacturing, software, consumer goods, agencies)",
              ],
            },
          ],
        },
        {
          title: "Taglines (Evaluated)",
          blocks: [
            {
              type: "Checklist",
              items: [
                { text: '"Momentum without micromanagement."', checked: true },
                { text: '"Strategy. Speed. Execution."', checked: true },
                { text: '"Outcomes over hours."', checked: true },
                { text: '"Independence, aligned."', checked: true },
                { text: '"Growth without fragmentation."', checked: true },
                {
                  text: '"Your partner for everything business." (generic)',
                  checked: false,
                },
                {
                  text: '"Solutions made simple." (overused, vague)',
                  checked: false,
                },
                { text: '"Think outside the box." (cliché)', checked: false },
              ],
            },
          ],
        },
        {
          title: "Client Do's & Don'ts",
          blocks: [
            {
              type: "Heading",
              level: 4,
              content: "✅ Do's (On-Brand Actions & Language)",
            },
            {
              type: "Bullets",
              items: [
                "Lead with clarity and confidence - short, declarative statements that emphasize outcomes.",
                "Highlight Swift's unique model: Support + Products + Platform.",
                "Emphasize independence, embedded collaboration, and elimination of silos.",
                "Celebrate measurable progress: execution speed, infrastructure, and momentum.",
                "Show proof through case studies, dashboards, and results, not just claims.",
                "Use modern, structured visuals - clean grids, bold typography, systems imagery.",
              ],
            },
            {
              type: "Heading",
              level: 4,
              content: "❌ Don'ts (Off-Brand Pitfalls to Avoid)",
            },
            {
              type: "Bullets",
              items: [
                'Don\'t use vague marketing jargon like "innovative solutions" or "cutting-edge."',
                "Don't position Swift as a traditional agency, consultancy, or dev shop.",
                "Don't overpromise outcomes - results must be shown through proof, not hype.",
                'Don\'t soften the voice with tentative phrases ("we try," "we hope"). Replace with assertive clarity ("we deliver," "we build," "we prove").',
                "Don't over-humanize with casual slang or emojis - Swift's tone is professional, modern, and outcome-driven.",
                "Don't hide the infrastructure. The platform, the embedded model, and the system approach are differentiators and should always be front and center.",
              ],
            },
          ],
        },
      ],
    },

    // CONTENT SECTION
    {
      title: "Content",
      subsections: [
        {
          title: "Keyword Opportunities",
          blocks: [
            {
              type: "Heading",
              level: 4,
              content: "Keyword analysis",
            },
            {
              type: "Paragraph",
              content:
                "Swift's keyword strategy focuses on owning mid-market B2B search intent across manufacturing, technology, services, and agency/partner ecosystems. The goal is to capture decision-makers searching for outsourced execution, embedded teams, CRM + analytics, and growth strategy-positioning Swift as the integrated alternative to fragmented agencies, consultants, and dev shops.",
            },
            {
              type: "Heading",
              level: 4,
              content: "Core Service Keywords (High Intent, Direct Fit)",
            },
            {
              type: "Bullets",
              items: [
                "outsourced marketing support",
                "embedded development team",
                "fractional operations partner",
                "CRM + analytics platform for mid-market businesses",
                "outsourced business strategy support",
              ],
            },
            {
              type: "Heading",
              level: 4,
              content: "Use Case Keywords (Functional Benefits)",
            },
            {
              type: "Bullets",
              items: [
                "workflow automation for manufacturers",
                "sales enablement for SaaS scaleups",
                "digital transformation for mid-market companies",
                "agency white-label execution partner",
                "CRM implementation for B2B growth",
              ],
            },
            {
              type: "Heading",
              level: 4,
              content: "Trust & Differentiation Keywords (Market Drivers)",
            },
            {
              type: "Bullets",
              items: [
                "growth without fragmentation",
                "embedded cross-functional team",
                "outcomes over hours",
                "strategy + execution partner",
                "momentum through connected disciplines",
              ],
            },
            {
              type: "Heading",
              level: 4,
              content: "B2B/Channel Keywords (Partnership + Ecosystem)",
            },
            {
              type: "Bullets",
              items: [
                "white-label marketing execution partner",
                "outsourced dev for agencies",
                "embedded team for consultants",
                "CRM + analytics white-label platform",
                "agency enablement partner",
              ],
            },
            {
              type: "Heading",
              level: 4,
              content: "Keyword Opportunity Analysis",
            },
            {
              type: "Paragraph",
              content: [
                {
                  text: "Phase 1: Mid-Market Ownership (Low Competition, High Relevance)",
                  bold: true,
                },
                {
                  text: '\nTarget niche intent like "fractional marketing support," "embedded development team," and "CRM for mid-market companies." Establish category clarity before broadening.',
                },
              ],
            },
            {
              type: "Paragraph",
              content: [
                {
                  text: "Phase 2: Category Expansion (Mid Competition, Category Building)",
                  bold: true,
                },
                {
                  text: '\nCompete on functional solutions: "workflow automation for B2B," "outsourced operations partner," "SaaS sales enablement."',
                },
              ],
            },
            {
              type: "Paragraph",
              content: [
                {
                  text: "Phase 3: High-Volume Capture (Broad Market, High Competition)",
                  bold: true,
                },
                {
                  text: '\nExpand into competitive, high-volume terms: "outsourced marketing agency," "business growth strategy," "CRM implementation services."',
                },
              ],
            },
          ],
        },
        {
          title: "Blog Strategy (Priority Ranking Topics)",
          blocks: [
            {
              type: "Paragraph",
              content:
                "Swift's blog strategy will position it as the go-to voice for clarity, infrastructure, and execution in the mid-market. Blogs will blend practical education, thought leadership, and credibility to show how connected systems outperform fragmented vendors.",
            },
            {
              type: "Heading",
              level: 4,
              content: "Hub 1: Growth Without Fragmentation (Education Hub)",
            },
            {
              type: "Bullets",
              items: [
                'Spoke: "Why Strategy Without Execution Stalls Growth"',
                'Spoke: "The True Cost of Siloed Agencies and Consultants"',
                'Spoke: "How Embedded Teams Build Sustainable Momentum"',
              ],
            },
            {
              type: "Heading",
              level: 4,
              content: "Hub 2: Tools & Infrastructure (Systems Hub)",
            },
            {
              type: "Bullets",
              items: [
                'Spoke: "5 Signs Your CRM is Holding You Back"',
                'Spoke: "Building a Scalable Analytics Backbone for B2B Companies"',
                'Spoke: "Automation Tools that Save Time-and Build Clarity"',
              ],
            },
            {
              type: "Heading",
              level: 4,
              content: "Hub 3: Industry Applications (Use Case Hub)",
            },
            {
              type: "Bullets",
              items: [
                'Spoke: "How Mid-Market Manufacturers Can Modernize Sales Ops"',
                'Spoke: "The SaaS Scaleup\'s Guide to Embedded Marketing Teams"',
                'Spoke: "Why Consultants Partner with Execution Experts"',
              ],
            },
            {
              type: "Heading",
              level: 4,
              content: "Hub 4: Partnerships & Ecosystems (Community Hub)",
            },
            {
              type: "Bullets",
              items: [
                'Spoke: "How Agencies Scale Faster with White-Label Partners"',
                'Spoke: "The Future of Outsourcing: Independence Moving Together"',
                'Spoke: "Client Spotlight: From Chaos to Clarity with Swift"',
              ],
            },
          ],
        },
        {
          title: "Blog Structure",
          blocks: [
            {
              type: "Paragraph",
              content: "Blogs must meet a word count of 750 words.",
            },
            {
              type: "Paragraph",
              content:
                "Each blog will follow a consistent framework to maximize readability, SEO, and conversion:",
            },
            {
              type: "Bullets",
              items: [
                "Title",
                "Introduction",
                "Problem/Need Context",
                "Core Insights (solutions, Swift's differentiation)",
                "Proof/Evidence (case studies, stats, examples)",
                "Practical Applications",
                "Industry/Market Trends",
                "Internal Links (other Swift content)",
                "External Sources (reputable stats, research)",
                "Call to Action",
                "About Swift",
              ],
            },
          ],
        },
        {
          title: "Social Strategy",
          blocks: [
            {
              type: "Paragraph",
              content:
                "The marketing kit and the Social Program Strategy section provide a clear, actionable framework for creating, writing, and designing organic social content. It is designed for internal creators to produce consistent, on-brand assets quickly.",
            },
            {
              type: "Paragraph",
              content:
                "We need a balanced mix of proof and case storytelling, thought leadership, system how-tos, behind-the-scenes team moments, and partner spotlights aligned to Swift's goals of clarity, momentum, and outcomes.",
            },
            {
              type: "Heading",
              level: 4,
              content: "Content preferences",
            },
            {
              type: "Bullets",
              items: [
                "Lead with outcomes, not hype, using short declarative statements that show how connected disciplines create momentum.",
                "Prioritize modern, structured visuals, clean grids, bold typography, and systems imagery that reinforce Support, Products, and Platform.",
                "Elevate credibility with case snippets, dashboards, and before-after narratives when available.",
                "Keep tone confident, precise, collaborative, and professional. Avoid casual slang and emoji.",
                "Align posts to mid-market B2B interests in manufacturing, technology, and services, plus agency white-label audiences.",
              ],
            },
            {
              type: "Heading",
              level: 4,
              content: "Required content mix",
            },
            {
              type: "Bullets",
              items: [
                "Static content, proof and case posts, thought leadership quotes, solution one-pagers translated to feed assets.",
                "Dynamic content, short-form videos for how-tos and system walkthroughs, stories for day-in-the-life and works-in-progress.",
                "Community and partner items, agency white-label spotlights, client wins, podcast episode clips, event or webinar promos and recaps.",
              ],
            },
            {
              type: "Heading",
              level: 4,
              content: "Creative Emphases",
            },
            {
              type: "Bullets",
              items: [
                "Growth without fragmentation, show embedded teams connecting design, marketing, development, operations, sales, and strategy.",
                "Outcomes over hours, highlight visible progress, speed to execution, and infrastructure that scales.",
                "Architect and Collective archetypes, balance system design with collaboration, independence aligned.",
                "Platform backbone, show CRM, analytics, and automation as the differentiator that turns activity into momentum.",
              ],
            },
            {
              type: "Heading",
              level: 4,
              content: "Primary Goals",
            },
            {
              type: "Bullets",
              items: [
                "Establish Swift as the trusted alternative to fragmented vendors and drive exploratory conversations.",
                "Demonstrate proof of execution speed and infrastructure through repeatable formats and case snippets.",
                "Attract partners and talent into the ecosystem by showcasing white-label wins and cross-disciplinary work.",
              ],
            },
            {
              type: "Heading",
              level: 4,
              content: "Primary Post Types",
            },
            {
              type: "Bullets",
              items: [
                "Static Feed",
                "Dynamic Stories",
                "Dynamic Reels",
                "Dynamic Videos",
                "Static UGC",
              ],
            },
            {
              type: "Heading",
              level: 4,
              content: "Notion Post Template, per post",
            },
            {
              type: "Bullets",
              items: [
                "Summary, what this post accomplishes, one line tied to Support, Products, or Platform.",
                "Copy, one to two sentences with a soft CTA to learn more or book exploratory at swiftinnovation.io.",
                "Hashtags, six to ten, mix of brand, category, and one audience or industry tag.",
                "Design Goal, clean grid, bold typographic hierarchy, systems imagery or artifact.",
                "Frequency, realistic cadence within the weekly rhythm.",
              ],
            },
            {
              type: "Heading",
              level: 4,
              content: "Social Examples",
            },
            {
              type: "Heading",
              level: 5,
              content: "Static Feed",
            },
            {
              type: "Bullets",
              items: [
                [
                  { text: "Summary", bold: true },
                  {
                    text: ", show a before-after of a fragmented stack replaced by Swift's connected system.",
                  },
                ],
                [
                  { text: "Copy", bold: true },
                  {
                    text: ", Most teams stall due to silos. We embed across disciplines so strategy, speed, and execution move together. See how a connected stack turned activity into outcomes, then let's plan your roadmap.",
                  },
                ],
                [
                  { text: "Hashtags", bold: true },
                  {
                    text: ", #SwiftInnovation #GrowthWithoutFragmentation #B2BMarketing #OpsEnablement #CRM #Analytics #AgencyPartners #MidMarket",
                  },
                ],
                [
                  { text: "Design Goal", bold: true },
                  {
                    text: ", side-by-side grid, simple system diagram, bold headline, minimal copy, clear CTA to swiftinnovation.io.",
                  },
                ],
                [
                  { text: "Frequency", bold: true },
                  { text: ", one to two times per week." },
                ],
              ],
            },
            {
              type: "Heading",
              level: 5,
              content: "Dynamic Stories",
            },
            {
              type: "Bullets",
              items: [
                [
                  { text: "Summary", bold: true },
                  {
                    text: ", day-in-the-life sequence showing design, marketing, and dev handoffs.",
                  },
                ],
                [
                  { text: "Copy", bold: true },
                  {
                    text: ", From brief to live, our teams move as one. Tap through the handoff trail, then grab the playbook link at the end.",
                  },
                ],
                [
                  { text: "Hashtags", bold: true },
                  {
                    text: ", #TeamInAction #SwiftInnovation #DesignToDev #B2BOperations #Workflow #Execution",
                  },
                ],
                [
                  { text: "Design Goal", bold: true },
                  {
                    text: ", quick storyboard panels, captioned steps, legible typography, link sticker to playbook on site.",
                  },
                ],
                [
                  { text: "Frequency", bold: true },
                  { text: ", two to three sequences per week." },
                ],
              ],
            },
            {
              type: "Heading",
              level: 5,
              content: "Dynamic Reels",
            },
            {
              type: "Bullets",
              items: [
                [
                  { text: "Summary", bold: true },
                  {
                    text: ", 30 to 45 second how-to breaking down a CRM or analytics setup step.",
                  },
                ],
                [
                  { text: "Copy", bold: true },
                  {
                    text: ", Five minutes to better visibility. Here is how we map events so leaders get real-time answers. Watch, then save for your next build.",
                  },
                ],
                [
                  { text: "Hashtags", bold: true },
                  {
                    text: ", #SwiftInnovation #CRMSetup #Analytics #HowTo #B2BGrowth #Operations",
                  },
                ],
                [
                  { text: "Design Goal", bold: true },
                  {
                    text: ", tight screen capture with callouts, large subtitles, clear hook, end card with URL.",
                  },
                ],
                [
                  { text: "Frequency", bold: true },
                  { text: ", one to two per month." },
                ],
              ],
            },
            {
              type: "Heading",
              level: 5,
              content: "Dynamic Videos",
            },
            {
              type: "Bullets",
              items: [
                [
                  { text: "Summary", bold: true },
                  {
                    text: ", 60 to 120 second founder or operator insight on outcomes over hours.",
                  },
                ],
                [
                  { text: "Copy", bold: true },
                  {
                    text: ", Strategy without delivery stalls growth. Here is how embedded teams convert plans into measurable outcomes. See the full breakdown on our site.",
                  },
                ],
                [
                  { text: "Hashtags", bold: true },
                  {
                    text: ", #SwiftInnovation #OutcomesOverHours #Leadership #GrowthStrategy #EmbeddedTeams",
                  },
                ],
                [
                  { text: "Design Goal", bold: true },
                  {
                    text: ", clean framing, lower-third headline, crisp audio, captioned for silent viewing, end slate with CTA.",
                  },
                ],
                [
                  { text: "Frequency", bold: true },
                  { text: ", one to two per month." },
                ],
              ],
            },
            {
              type: "Heading",
              level: 5,
              content: "Static UGC",
            },
            {
              type: "Bullets",
              items: [
                [
                  { text: "Summary", bold: true },
                  {
                    text: ", partner spotlight featuring an agency's white-label win with Swift behind the scenes.",
                  },
                ],
                [
                  { text: "Copy", bold: true },
                  {
                    text: ", Capacity without overhead. This partner scaled delivery while protecting margins, and their client saw clearer execution. Want a discreet extension of your team, let's talk.",
                  },
                ],
                [
                  { text: "Hashtags", bold: true },
                  {
                    text: ", #SwiftInnovation #WhiteLabel #AgencyPartners #DeliveryAtScale #B2BCreative #DevSupport",
                  },
                ],
                [
                  { text: "Design Goal", bold: true },
                  {
                    text: ", partner logo lockup with permission, single stat or quote if approved, neutral backdrop, clear attribution.",
                  },
                ],
                [
                  { text: "Frequency", bold: true },
                  { text: ", one to two times per month." },
                ],
              ],
            },
            {
              type: "Heading",
              level: 4,
              content: "Social Production Checklist",
            },
            {
              type: "Heading",
              level: 5,
              content: "Content Sources",
            },
            {
              type: "Bullets",
              items: [
                "Approved sources include Swift case materials, leadership insights, solution pages, CRM and analytics artifacts, and podcast clips.",
                "Use published site content at swiftinnovation.io, existing decks, and internal screenshots of systems when cleared.",
              ],
            },
            {
              type: "Heading",
              level: 5,
              content: "Design Tips",
            },
            {
              type: "Bullets",
              items: [
                "Use clean grids and clear hierarchy, large headlines and concise body text.",
                "Favor bold typography and systems or workflow imagery.",
                "Maintain ample spacing, avoid clutter, keep overlays minimal and legible.",
                "Ensure captions on video for silent playback, and provide descriptive alt text on images.",
                "Keep brand elements modern and structured, avoid heavy filters or novelty effects.",
              ],
            },
            {
              type: "Heading",
              level: 5,
              content: "Copy Guidelines",
            },
            {
              type: "Bullets",
              items: [
                "Voice is confident, precise, and outcome focused.",
                "Use declarative sentences that avoid jargon and filler.",
                "No emoji, no casual slang, no overpromising.",
                "Reference Support, Products, and Platform when relevant, tying posts to real artifacts or actions.",
                "Invite soft CTAs to learn more or book exploratory at swiftinnovation.io.",
              ],
            },
            {
              type: "Heading",
              level: 5,
              content: "Idea Starters",
            },
            {
              type: "Bullets",
              items: [
                "A three-panel before-after showing how a connected CRM and analytics stack changed weekly reporting.",
                "A reel that compresses an end-to-end handoff, brief to live, in under 45 seconds.",
                "A founder quote card on growth stalling from fragmentation, linked to a short blog.",
                "A partner spotlight on a white-label delivery win with a single approved proof point.",
                "A story sequence that tracks one task across design, marketing, and development in a single day.",
                "A quick how-to showing one automation that saves time and increases clarity.",
              ],
            },
            {
              type: "Heading",
              level: 4,
              content: "Cadence and Governance",
            },
            {
              type: "Paragraph",
              content:
                "Weekly rhythm aligns to the kit, three to five posts across LinkedIn, Instagram, and Facebook, plus two to three short-form videos per month and two to three thought leadership posts per month. Rotate formats to balance proof, thought leadership, how-tos, behind-the-scenes, and partner spotlights.",
            },
          ],
        },
      ],
    },

    // CAMPAIGN STRUCTURE SECTION
    {
      title: "Campaign Structure (Evergreen, Prospecting, Event)",
      blocks: [
        {
          type: "Paragraph",
          content: "Each Swift campaign should include:",
        },
        {
          type: "Bullets",
          items: [
            "3-6 Emails",
            "3-10 Social Posts",
            "1-3 Blogs",
            "0-2 Press Releases",
            "1 Landing Page or Funnel Page (built in either CRM or Website)",
          ],
        },
      ],
    },

    // LANDING PAGE STRATEGY SECTION
    {
      title: "Landing Page Strategy",
      blocks: [
        {
          type: "Paragraph",
          content:
            "Landing pages emphasize clarity, momentum, and outcomes-positioning Swift as the embedded partner that delivers growth without fragmentation.",
        },
        {
          type: "Heading",
          level: 3,
          content: "Landing Page Structure",
        },
        {
          type: "Bullets",
          items: [
            "Hero Section (headline + subheadline + CTA)",
            "Features/Benefits Section (value breakdown)",
            "Problem → Solution Section (storytelling)",
            "Visual/Offer Section (mockup/product image or explainer)",
            "Testimonials/Social Proof Section",
            "FAQ Section (optional but powerful)",
            "Final CTA Section (close strong, repeat offer)",
          ],
        },
        {
          type: "Heading",
          level: 3,
          content: "Landing Page Types",
        },
        {
          type: "Bullets",
          items: [
            [
              { text: "CRM Landing Page:", bold: true },
              { text: " CTA = Book Appointment" },
            ],
            [
              { text: "CRM Funnel Page (Event or Webinar):", bold: true },
              {
                text: " CTA = Register for In-Person and/ Online. Funnel Pages are 2-steps (1st step = lander with CTA, 2nd step is Acceptance of Registration)",
              },
            ],
            [
              { text: "Website Landing Page:", bold: true },
              { text: " CTA = Contact Us" },
            ],
          ],
        },
      ],
    },

    // REFERENCES SECTION
    {
      title: "References",
      blocks: [
        {
          type: "Bullets",
          items: [
            [
              { text: "DemandSage. (2025). " },
              {
                text: "Outsourcing Statistics: Key Facts and Trends",
                italic: true,
              },
              { text: ". Retrieved from " },
              {
                text: "https://www.demandsage.com/outsourcing-statistics/",
                link: "https://www.demandsage.com/outsourcing-statistics/",
              },
            ],
            [
              { text: "Wired. (2023). " },
              {
                text: "High-Value Freelancers Are Keeping the Wheels of Tech Turning",
                italic: true,
              },
              { text: ". Retrieved from " },
              {
                text: "https://www.wired.com/story/high-value-freelancers-are-keeping-the-wheels-of-tech-turning/",
                link: "https://www.wired.com/story/high-value-freelancers-are-keeping-the-wheels-of-tech-turning/",
              },
            ],
            [
              { text: "Wikipedia. (2025). " },
              { text: "Business process outsourcing", italic: true },
              { text: ". Retrieved from " },
              {
                text: "https://en.wikipedia.org/wiki/Business_process_outsourcing",
                link: "https://en.wikipedia.org/wiki/Business_process_outsourcing",
              },
            ],
            [
              { text: "Shekhar, S. (2022). " },
              {
                text: "Outsourcing for Innovation and Flexibility",
                italic: true,
              },
              { text: ". arXiv. Retrieved from " },
              {
                text: "https://arxiv.org/abs/2206.00982",
                link: "https://arxiv.org/abs/2206.00982",
              },
            ],
            [
              { text: "SICCODE.com. (n.d.). " },
              {
                text: "NAICS Code 459910 – Pet and Pet Supplies Retailers",
                italic: true,
              },
              { text: ". Retrieved 8-24-25, from siccode.com website: " },
              {
                text: "https://siccode.com/naics-code/459910/pet-pet-supplies-retailers",
                link: "https://siccode.com/naics-code/459910/pet-pet-supplies-retailers",
              },
            ],
          ],
        },
      ],
    },
  ],
};

export default function App() {
  return (
    <div className="min-h-screen bg-gray-50 py-8 px-6">
      <MarketingKit data={sampleData} />
    </div>
  );
}
