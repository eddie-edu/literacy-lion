/*current is the id of the page to highlight. exists for screen readers and the highlight style*/
function NavigationBar({ current = 'start-here' }) {
    const page = (id) => (current === id ? 'page' : undefined);

    return (
        <div>
        <header className="site-header">
    {/*literacy lion branding goes here*/}
    <a className="logo" href="#top">
      {/*swap this with the real lion logo when we have it*/}
      <span className="logo-word">
        literacy<span>lion.</span>
      </span>
      <span className="logo-sub">Penn State Abington</span>
    </a>
    {/*these are the main areas teachers can move through*/}
    <nav className="main-nav" aria-label="Main">
      <ul>
        {/*added "/" to front of links so they also work from other pages*/}
        <li><a href="/#start-here" aria-current={page('start-here')}> Start Here</a></li>
        <li><a href="/#know-your-learners" aria-current={page('know-your-learners')}>Know Your Learners</a> </li>
        <li><a href="/#teach-literacy" aria-current={page('teach-literacy')}>Teach Literacy</a></li>
        <li><a href="/#translanguaging" aria-current={page('translanguaging')}>Translanguaging</a></li>
        <li><a href="/#plan-differentiate" aria-current={page('plan-differentiate')}>Plan &amp; Differentiate</a></li>
        <li><a href="/#ai-decisions" aria-current={page('ai-decisions')}>AI + Teacher Decisions</a></li>
        <li><a href="/resources" aria-current={page('resources')}>Resources</a></li>
      </ul>
    </nav>
    
    {/*this will eventually open leo*/}
 <a className="button button-primary" href="#">
      Chat with Leo
    </a>
  </header>
        </div>
    );
}

export default NavigationBar;