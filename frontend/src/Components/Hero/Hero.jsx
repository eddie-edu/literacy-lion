import literacyCircleIllustration from '../../Assets/literacy-circle-illustration.jpg';
function Hero() {
    return (
        <section className="hero" id="top">
            <p className="badge">For new teachers of K–2 English learners</p>
            <h1>Every young reader deserves a <em>confident</em> teacher.</h1>
            <p className="lead">
                Strategies, examples, and planning tools for teachers of young
                multilingual readers.
            </p>
            <p className="hero-actions"><a className="button button-primary" href="#start-here">
                    Start here
                </a>
                <a className="button button-secondary" href="#resources">
                    Browse resources
                </a>
            </p>
            <div
                className="hero-image"
                role="img"
                aria-label="Illustration placeholder: students reading and writing with their teacher"
            >
                <img src={literacyCircleIllustration} alt="Illustration placeholder: students reading and writing with their teacher" className={Hero.heroImage}/>
            </div>
        </section>
    );
}
export default Hero;