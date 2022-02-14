import { Link } from "react-router-dom";
import { 
    Container, 
    Navbar, 
    Nav, 
    Form,
    FormControl,
    Button} from "react-bootstrap";
import 'bootstrap/dist/css/bootstrap.min.css';

const Navigation = () => {
    return (
        <div>
            <Navbar bg="light" expand="lg">
              <Container>
                <Navbar.Brand href="/">
                    <img
                      alt=""
                      src="img/island.svg"
                      width="30"
                      height="30"
                      className="d-inline-block align-top"
                    />{' '}SUMM
                </Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                  <Nav className="me-auto">
                    <Nav.Link href="/">Main</Nav.Link>
                    <Nav.Link href="/slider">slider</Nav.Link>
                    <Form className="d-flex">
                        <FormControl
                          type="search"
                          placeholder="Search keyword"
                          className="me-2"
                          aria-label="Search"
                        />
                        <Button variant="outline-info">Search</Button>
                    </Form>
                  </Nav>
                </Navbar.Collapse>
              </Container>
            </Navbar>
        </div>
    );
};
export default Navigation;