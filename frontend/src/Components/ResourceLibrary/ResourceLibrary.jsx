import ResourceCard from '../ResourceCard/ResourceCard';

/*layout of the resource page i.e. title, search, filters, cards and page numbers.
The filter groups and card details are set in ResourceCard and imported so it's easier to change if needed*/
function ResourceLibrary({ heading, intro, searchHint, filterGroups, cards }) {
    return (
        <div className="resources-page">

            {/*title area for this page*/}
            <header className="library-header">
                <h1>{heading}</h1>
                <p>{intro}</p>
            </header>

            <div className="library-body">

                {/*search box and sort dropdown are layout only for now*/}
                <div className="library-tools">
                    <div className="library-field">
                        <label htmlFor="resource-search">Search resources</label>
                        <input id="resource-search" type="search" placeholder={searchHint} />
                    </div>
                    <div className="library-field">
                        <label htmlFor="resource-sort">Sort by</label>
                        <select id="resource-sort" defaultValue="relevant">
                            <option value="relevant">Most relevant</option>
                            <option value="az">A–Z</option>
                        </select>
                    </div>
                </div>

                <div className="library-layout">

                    {/*filters are layout only for now*/}
                    <aside className="library-filters" aria-label="Filters">
                        {filterGroups.map((group) => (
                            <fieldset key={group.legend}>
                                <legend>{group.legend}</legend>
                                {group.options.map((option) => (
                                    <label key={option.id}>
                                        <input type="checkbox" />
                                        {option.color && (
                                            <span className="topic-dot"
                                                  style={{ '--topic': option.color }}
                                                  aria-hidden="true"></span>
                                        )}
                                        {option.label}
                                    </label>
                                ))}
                            </fieldset>
                        ))}
                        <button className="button button-primary" type="button">Clear filters</button>
                    </aside>

                    <section aria-label="Resources">
                        <p className="results-count">Showing {cards.length} of [N] resources</p>

                        <div className="resource-grid">
                            {cards.map((card) => (
                                <ResourceCard key={card.title} {...card} />
                            ))}
                        </div>

                        {/*page numbers are placeholders for now*/}
                        <nav className="pagination" aria-label="Pagination">
                            <a href="#">Previous</a>
                            <a href="#" aria-current="page">1</a>
                            <a href="#">2</a>
                            <a href="#">3</a>
                            <a href="#">Next</a>
                        </nav>
                    </section>

                </div>
            </div>
        </div>
    );
}

export default ResourceLibrary;
