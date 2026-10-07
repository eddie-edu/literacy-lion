import Card from "../Components/Cards";

function Landing_page(){
    return(
        <header>
            <h1>Literacy Lion</h1>
            <nav className="nav-menu">
                <ul>
                    <li><a href="#landing_page">Home</a></li>
                    <li><a href="#ask_leo">AskLeo</a></li>
                    <li><a href="#about">About</a></li>
                    <li><a href="#archive">Archive</a></li>
                    <li><a href="#FAQ">FAQ</a></li>
                    <li><a href="Terms_and_conditions">Terms and Conditions</a></li>
                    <li><a href="#contact">Contact</a></li>
                    <li><a href="#login">Login</a></li>
                </ul>
            </nav>
            <button className="AskLeo2">Ask Leo</button>
            <Card>
            </Card>
        </header>
    );
}
export default Landing_page