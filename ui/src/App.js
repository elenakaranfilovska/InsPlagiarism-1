import React, { Component } from 'react';
import './App.css';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.css';

import ReactHover from 'react-hover';

class App extends Component {

  constructor(props) {
    super(props);

    this.state = {
      isLoading: false,
      formData: {
        fileupload1: '',
        fileupload2: '',
      },
      result: "",
      maxSentencePercentPlagiat: "",
      staticServerHeatMapUrl: "http://127.0.0.1:4999/heatmap",
      options : {
        followCursor:true,
        shiftX: 20,
        shiftY: 0
      }
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
    //this.refs.name.innerHTML=this.state.formData[name];
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
          maxSentencePercentPlagiat: response.maxSentencePercentPlagiat,
          isLoading: false
        });
      });
  }


  handleCancelClick = (event) => {
    this.setState({ result: "" });
  }

  filterString = (str) =>{
    str = str.replace(/\[/g, '');
    str = str.replace(/\]/g, '');
     str = str.replace(/\\/g, '');
     str = str.replace(/,/g, '');
     str = str.replace(/'/g, '');
    return str;
  }
  


  render() {
    const isLoading = this.state.isLoading;
    const formData = this.state.formData;
    const result = this.state.result;
    const maxSentencePercentPlagiat = this.state.maxSentencePercentPlagiat;

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

                <h5 id="result">{this.filterString(result)}</h5>
                <h5 id="result">{this.filterString(maxSentencePercentPlagiat)}</h5>
                <a key={Math.random()} href={this.state.staticServerHeatMapUrl} target="_blank">
                  <img key={Math.random()} className="img-fluid mx-auto" src={this.state.staticServerHeatMapUrl} disableCache="true"></img>
                </a>

              </Col>
            </Row>)
          }
        </div>

        
        {result === "" ? null :<div>
        <h2>Text1</h2> 
        {this.state.formData['fileupload1'].split("\n").map((value, index) => {
            return <p>{value}</p>
            })}
          <br/>
          <br/>
        </div> }

           
          {result === "" ? null : <div><h2>Text2</h2> <h6 className="text-center">Hover on sentences to see percentage.</h6></div>}
          <br/>
          
          {this.state.formData['fileupload2'].split("\n").map((value, index) => {

            return <ReactHover options={this.state.options}>
            <ReactHover.Trigger type='trigger'>
            <div> {value} </div>
            </ReactHover.Trigger>
            <ReactHover.Hover type='hover'>
            <h6> {this.filterString(maxSentencePercentPlagiat).split(" ")[index]} % </h6>
            </ReactHover.Hover>
            </ReactHover>
            })}
<br/><br/><br/>
      </Container>
      
    );
  }
}

export default App;


