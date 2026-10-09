/*stacked puts meta text under the tag instead of beside it for long type names*/
function ResourceCard({
                          title, tag, color, meta,
                          stacked = false,
                          source = '[Source]',
                          href = '#',
                          summary = '[Placeholder summary of the resource.]' }) {
    return (
        /*color sets the band across the top of a card and the tint of the tag*/
        <article className="resource-card" style={{ '--topic': color }}>
            <div className={stacked ? 'card-meta card-meta-stacked' : 'card-meta'}>
                <span className="topic-tag">{tag}</span>
                <span>{meta}</span>
            </div>
            <h3>{title}</h3>
            <div className="card-footer">
                <span>{source}</span>
                <a href={href} target="_blank" rel="noopener noreferrer">
                    Open<span className="visually-hidden"> (opens in new tab)</span>
                </a>
            </div>
            {/*floats below the card after hovering for a second, or right away on keyboard focus*/}
            <div className="card-summary">
                <p>{summary}</p>
            </div>
        </article>
    );
}

export default ResourceCard;
