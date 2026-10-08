function TipRow() {
    return (
        <section className="tip-row">
            <article className="notebook" aria-labelledby="tip-title">
                <p id="tip-title" className="tip-label">
                    Today's literacy tip
                </p>
                <h2>Pre-teach key words with a picture and a gesture.</h2>
                <p>
                    Before a read-aloud, introduce three to five essential words with an
                    image and a simple motion.
                </p>
                <p>
                    <a href="#resources">Find related resources</a>
                </p>
            </article>
            <aside className="ai-card" id="ai-decisions" aria-labelledby="ai-title">
                <h2 id="ai-title">AI + Teacher Decision-Making</h2>
                <ul className="check-list">
                    <li>Leo uses approved resources only, not the open web.</li>
                    <li>Every suggestion shows its source.</li>
                    <li>You check it and make the call.</li>
                </ul>
                <p>
                    <a className="button button-primary" href="#">
                        Chat with Leo
                    </a>
                </p>
            </aside>
        </section>
    );
}

export default TipRow;