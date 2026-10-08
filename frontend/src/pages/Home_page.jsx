import NavigationBar from "../Components/Navigation_bar/navigation_bar";
import Footer from "../Components/Footer/Footer";
import How_Lit_LionWorks from "../Components/How_LitLionWorks/How_LitLionWorks";
import PennStateBranding from "../Components/PennStateBranding/PennStateBranding";
import Hero from "../Components/Hero/Hero";
import TopBar from "../Components/TopBar/TopBar";
import Mission from "../Components/Mission/Mission";
import TipRow from "../Components/TipRow/TipRow";
import RessourcesSection from "../Components/ResourcesSection/ResourcesSection";
import PartnerStrip from "../Components/PartnerStrip/PartnerStrip";

function Home_page() {
    return (
        <>
  <title>Literacy Lion | Penn State Abington</title>
{/*these links are placeholders until the real pages are made*/}

  {/*official penn state branding at the top*/}
  <div className="penn-state-branding-container">
    <PennStateBranding />
      {/*small bar showing the penn state project info*/}
  <TopBar/>
  </div>

  {/*this is the main header and navigation*/}
  <NavigationBar/>
  
{/*this is the main hero section*/}
<Hero/>
    {/*this section helps teachers choose where to start*/}
<How_Lit_LionWorks/>
    {/*this is the mission section*/}
    <Mission/>
    {/*this section has the literacy tip and ai decision making*/}
    <TipRow/>
    {/*this section shows the different resource types*/}
    <RessourcesSection/>
    {/*this section explains the penn state connection*/}
    <PartnerStrip/>

    <Footer/>
</>
    );
}

export default Home_page;