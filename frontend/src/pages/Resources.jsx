import SiteLayout from '../Components/SiteLayout/SiteLayout';
import ResourceLibrary from '../Components/ResourceLibrary/ResourceLibrary';

const Grades = [
    { id: 'k', label: 'Kindergarten' },
    { id: '1', label: '1st grade' },
    { id: '2', label: '2nd grade' },
];

/*resource categories/filters changed to fit client feedback
section comes from the main navigation tabs (which part of the site a resource belongs to)
type comes from the client's resource designations (what kind of resource it is)*/

const Sections = [
    { id: 'know-your-learners', label: 'Know Your Learners', color: 'var(--cat-crimson)' },
    { id: 'teach-literacy', label: 'Teach Literacy', color: 'var(--cat-blue)' },
    { id: 'translanguaging', label: 'Translanguaging', color: 'var(--cat-purple)' },
    { id: 'plan-differentiate', label: 'Plan & Differentiate', color: 'var(--cat-teal)' },
    { id: 'ai-decisions', label: 'AI + Teacher Decisions', color: 'var(--cat-yellow)' },
    { id: 'resources', label: 'Resources', color: 'var(--cat-green)' },
];

const Types = [
    { id: 'research-evidence', label: 'Research/Evidence' },
    { id: 'strategy', label: 'Strategy' },
    { id: 'classroom-example', label: 'Classroom Example' },
    { id: 'planning-tool', label: 'Planning Tool' },
    { id: 'ai-example', label: 'AI Example' },
    { id: 'professional-learning', label: 'Professional Learning & Support' },
];

const filterGroups = [
    { legend: 'Grade', options: Grades },
    { legend: 'Section', options: Sections },
    { legend: 'Type', options: Types },
];

/*placeholder resources*/
const Resources = [
    { title: 'Vocabulary development', section: 'teach-literacy', type: 'strategy', grades: 'K–2' },
    { title: 'What research says about vocabulary instruction for ELs', section: 'teach-literacy', type: 'research-evidence', grades: 'K–2' },
    { title: 'Vocabulary lesson example', section: 'teach-literacy', type: 'classroom-example', grades: 'K–1' },
    { title: 'Vocabulary planning template', section: 'teach-literacy', type: 'planning-tool', grades: 'K–2' },
    { title: 'Using AI to generate vocabulary supports', section: 'teach-literacy', type: 'ai-example', grades: '1–2' },
    { title: 'Engage families and communities', section: 'know-your-learners', type: 'strategy', grades: 'K–2' },
    { title: 'Learning about your students’ languages and strengths', section: 'know-your-learners', type: 'planning-tool', grades: 'K–2' },
    { title: 'Using home languages to support reading in English', section: 'translanguaging', type: 'strategy', grades: 'K–2' },
    { title: 'Translanguaging in a read-aloud', section: 'translanguaging', type: 'classroom-example', grades: 'K–1' },
    { title: 'Differentiating a lesson for multilingual readers', section: 'plan-differentiate', type: 'planning-tool', grades: '1–2' },
    { title: 'Checking AI suggestions before you use them', section: 'ai-decisions', type: 'ai-example', grades: 'K–2' },
    { title: 'Professional learning and support', section: 'resources', type: 'professional-learning', grades: 'K–2' },
];

/*turn each resource into a card; section determines band color and type shows next to the tag*/
const cards = Resources.map((resource) => {
    const section = Sections.find((item) => item.id === resource.section);
    const type = Types.find((item) => item.id === resource.type);
    return {
        title: resource.title,
        tag: section.label,
        color: section.color,
        meta: `${type.label} · ${resource.grades}`,
        stacked: true,
    };
});

function Archive() {
    return (
        <SiteLayout title="Resources | Literacy Lion" current="resources">
            <ResourceLibrary
                heading="Resources"
                intro="Evidence, examples, tools, and professional learning for teachers of young multilingual readers. Hover a card for its summary, then open the original in a new tab."
                searchHint="Try vocabulary, families, or planning template"
                filterGroups={filterGroups}
                cards={cards}
            />
        </SiteLayout>
    );
}

export default Archive;
