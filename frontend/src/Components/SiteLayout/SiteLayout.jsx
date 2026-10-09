import PennStateBranding from '../PennStateBranding/PennStateBranding';
import TopBar from '../TopBar/TopBar';
import NavigationBar from '../Navigation_bar/navigation_bar';
import Footer from '../Footer/Footer';

/*the universal parts every page shares i.e. Penn State bar, navigation, footer*/
function SiteLayout({ title, current, children }) {
    return (
        <>
            <title>{title}</title>

            {/*official penn state branding and project bar at the top*/}
            <div className="penn-state-branding-container">
                <PennStateBranding />
                <TopBar />
            </div>

            {/*current is the id of the nav link to highlight, for example "resources"*/}
            <NavigationBar current={current} />

            <main id="main">
                {children}
            </main>

            <Footer />
        </>
    );
}

export default SiteLayout;
