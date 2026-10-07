function Footer(){
    return(
        <footer>
            {/*footer links for the main parts of the site*/}
    <nav className="footer-nav" aria-label="Footer">
      <div>
        <h2>Explore</h2>
        <ul>
          <li><a href="#start-here">Start Here</a></li>
          <li><a href="#resources">Resources</a></li>
          <li><a href="#">Chat with Leo</a></li>
        </ul>
      </div>

      <div>
        <h2>Learn</h2>
        <ul>
          <li><a href="#">About us</a></li>
          <li><a href="#">FAQ</a></li>
          <li><a href="#">Terms &amp; Privacy</a></li>
        </ul>
      </div>
      
      <div>
        <h2>Contact</h2>
        <p>[Project contact email]</p>
      </div>
    </nav>
    {/*small credit at the bottom*/}
            <p className="footer-credit">&copy; {new Date().getFullYear()} Literacy Lion. · Penn State Abington · Built by the CMPSC 487
      capstone team · All rights reserved.</p>
        </footer>
    );
}
export default Footer