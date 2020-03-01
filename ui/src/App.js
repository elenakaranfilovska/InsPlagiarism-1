import React, { Component } from 'react';
import './App.css';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.css';

class App extends Component {

  constructor(props) {
    super(props);

    this.state = {
      isLoading: false,
      formData: {
        fileupload1: '',
        fileupload2: '',
      },
      result: ""
    };
  }

  handleChange = (event) => {
    const value = event.target.value;
    const name = event.target.name;
    var formData = this.state.formData;
    formData[name] = value;
    this.setState({
      formData
    });
  }
  loadFileAsText = (event) => {
  var file= event.target.files[0];
  var name=event.target.name;
    let reader=new FileReader()
     var formData = this.state.formData;
     var content="";
  reader.onload = function() {
    formData[name]=reader.result;
  };
    reader.readAsText(file);
    this.setState({
      formData
    });
  }

  handlePredictClick = (event) => {
    const formData = this.state.formData;
    this.setState({ isLoading: true });
    fetch('http://127.0.0.1:5000/prediction/',
      {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: 'POST',
        body: JSON.stringify(formData)
      })
      .then(response => response.json())
      .then(response => {
        this.setState({
          result: response.result,
          isLoading: false
        });
      });
  }

  handleCancelClick = (event) => {
    this.setState({ result: "" });
  }


  render() {
    const isLoading = this.state.isLoading;
    const formData = this.state.formData;
    const result = this.state.result;

    return (
      <Container>
        <div>
          <img className="logo rounded mx-auto d-block" src="https://image.freepik.com/free-vector/working-copier-printer_90508-126.jpg" alt=""/>
          <h1 className="text-center text-dark display-4 dark-gray text-monospace pt-0">InsPlagiarism</h1>
        </div>
        <div className="content">
          <Form>
            <Form.Row>
              <Form.Group as={Col}>
                <Form.Label>File 1</Form.Label>
                 <Form.Control
                  type="file"
                  placeholder="Insert File"
                  name="fileupload1"
                  id="fileToLoad"
                  onChange={this.loadFileAsText} />
              </Form.Group>
              <Form.Group as={Col}>
                <Form.Label>File 2</Form.Label>
                <Form.Control
                  type="file"
                  placeholder="Insert File"
                  name="fileupload2"
                  onChange={this.loadFileAsText} />
              </Form.Group>
            </Form.Row>
            <Row>
              <Col>
                <Button
                  block
                  variant="dark"
                  className="text-monospace"
                  disabled={isLoading}
                  onClick={!isLoading ? this.handlePredictClick : null}>
                  { isLoading ? 'Making prediction' : 'Predict' }
                </Button>
              </Col>
            </Row>
          </Form>
          {result === "" ? null :
            (<Row>
              <Col className="result-container">
                <h5 id="result">{result}</h5>
              </Col>
            </Row>)
          }
        </div>

      </Container>
    );
  }
}

export default App;
