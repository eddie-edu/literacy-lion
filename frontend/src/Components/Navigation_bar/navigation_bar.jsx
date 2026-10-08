function NavigationBar() {
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
        <li><a href="#start-here" aria-current="page"> Start Here</a></li>
        <li><a href="#know-your-learners">Know Your Learners</a> </li>
        <li><a href="#teach-literacy">Teach Literacy</a></li>
        <li><a href="#translanguaging">Translanguaging</a></li>
        <li><a href="#plan-differentiate">Plan &amp; Differentiate</a></li>
        <li><a href="#ai-decisions">AI + Teacher Decisions</a></li>
        <li><a href="#resources">Resources</a></li>
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