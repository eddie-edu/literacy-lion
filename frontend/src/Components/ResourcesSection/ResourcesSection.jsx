function RessourcesSection() {
    return (
        <section className="resources" id="resources" aria-labelledby="resources-title">
            <h2 id="resources-title">Resources</h2>
            {/*teachers can eventually filter resources using these*/}
            <ul className="type-filters" aria-label="Resource types">
                <li>
                    <a href="#">Research/Evidence</a>
                </li>
                <li>
                    <a href="#">Strategy</a>
                </li>
                <li>
                    <a href="#">Classroom Example</a>
                </li>
                <li>
                    <a href="#">Planning Tool</a>
                </li>
                <li>
                    <a href="#">AI Example</a>
                </li>
                <li>
                    <a href="#">Professional Learning &amp; Support</a>
                </li>
            </ul>
            {/*sample resource cards for now*/}
            <ul className="card-grid light">
                <li className="card c-crimson">
                    <p className="type-pill">Strategy</p>
                    <h3>
                        <a href="#">Teaching vocabulary with visuals and gestures</a>
                    </h3>
                    <p className="source">[Source]</p>
                </li>
            </ul>
        </section>
    );
}

export default RessourcesSection;